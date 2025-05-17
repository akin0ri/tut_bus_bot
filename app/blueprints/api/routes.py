from flask import request, abort, current_app
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, TextMessageContent
import os

from app.bus_status import get_bus_status
from app.bus_time import get_last_5_bus_times
from app.food_status import get_food_status
from . import api_bp

configuration = Configuration(access_token=os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("LINE_CHANNEL_SECRET"))

@api_bp.route("/line/webhook", methods=['POST'])
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

# ここにAPI用のルートを追加予定 