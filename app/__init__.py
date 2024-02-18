from os import environ
from dotenv import load_dotenv
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)
load_dotenv(".env", verbose=True)

if not (access_token := environ.get("LINE_CHANNEL_ACCESS_TOKEN")):
    raise Exception("access token is not set as an environment variable")

if not (channel_secret := environ.get("LINE_CHANNEL_SECRET")):
    raise Exception("channel secret is not set as an environment variable")

# Line Messaging APIのチャネルアクセストークンとチャネルシークレットを設定してください
line_bot_api = LineBotApi(access_token)
handler = WebhookHandler(channel_secret)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=message)
    )

if __name__ == "__main__":
    app.run()
