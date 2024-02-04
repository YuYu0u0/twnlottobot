from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookHandler, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, TextMessage, ImageSendMessage

from crawl.twnlotto import lotto_radNo, show_lottoNum, win_lotto

# Create your views here.

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parse = WebhookParser(settings.LINE_CHANNEL_SECRET)

# 輪詢條件(全域變數)
lotto_mode = 0
mode2_status = False
txtnum = ''


@require_POST
@csrf_exempt
def callback(request):
    global lotto_mode
    global mode2_status
    global txtnum
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parse.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        for event in events:
            if isinstance(event, MessageEvent):
                message = event.message.text
                message_object = None
                # 判斷是否進入對獎模式,進入輪詢
                if (lotto_mode == 1) or (lotto_mode == 2):
                    if message == "0":  # 離開條件
                        lotto_mode = 0
                        mode2_status = False
                        message_text = "離開對獎模式"

                    elif lotto_mode == 1:  # 月份對獎模式
                        year = message.strip().split(' ')[0]
                        month = message.strip().split(' ')[1]
                        message_text = show_lottoNum(year, month)
                        message_text += "\n請輸入年(民國)月份(以空格隔開)(0:離開)"
                    elif lotto_mode == 2:
                        if mode2_status:  # 輸入對獎號碼以空格隔開
                            numbers = message.strip().split()
                            message_text = win_lotto(
                                numbers, lotto_radNo(txtnum), txtnum)
                            message_text += "\n請輸入號碼(以空格隔開)(0:離開)"

                        else:
                            txtnum = message.strip()  # 輸入要對獎的期數
                            message_text = "請輸入號碼(以空格隔開)(0:離開)"
                            mode2_status = True

                    message_object = TextMessage(text=message_text)
                # 設定其他回應及進入輪詢條件
                else:
                    if message == "1":
                        message_text = '月份查詢:'
                        message_text += '\n請輸入年(民國)月份(以空格隔開):'
                        message_object = TextMessage(text=message_text)
                        lotto_mode = 1

                    elif message == "2":

                        print(type(txtnum))
                        message_text = '期數號碼對獎模式:'
                        message_text += '\n請輸入查詢期數:'
                        message_object = TextMessage(text=message_text)
                        lotto_mode = 2
                    elif message == "你好":
                        message_text = '你好,請按1進入月份查詢模式,按2進入期別對獎模式'
                        message_object = TextMessage(text=message_text)
                        print(lotto_mode)
                    else:
                        message_object = TextSendMessage(
                            text="我不懂你的意思!請按1進入月份查詢模式,按2進入期別對獎模式")
                    # if event.message.text=='hello':
                line_bot_api.reply_message(
                    event.reply_token,
                    # TextSendMessage(text='hello world')
                    message_object,
                )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
