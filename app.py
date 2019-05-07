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

app = Flask(__name__)

line_bot_api = LineBotApi('49B3Uyg8fH9+K7UDdwNnu6XKEbQCWbYG0Z1+VI9Ozz8X1IQsOjnQfBtbwQ622XidUyvrIV35b0OrhdvVVxlqQY5doyJOXwQvbLBKpsuhOhrS+VvetlVNgL9kHULU23uFS8ddLVamEbPbyX46vmXi9wdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('28610dfddc4c40de63105a743d75c7c8')



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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()