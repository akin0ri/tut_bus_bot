from flask import request, abort, jsonify, current_app
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, TextMessageContent
import os
import pandas as pd
from datetime import datetime, timezone, timedelta
import logging

from app.bus_status import get_bus_status
from app.bus_time import get_last_5_bus_times
from app.food_status import get_food_status
from . import bp
from app import db
from app.models.timetable import Timetable

logger = logging.getLogger(__name__)

configuration = Configuration(access_token=os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("LINE_CHANNEL_SECRET"))

@bp.route("/line/webhook", methods=['POST'])
def line_webhook():
    signature = request.headers.get('X-Line-Signature')
    if not signature:
        logger.warning("署名ヘッダがありません")
        abort(400)
    body = request.get_data(as_text=True)
    logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.warning("署名検証失敗")
        abort(403)
    except Exception as e:
        logger.error(f"Webhook処理中に例外: {e}")
        abort(500)
    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    logger.info(f"メッセージ受信: {event.message.text}")
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        try:
            if event.message.text == "運行予定":
                logger.info("運行予定コマンドを受信")
                reply_text = get_bus_status(7)
            elif event.message.text == "問い合わせ":
                logger.info("問い合わせコマンドを受信")
                reply_text = "お問い合わせはこちらから \n https://forms.gle/Q3vcxdm2mXz2fBTK8"
            else:
                try:
                    # コマンドを分割
                    parts = event.message.text.split("_")
                    bustype = parts[0]
                    
                    # 日時指定がある場合
                    specified_datetime = None
                    if len(parts) >= 3:
                        try:
                            date_str = parts[2]
                            time_str = parts[3] if len(parts) > 3 else "000000"
                            datetime_str = f"{date_str}{time_str}"
                            specified_datetime = datetime.strptime(datetime_str, "%Y%m%d%H%M%S")
                            specified_datetime = specified_datetime.replace(tzinfo=timezone(timedelta(hours=+9), 'JST'))
                            logger.info(f"指定日時: {specified_datetime}")
                        except (ValueError, IndexError) as e:
                            logger.warning(f"日時指定の解析に失敗: {str(e)}")
                            specified_datetime = None
                    
                    direction = int(parts[1])
                    logger.info(f"時刻表確認コマンドを受信: bustype={bustype}, direction={direction}, 指定日時={specified_datetime}")
                    
                    # 路線名の英語表記を漢字に変換
                    route_map = {
                        "hachioji": "八王子",
                        "minamino": "南野",
                        "kamata": "蒲田"
                    }
                    if bustype in route_map:
                        # directionの定義:
                        # hachioji_0: 大学 -> 八王子駅
                        # hachioji_1: 八王子駅 -> 大学
                        # minamino_0: 大学 -> 八王子みなみ野駅
                        # minamino_1: 八王子みなみ野駅 -> 大学
                        reply_text = get_last_5_bus_times(route_map[bustype], direction, specified_datetime)
                    else:
                        logger.warning(f"不正な路線名: {bustype}")
                        reply_text = "コマンドが不正です。\n\n使用可能なコマンド:\n" + \
                                   "1. 運行予定\n" + \
                                   "2. 問い合わせ\n" + \
                                   "3. 時刻表確認:\n" + \
                                   "   - hachioji_0: 大学 -> 八王子駅\n" + \
                                   "   - hachioji_1: 八王子駅 -> 大学\n" + \
                                   "   - minamino_0: 大学 -> 八王子みなみ野駅\n" + \
                                   "   - minamino_1: 八王子みなみ野駅 -> 大学\n" + \
                                   "   - kamata_0: 大学 -> 蒲田駅\n" + \
                                   "   - kamata_1: 蒲田駅 -> 大学\n" + \
                                   "   ※日時指定: _YYYYMMDD_HHMMSS を追加可能\n" + \
                                   "   例: hachioji_0_20240524_120000"
                except ValueError as ve:
                    logger.error(f"コマンド形式エラー: {str(ve)}")
                    reply_text = "コマンドが不正です。\n\n使用可能なコマンド:\n" + \
                               "1. 運行予定\n" + \
                               "2. 問い合わせ\n" + \
                               "3. 時刻表確認:\n" + \
                               "   - hachioji_0: 大学 -> 八王子駅\n" + \
                               "   - hachioji_1: 八王子駅 -> 大学\n" + \
                               "   - minamino_0: 大学 -> 八王子みなみ野駅\n" + \
                               "   - minamino_1: 八王子みなみ野駅 -> 大学\n" + \
                               "   - kamata_0: 大学 -> 蒲田駅\n" + \
                               "   - kamata_1: 蒲田駅 -> 大学\n" + \
                               "   ※日時指定: _YYYYMMDD_HHMMSS を追加可能\n" + \
                               "   例: hachioji_0_20240524_120000"
                except Exception as e:
                    logger.error(f"予期せぬエラー: {str(e)}")
                    reply_text = "コマンドが不正です。\n\n使用可能なコマンド:\n" + \
                               "1. 運行予定\n" + \
                               "2. 問い合わせ\n" + \
                               "3. 時刻表確認:\n" + \
                               "   - hachioji_0: 大学 -> 八王子駅\n" + \
                               "   - hachioji_1: 八王子駅 -> 大学\n" + \
                               "   - minamino_0: 大学 -> 八王子みなみ野駅\n" + \
                               "   - minamino_1: 八王子みなみ野駅 -> 大学\n" + \
                               "   - kamata_0: 大学 -> 蒲田駅\n" + \
                               "   - kamata_1: 蒲田駅 -> 大学\n" + \
                               "   ※日時指定: _YYYYMMDD_HHMMSS を追加可能\n" + \
                               "   例: hachioji_0_20240524_120000"
            logger.info(f"返信メッセージ: {reply_text}")
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=reply_text)]
                )
            )
        except Exception as e:
            logger.error(f"返信処理中に例外: {e}")
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="エラーが発生しました")]
                )
            )

@bp.route('/timetable/upload', methods=['POST'])
def upload_timetable():
    logger.info("時刻表アップロードリクエスト受信")
    if 'file' not in request.files:
        logger.warning("ファイルがアップロードされていません")
        return jsonify({'error': 'ファイルがアップロードされていません'}), 400
    
    file = request.files['file']
    if file.filename == '':
        logger.warning("ファイルが選択されていません")
        return jsonify({'error': 'ファイルが選択されていません'}), 400
    
    if not file.filename.endswith('.csv'):
        logger.warning("CSVファイル以外がアップロードされました")
        return jsonify({'error': 'CSVファイルのみアップロード可能です'}), 400
    
    try:
        df = pd.read_csv(file)
        required_columns = ['route', 'direction', 'departure_time', 'arrival_time', 'valid_from', 'valid_to']
        if not all(col in df.columns for col in required_columns):
            logger.warning("必要なカラムが不足しています")
            return jsonify({'error': '必要なカラムが不足しています'}), 400
        
        for _, row in df.iterrows():
            # is_shuttle関連の処理を追加
            is_shuttle = bool(int(row.get('is_shuttle', 0))) if pd.notna(row.get('is_shuttle')) else False
            shuttle_start = None
            shuttle_end = None
            timetable_type = int(row.get('timetable_type', 1)) if pd.notna(row.get('timetable_type')) else 1
            
            if is_shuttle:
                if pd.notna(row.get('shuttle_start')) and row['shuttle_start']:
                    shuttle_start = datetime.strptime(row['shuttle_start'], '%H:%M:%S').time()
                if pd.notna(row.get('shuttle_end')) and row['shuttle_end']:
                    shuttle_end = datetime.strptime(row['shuttle_end'], '%H:%M:%S').time()
            
            timetable = Timetable(
                route=row['route'],
                direction=row['direction'],
                timetable_type=timetable_type,
                departure_time=datetime.strptime(row['departure_time'], '%H:%M:%S').time(),
                arrival_time=datetime.strptime(row['arrival_time'], '%H:%M:%S').time() if pd.notna(row['arrival_time']) else None,
                is_shuttle=is_shuttle,
                shuttle_start=shuttle_start,
                shuttle_end=shuttle_end,
                valid_from=datetime.strptime(row['valid_from'], '%Y-%m-%d').date(),
                valid_to=datetime.strptime(row['valid_to'], '%Y-%m-%d').date() if pd.notna(row['valid_to']) else None
            )
            db.session.add(timetable)
        
        db.session.commit()
        logger.info("時刻表のアップロードが完了しました")
        return jsonify({'message': '時刻表のアップロードが完了しました'}), 200
    
    except Exception as e:
        logger.error(f"アップロード中にエラーが発生: {str(e)}")
        db.session.rollback()
        return jsonify({'error': f'アップロード中にエラーが発生しました: {str(e)}'}), 500

@bp.route('/timetable/download', methods=['GET'])
def download_timetable():
    logger.info("時刻表ダウンロードリクエスト受信")
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
        
        logger.info("時刻表のダウンロードが完了しました")
        return jsonify({'message': '時刻表のダウンロードが完了しました', 'path': csv_path}), 200
    
    except Exception as e:
        logger.error(f"ダウンロード中にエラーが発生: {str(e)}")
        return jsonify({'error': f'ダウンロード中にエラーが発生しました: {str(e)}'}), 500

# ここにAPI用のルートを追加予定 