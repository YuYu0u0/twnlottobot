import requests
import json


def lotto_radYM(year, mon):
    try:
        if year<2000:
            year+=1911
        if mon<10:
            month = str(year)+"-0"+str(mon)
        else:      
            month = str(year)+"-"+str(mon)
        url = f"https://api.taiwanlottery.com/TLCAPIWeB/Lottery/Lotto649Result?period&month={month}&pageNum=1&pageSize=10"

        my_headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
        r = requests.get(url, headers=my_headers)
        if r.status_code == 200:
            datas = json.loads(r.text)
            dataList = datas["content"]["lotto649Res"]
            lotto_number = {}

            for data in dataList:
                period = data["period"]
                date = data["lotteryDate"].split("T")[0]
                nums = data['drawNumberSize']

                lotto_number[date] = [period]+nums
            return lotto_number
    except Exception as e:
        print(e)


def lotto_radNo(txtnum):
    try:
        url = f"https://api.taiwanlottery.com/TLCAPIWeB/Lottery/Lotto649Result?period={txtnum}&month&pageNum=1&pageSize=10"
        my_headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
        r = requests.get(url, headers=my_headers)
        if r.status_code == 200:
            datas = json.loads(r.text)
            datalist = datas["content"]["lotto649Res"]
            lotto_number = {}
            for data in datalist:
                period = data["period"]
                nums = data['drawNumberSize']
                lotto_number[str(period)] = nums

            return lotto_number
    except Exception as e:
        print(e)


# 將爬蟲下來的資訊從字典整理成統一格式的字串回傳
def show_lottoNum(year, month):
    try:
        results = ''
        datas = lotto_radYM(year, month)
        print(datas)
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
        if int(num) in lotto_number[txtnum]:
            count += 1

    if count == 6:
        if sNum in numbers:
            result = "恭喜中二獎"
        else:
            result = "恭喜中頭獎"
    elif count == 5:
        if sNum in numbers:
            result = "恭喜中四獎"
        else:
            result = "恭喜中三獎"
    elif count == 4:
        if sNum in numbers:
            result = "恭喜中六獎1000元"
        else:
            result = "恭喜中五獎2000元"
    elif count == 3:
        if sNum in numbers:
            result = "恭喜中七獎400元"
        else:
            result = "恭喜中普獎400元"
    else:
        result = "沒中獎,再接再厲!!"

    return result


# 測試
if __name__ == "__main__":
    # print(lotto_radYM(107,12))
    # show_lottoNum(107,2)
    numbers = ['13', '21', '07', '47', '44', '08']
    txtnum = '112000101'
    # print(lotto_radNo(txtnum))
    print(win_lotto(numbers, lotto_radNo(txtnum), txtnum))
