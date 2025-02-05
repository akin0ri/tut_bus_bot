import os
from os import environ
from dotenv import load_dotenv
from flask import Flask, request, abort

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from app.bus_status import get_bus_status
from app.bus_time import get_last_5_bus_times
from app.food_status import get_food_status

app = Flask(__name__)

load_dotenv(".env", verbose=True)

# set LINE channel secret and access token
if not (access_token := environ.get("LINE_CHANNEL_ACCESS_TOKEN")):
    raise Exception("access token is not set as an environment variable")
if not (channel_secret := environ.get("LINE_CHANNEL_SECRET")):
    raise Exception("channel secret is not set as an environment variable")

configuration = Configuration(access_token=access_token)
handler = WebhookHandler(channel_secret)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    except Exception as e:
        print(e)
        abort(500)
    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        
        try:
                
            if event.message.text == "運行予定":
                reply_text = get_bus_status(7)
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=reply_text)]
                    )
                )
            
            elif event.message.text == "問い合わせ":
                reply_text = get_food_status()
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text="お問い合わせはこちらから \n https://forms.gle/Q3vcxdm2mXz2fBTK8")]
                    )
                )
            
            else:
                bustype, direction = event.message.text.split("_")
                timetable = get_last_5_bus_times(bustype, int(direction)+1)
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=timetable)]
                    )
                )
        except Exception as e:
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="エラーが発生しました")]
                )
            )

if __name__ == "__main__":
    app.run(port=3131, debug=True)
