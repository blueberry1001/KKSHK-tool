from fastapi import FastAPI, Request
from linebot import WebhookParser, LineBotApi
from linebot.models import TextSendMessage
import os

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
line_parser = WebhookParser(LINE_CHANNEL_SECRET)
app = FastAPI()

username = "default-username"
groupname = "default-groupname"
nowtime = 0
place = "School"
teacher = "default-teacher"

import urllib.parse
def tourl(x):
    return urllib.parse.quote(x)

@app.post('/')
async def kkshk(request: Request):
    global username,groupname,nowtime,place,teacher
    # X-Line-Signature ヘッダーの値を取得
    signature = request.headers.get('X-Line-Signature', '')

    # request body から event オブジェクトを取得
    events = line_parser.parse((await request.body()).decode('utf-8'), signature)

    # 各イベントの処理（※1つの Webhook に複数の Webhook イベントオブジェクトが含まれる場合あるため）
    for event in events:
        if event.type != 'message':
            continue
        if event.message.type != 'text':
            continue

        # LINE パラメータの取得
        line_user_id = event.source.user_id
        line_message = event.message.text


        #初回登録判定、どうしようか
        if username != "default-username" or True:
            line_bot_api.push_message(line_user_id, TextSendMessage("初めまして！あなたが送ったメッセージをもとに、空白区切りで情報を登録します。"))
            x = line_message.split()
            if len(list(line_message().split()))<4:
                line_bot_api.push_message(line_user_id, TextSendMessage("送られたメッセージが空白区切りで4個以下であるため、登録を行うことができませんでした。"))
            else:
                username = x[0]
                groupname = x[1]
                place = x[2]
                teacher = x[3]
                line_bot_api.push_message(line_user_id, TextSendMessage(f"username:{username},groupname:{groupname},place:{place},teacher:{teacher}として登録したよ"))
        line_bot_api.push_message(line_user_id, TextSendMessage("こんにちは、"+username+"さん。"))
        line_bot_api.push_message(line_user_id, TextSendMessage("URLを発行します。"))
        mode = "活動開始"
        no = "いいえ"
        
        line_bot_api.push_message(line_user_id, TextSendMessage(f"https://docs.google.com/forms/d/e/1FAIpQLSfKyju5yd5Fw08TiEo6Bwe3IO3HTM1gjngvWASKtMR8FpKtuA/viewform?usp=pp_url&entry.998530319={tourl(groupname)}&entry.273281967=2024-02-09&entry.1630282032={tourl(username)}&entry.449921247={tourl(mode)}&entry.1302965683=15:10&entry.2092899857={tourl(place)}&entry.358162710={tourl(teacher)}&entry.841836120={tourl(no)}&entry.1958684523=17:30"))
        
    # LINE Webhook サーバーへ HTTP レスポンスを返す
    return 'ok'
