from fastapi import FastAPI, Request
from linebot import WebhookParser, LineBotApi
from linebot.models import TextSendMessage
import datetime
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
prog = 0
dic = {"バドミントン部":"バトミントン部","陸部":"陸上部","陸上競技部":"陸上部","バトミントン":"バトミントン部","男子排球部":"男子バレーボール部","クイ研":"附属クイズ研究部","男子庭球部":"男子テニス部","男バス":"男子バスケットボール部","クイズ研究会":"附属クイズ研究部","男バレ":"男子バレーボール部","かるた":"かるた部","ジャズ研":"JAZZ研究会","jazz研":"JAZZ研究会","jazz研究会":"JAZZ研究会"}
import urllib.parse
def tourl(x):
    return urllib.parse.quote(x)

@app.post('/')
async def kkshk(request: Request):
    global username,groupname,nowtime,place,teacher,prog
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
        def send(val):
            line_bot_api.push_message(line_user_id, TextSendMessage(val))
        if prog == 0:
            #名前の登録をする
            username = line_message
            send("次に、部活名を入力してください。")
            prog += 1
        elif prog == 1:
            #部活名
            if line_message in dic:
                groupname = dic[line_message]
            else:
                groupname = line_message
            send(groupname+"として登録しました。次に、場所を入力してください。")
            
            prog += 1
        elif prog == 2:
            #場所
            send("最後に、担当教員の名前を入力してください")
            place = line_message
            prog += 1
        elif prog == 3:
            #先生
            teacher = line_message
            send("登録が完了しました。登録をやり直したい場合は、「0」を入力してください。0以外のメッセージを送信すると、自動入力されたリンクを送ります")
            prog += 1
        else:
            if line_message == "0":
                send("再度登録を行います。名前を入力してください。")
                prog = 0
            else:
                send("こんにちは、"+username+"さん。URLを発行します。なお、登録をやり直したい場合は「0」を入力してください。")
                mode = "活動開始"
                no = "いいえ"
                d = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
                line_bot_api.push_message(line_user_id, TextSendMessage(f"https://docs.google.com/forms/d/e/1FAIpQLSfKyju5yd5Fw08TiEo6Bwe3IO3HTM1gjngvWASKtMR8FpKtuA/viewform?usp=pp_url&entry.998530319={tourl(groupname)}&entry.273281967={tourl(d.strftime('%Y-%m-%d'))}&entry.1630282032={tourl(username)}&entry.449921247={tourl(mode)}&entry.1302965683={tourl(d.strftime('%H:%M'))}&entry.2092899857={tourl(place)}&entry.358162710={tourl(teacher)}&entry.841836120={tourl(no)}&entry.1958684523={tourl(d.strftime('%H:%M'))}"))
        
    # LINE Webhook サーバーへ HTTP レスポンスを返す
    return 'ok'
