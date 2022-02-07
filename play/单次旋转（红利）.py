import json
import requests
import time
import threading

game_numb = 0


def parse(response):  # 旋转后解析最小金额位置方法
    INDEX_LIST = [0, 1, 2, 3, 4]
    list_with12 = []
    gold_list = []
    points = response['et']['Data']['Points']

    for i in range(12):
        # print(points[i])
        if points[i] == 12:
            list_with12.append(i % 5)
    list_without12 = [x for x in INDEX_LIST if x not in list_with12]
    for i in list_without12:
        gold_list.append(response['et']['Data']['RotaryBls'][i])
    # print("list_with12:%s,list_without12:%s,gold_list:%s" % (str(list_with12),str(list_without12),str(gold_list)))
    return list_with12,list_without12,gold_list


def one_spin(response,tk):  # 单次旋转方法
    one_spin_url = "http://192.168.10.25:8001/api/usercore/CallLotteryRoteRow"
    while True:
        global game_numb
        game_numb += 1
        # print('跳出循环')
        gold = (response['et']['Gold']) / 100
        Ngold = (response['et']['NGold']) / 100

        if response['code'] == 20000:
            list_with12,list_without12,gold_list = parse(response)
            for i in range(len(gold_list)):
                if gold_list[i] == min(gold_list):
                    millis = int(round(time.time() * 1000))
                    one_spin_data = {
                        "tk": tk,
                        "gt": 133,
                        "betScore": str(min(gold_list)),
                        "timestamp": str(millis),
                        "RoteKey": "ddd",
                        "RoteRow": list_without12[i] + 1
                    }
                    one_spin_data = json.dumps(one_spin_data)
                    try:
                        print(f'单次旋转里面{tk}--投入{min(gold_list)/100}---{Ngold}')
                        response = requests.post(url = one_spin_url,data = one_spin_data)
                        # print('dandu', response.text)
                        # print("betScore:%s,RoteRow:%d,response:%s" % (str(min(gold_list)),list_without12[i] + 1,response.text))
                        response = response.json()
                        if response['code'] == 20000:
                            if response['et']['Data']['isFree']:
                                print(f"进入红利了---{tk}")
                                return

                    except:
                        pass


def all_spin(i,tk):
    INDEX_LIST = [0, 1, 2, 3, 4]
    url = "http://192.168.10.25:8001/api/UserCore/CallLotteryModel"
    # print('开始正常摇')
    if i == 0:    # 摇一次非红利，就最小的开始单独旋转
        gold = 0
        while True:
            global game_numb
            game_numb += 1
            millis = int(round(time.time() * 1000))
            data = {
                "tk": tk,
                "gt": 133,
                "betScore": "2500",
                "timestamp": str(millis)
            }
            data = json.dumps(data)
            try:
                response = requests.post(url = url,data = data)
                # print('putong', response.text)
                response = response.json()
                if response['et']['Data']['isFree'] == False and response['et']['Type'] == 0:
                    gold = 0
                    one_spin(response, tk)
                else:

                    a = (response['et']['Gold']) / 100
                    gold += a
                    print(f'中奖金额{a}---总计赢取{gold}')
            except:
                pass

    if i == 1:  # 摇中一个或者两个散步，就最小的开始单独旋转
        while True:
            millis = int(round(time.time() * 1000))
            data = {
                "tk": tk,
                "gt": 133,
                "betScore": "2500",
                "timestamp": str(millis)
            }
            data = json.dumps(data)
            try:
                response = requests.post(url = url,data = data)
                print(response.text)
                response = response.json()
                if response['code'] == 20000:
                    list_with12,list_without12,gold_list = parse(response)
                    if 1 <= len(list_with12) <= 2 and response['et']['Type'] == 0:
                        one_spin(response, tk)
            except:
                pass
    if i == 2:   #必须摇中2个散步,开始选择最小的转轴单次旋转
        while True:
            millis = int(round(time.time() * 1000))
            data = {
                "tk": tk,
                "gt": 133,
                "betScore": "2500",
                "timestamp": str(millis)
            }
            data = json.dumps(data)
            try:
                response = requests.post(url = url,data = data)
                # print(response.text)
                response = response.json()
                if response['code'] == 20000:
                    list_with12,list_without12,gold_list = parse(response)
                    if len(list_with12) == 2 and response['et']['Type'] == 0:
                        one_spin(response, tk)
            except:
                pass
    if i == 3:    #普通抽奖
        while True:
            millis = int(round(time.time() * 1000))
            data = {
                "tk": tk,
                "gt": 133,
                "betScore": "2500",
                "timestamp": str(millis)
            }
            data = json.dumps(data)
            try:
                response = requests.post(url=url, data=data)
                print(response.text)
            except:
                pass


if __name__ == '__main__':
    tk_list = ['DFD8FC398A7C4EDDED37C7103013A2A4AA34','5A2D1F8F5BAAA5436C8C0BD1B1D7340CBE9C','A0FDAD73BE9CC6AB65FF825926D3EE5D345D',"6E544A618F6C18844DB81C88D5E0501595F0"]
    a = threading.Thread(target=all_spin, args=(0, tk_list[0])) # liu1006
    # print('kaishi')
    b = threading.Thread(target=all_spin, args=(2, tk_list[1])) # liu1007
    # all_spin(0, tk_list[0])
    a.start()
    print('aa')
    b.start()




