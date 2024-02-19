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

        
        if username == "None":
            line_bot_api.push_message(line_user_id, TextSendMessage("初めまして！（これは、名前が登録されていない時のメッセージ）"))
            line_bot_api.push_message(line_user_id, TextSendMessage("あなたが送ったメッセージは「"+line_message+"」です。これをあなたの名前として登録します"))
            username = line_message
        else:    
            line_bot_api.push_message(line_user_id, TextSendMessage("こんにちは、"+username+"さん。"))
            line_bot_api.push_message(line_user_id, TextSendMessage(line_message+"とはどういう意味でしょうか？"))
        mode = "活動開始"
        no = "いいえ"
        
        line_bot_api.push_message(line_user_id, TextSendMessage(f"https://docs.google.com/forms/d/e/1FAIpQLSfKyju5yd5Fw08TiEo6Bwe3IO3HTM1gjngvWASKtMR8FpKtuA/viewform?usp=pp_url&entry.998530319={tourl(groupname)}&entry.273281967=2024-02-09&entry.1630282032={tourl(username)}&entry.449921247={tourl(mode)}&entry.1302965683=15:10&entry.2092899857={tourl(place)}&entry.358162710={tourl(teacher)}&entry.841836120={tourl(no)}&entry.1958684523=17:30"))
        
    # LINE Webhook サーバーへ HTTP レスポンスを返す
    return 'ok'
