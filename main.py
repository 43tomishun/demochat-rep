
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os
import logging 
import re

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header valuae
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

a_value = 0 
b_value = 0

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    global a_value
    global b_value
    message_text = event.message.text
    if '@tip' in message_text:
        if 'from@a' in message_text:
            amount = re.sub(r"\D", "", message_text)
            amount = int(amount)
            a_value = a_value - amount
            b_value = b_value + amount
            reply_text = f"aの残高は{a_value}です。bの残高は{b_value}です。"

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply_text)
            )
        
        elif 'from@b' in message_text:
            amount = re.sub(r"\D", "", message_text)
            amount = int(amount)
            a_value = a_value + amount
            b_value = b_value - amount
            reply_text = f"aの残高は{a_value}です。bの残高は{b_value}です。"

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply_text)
            )

        else :
            reply_text = f"aの残高は{a_value}です。bの残高は{b_value}です。"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply_text)
            )
    else:
        pass

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
