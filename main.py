# インポートするライブラリ
from flask import Flask, request, abort
import psycopg2

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

# 軽量なウェブアプリケーションフレームワーク:Flask
app = Flask(__name__)


#環境変数からLINE Access Tokenを設定
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
#環境変数からLINE Channel Secretを設定
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


# DBコネクション取得関数
def get_connection():
    host="ec2-107-21-255-181.compute-1.amazonaws.com"
    port=5432
    dbname="dduecrd1p23pgq"
    user="grcmdjajgfsjex"
    password="e9ace79c30017efd493887b9d8d9ed1ac0e3bc0eeca060cfed0271b99be2c9d7"
    conText = "host={} port={} dbname={} user={} password={}"
    conText = conText.format(host,port,dbname,user,password)
    return psycopg2.connect(conText)


# 返事取得関数（今は暫定で日付返す関数）
def get_response_message(mes_from):

    # "日付"が入力された時だけDBアクセス
    if mes_from=="日付":
        with get_connection() as conn:
            with conn.cursor() as cur:
                sql1 = "SELECT TO_CHAR(CURRENT_DATE, 'yyyy/mm/dd');"
                cur.execute(sql1)
                (mes,) = cur.fetchone()
                return mes

    # それ以外はオウム返し
    with get_connection() as conn:
            with conn.cursor() as cur:
                sql2 = "insert into test(name,nedan) values('リンゴ',100);"
                cur.execute(sql2)
                conn.commit()
                return mes_from


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
