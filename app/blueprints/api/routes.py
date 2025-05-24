from flask import request, abort, jsonify, current_app
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, TextMessageContent
import os
import pandas as pd
from datetime import datetime

from app.bus_status import get_bus_status
from app.bus_time import get_last_5_bus_times
from app.food_status import get_food_status
from . import bp
from app import db
from app.models.timetable import Timetable

configuration = Configuration(access_token=os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("LINE_CHANNEL_SECRET"))

@bp.route("/line/webhook", methods=['POST'])
def line_webhook():
    signature = request.headers.get('X-Line-Signature')
    if not signature:
        current_app.logger.warning("署名ヘッダがありません")
        abort(400)
    body = request.get_data(as_text=True)
    current_app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        current_app.logger.warning("署名検証失敗")
        abort(403)
    except Exception as e:
        current_app.logger.error(f"Webhook処理中に例外: {e}")
        abort(500)
    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        try:
            if event.message.text == "運行予定":
                reply_text = get_bus_status(7)
            elif event.message.text == "問い合わせ":
                reply_text = "お問い合わせはこちらから \n https://forms.gle/Q3vcxdm2mXz2fBTK8"
            else:
                try:
                    bustype, direction = event.message.text.split("_")
                    reply_text = get_last_5_bus_times(bustype, int(direction)+1)
                except Exception:
                    reply_text = "コマンドが不正です。"
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=reply_text)]
                )
            )
        except Exception as e:
            current_app.logger.error(f"返信処理中に例外: {e}")
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="エラーが発生しました")]
                )
            )

@bp.route('/timetable/upload', methods=['POST'])
def upload_timetable():
    if 'file' not in request.files:
        return jsonify({'error': 'ファイルがアップロードされていません'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'ファイルが選択されていません'}), 400
    
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'CSVファイルのみアップロード可能です'}), 400
    
    try:
        df = pd.read_csv(file)
        required_columns = ['route', 'direction', 'departure_time', 'arrival_time', 'valid_from', 'valid_to']
        if not all(col in df.columns for col in required_columns):
            return jsonify({'error': '必要なカラムが不足しています'}), 400
        
        for _, row in df.iterrows():
            timetable = Timetable(
                route=row['route'],
                direction=row['direction'],
                departure_time=datetime.strptime(row['departure_time'], '%H:%M:%S').time(),
                arrival_time=datetime.strptime(row['arrival_time'], '%H:%M:%S').time() if pd.notna(row['arrival_time']) else None,
                valid_from=datetime.strptime(row['valid_from'], '%Y-%m-%d').date(),
                valid_to=datetime.strptime(row['valid_to'], '%Y-%m-%d').date() if pd.notna(row['valid_to']) else None
            )
            db.session.add(timetable)
        
        db.session.commit()
        return jsonify({'message': '時刻表のアップロードが完了しました'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'アップロード中にエラーが発生しました: {str(e)}'}), 500

@bp.route('/timetable/download', methods=['GET'])
def download_timetable():
    try:
        timetables = Timetable.query.all()
        data = []
        for t in timetables:
            data.append({
                'route': t.route,
                'direction': t.direction,
                'departure_time': t.departure_time.strftime('%H:%M:%S'),
                'arrival_time': t.arrival_time.strftime('%H:%M:%S') if t.arrival_time else None,
                'valid_from': t.valid_from.strftime('%Y-%m-%d'),
                'valid_to': t.valid_to.strftime('%Y-%m-%d') if t.valid_to else None
            })
        
        df = pd.DataFrame(data)
        csv_path = os.path.join('static', 'downloads', 'timetable.csv')
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        df.to_csv(csv_path, index=False)
        
        return jsonify({'message': '時刻表のダウンロードが完了しました', 'path': csv_path}), 200
    
    except Exception as e:
        return jsonify({'error': f'ダウンロード中にエラーが発生しました: {str(e)}'}), 500

# ここにAPI用のルートを追加予定 