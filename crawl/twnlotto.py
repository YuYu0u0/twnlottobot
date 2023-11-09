import requests
import re
from bs4 import BeautifulSoup


def lotto_radYM(year, month):
    try:
        my_headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
        # 第一次get將隨機生成的參數值取下
        r = requests.get(
            "https://www.taiwanlottery.com.tw/lotto/Lotto649/history.aspx", headers=my_headers)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')

            __VIEWSTATE = soup.find('input', id="__VIEWSTATE").get("value")
            __VIEWSTATEGENERATOR = soup.find(
                'input', id="__VIEWSTATEGENERATOR").get("value")
            __EVENTVALIDATION = soup.find(
                'input', id="__EVENTVALIDATION").get("value")

            payLoad = {
                "__EVENTTARGET": "",
                "__EVENTARGUMENT": "",
                "__LASTFOCUS": "",
                "__VIEWSTATE": __VIEWSTATE,
                "__VIEWSTATEGENERATOR": __VIEWSTATEGENERATOR,
                "__EVENTVALIDATION": __EVENTVALIDATION,
                "forma": "請選擇遊戲",
                "Lotto649Control_history$chk": "radYM",
                "Lotto649Control_history$dropYear": year,
                "Lotto649Control_history$dropMonth": month,
                "Lotto649Control_history$btnSubmit": "查詢",
            }
            # 將get的參數值跟年月份寫進payload並post請求資料
            r = requests.post(
                'https://www.taiwanlottery.com.tw/lotto/Lotto649/history.aspx', headers=my_headers, data=payLoad)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                result = ''
                no = soup.find_all("span", id=re.compile(
                    "Lotto649Control_history_dlQuery_L649_DrawTerm_\d"))
                date = soup.find_all("span", id=re.compile(
                    "Lotto649Control_history_dlQuery_L649_DDate_\d"))
                num = soup.find_all("span", id=re.compile(
                    "Lotto649Control_history_dlQuery_SNo\d_\d"))
                sNum = soup.find_all("span", id=re.compile(
                    "SuperLotto638Control_history1_dlQuery_SNo7_\d"))
                # 將開獎號碼,日期,期別整理成字典
                lotto_number = {}
                for i in range(len(no)):
                    lotto_num = []
                    for j in range(6):
                        lotto_num.append(num[i*6+j].text)

                    lotto_number[date[i].text] = [
                        no[i].text]+lotto_num+[sNum[i].text]

            return lotto_number
    except Exception as e:
        print(e)


def lotto_radNo(txtnum):
    try:
        my_headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
        # 第一次get將隨機生成的參數值取下
        r = requests.get(
            "https://www.taiwanlottery.com.tw/lotto/Lotto649/history.aspx", headers=my_headers)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')

            __VIEWSTATE = soup.find('input', id="__VIEWSTATE").get("value")
            __VIEWSTATEGENERATOR = soup.find(
                'input', id="__VIEWSTATEGENERATOR").get("value")
            __EVENTVALIDATION = soup.find(
                'input', id="__EVENTVALIDATION").get("value")

            payLoad = {
                "__EVENTTARGET": "",
                "__EVENTARGUMENT": "",
                "__LASTFOCUS": "",
                "__VIEWSTATE": __VIEWSTATE,
                "__VIEWSTATEGENERATOR": __VIEWSTATEGENERATOR,
                "__EVENTVALIDATION": __EVENTVALIDATION,
                "forma": "請選擇遊戲",
                "Lotto649Control_history$chk": "radNO",
                "Lotto649Control_history$txtNO": txtnum,
                "Lotto649Control_history$btnSubmit": "查詢",
            }
            # 將get的參數值跟查詢期別寫進payload並post請求資料
            r = requests.post(
                'https://www.taiwanlottery.com.tw/lotto/Lotto649/history.aspx', headers=my_headers, data=payLoad)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                result = ''
                no = soup.find_all("span", id=re.compile(
                    "Lotto649Control_history_dlQuery_L649_DrawTerm_\d"))
                date = soup.find_all("span", id=re.compile(
                    "Lotto649Control_history_dlQuery_L649_DDate_\d"))
                num = soup.find_all("span", id=re.compile(
                    "Lotto649Control_history_dlQuery_SNo\d_\d"))
                sNum = soup.find_all("span", id=re.compile(
                    "SuperLotto638Control_history1_dlQuery_SNo7_\d"))
                # 將開獎號碼,日期,期別整理成字典
                lotto_number = {}
                for i in range(len(no)):
                    lotto_num = []
                    for j in range(6):
                        lotto_num.append(num[i*6+j].text)

                    lotto_number[no[i].text] = [
                        date[i].text]+lotto_num+[sNum[i].text]

            return lotto_number
    except Exception as e:
        print(e)


# 將爬蟲下來的資訊從字典整理成統一格式的字串回傳
def show_lottoNum(year, month):
    try:
        results = ''
        datas = lotto_radYM(year, month)
        if len(datas) == 0:
            print('輸入錯誤')
            return '輸入錯誤'
        for data in datas:
            result = data+" "+datas[data][0]+"期\t"
            for i in datas[data][1:7]:
                result += i+" "
            result += "特別號:"+datas[data][-1]
            results += "\n"+result
        return results.strip()
    except Exception as e:
        print(e)


# 以期別整理下來的資訊和輸入的號碼做對比以進行對獎
def win_lotto(numbers, lotto_number, txtnum):
    count = 0
    if len(numbers) != 6:
        result = '請輸入6個號碼'
        return result
    sNum = lotto_number[txtnum][-1]

    for num in numbers:
        if num in lotto_number[txtnum]:
            count += 1

        if count == 6:
            if sNum in num:
                result = "恭喜中二獎"
            else:
                result = "恭喜中頭獎"
        elif count == 5:
            if sNum in num:
                result = "恭喜中四獎"
            else:
                result = "恭喜中三獎"
        elif count == 4:
            if sNum in num:
                result = "恭喜中六獎1000元"
            else:
                result = "恭喜中五獎2000元"
        elif count == 3:
            if sNum in num:
                result = "恭喜中七獎400元"
            else:
                result = "恭喜中普獎400元"
        else:
            result = "沒中獎,再接再厲!!"

    return result


# 測試
if __name__ == "__main__":
    show_lottoNum(107, 12)
    numbers = ['21', '07', '47', '44', '08', '13']
    txtnum = '112000101'
    print(lotto_radNo(txtnum))
    print(win_lotto(numbers, lotto_radNo(txtnum), txtnum))
