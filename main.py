# インポートするライブラリ
from flask import Flask, request, abort, psycopg2

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    FollowEvent, MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction
)
import os

# DBコネクション取得関数
def get_connection():
    dsn = "host=＜Host＞ port=5432 dbname=＜Database＞ user=＜User＞ password=＜Password＞"
    return psycopg2.connect(dsn)

# 返事取得関数（今は暫定で日付返す関数）
def get_response_message(mes_from):
    # "日付"が入力された時だけDBアクセス
    if mes_from=="日付":
        with get_connection() as conn:
            with conn.cursor(name="cs") as cur:
                try:
                    sqlStr = "SELECT TO_CHAR(CURRENT_DATE, 'yyyy/mm/dd');"
                    cur.execute(sqlStr)
                    (mes,) = cur.fetchone()
                    return mes
                except:
                    mes = "exception"
                    return mes

    # それ以外はオウム返し
    return mes_from

# 軽量なウェブアプリケーションフレームワーク:Flask
app = Flask(__name__)


#環境変数からLINE Access Tokenを設定
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
#環境変数からLINE Channel Secretを設定
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

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

    return 'OK'

# MessageEvent
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=get_response_message(event.message.text))
     )

if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
