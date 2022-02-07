import requests, json, threading, time, random,datetime
import operator
from functools import reduce
from queue import Queue
import copy
gt = 131
game_numb = 0
game_one = 0
free = 0
game_spin = 0
free_plural = 0

def parse(response):  # 旋转后解析最小金额位置方法
    INDEX_LIST = [0, 1, 2, 3, 4]
    list_with12 = []
    gold_list = []
    points = response['et']['data']['points']

    for i in range(12):
        # print(points[i])
        if points[i] == 12:
            list_with12.append(i % 5)
    list_without12 = [x for x in INDEX_LIST if x not in list_with12]
    for i in list_without12:
        gold_list.append(response['et']['data']['rotaryBls'][i])
    # print("list_with12:%s,list_without12:%s,gold_list:%s" % (str(list_with12),str(list_without12),str(gold_list)))
    return list_with12,list_without12,gold_list

def one_spin(response,tk):  # 单次旋转方法
    one_spin_url = "http://192.168.10.25:9000/getSlotData"
    while True:
        global game_numb, game_one, free, roteKey
        game_numb += 1
        game_one += 1
        # print('跳出循环')
        gold = (response['et']['gold']) / 100
        Ngold = (response['et']['nGold']) / 100

        if response['code'] == 20000:
            list_with12,list_without12, gold_list = parse(response)
            # print(list_without12, list_without12, gold_list)
            for i in range(len(gold_list)):
                if gold_list[i] == min(gold_list):
                    print(list_without12[i] + 1)
                    millis = int(round(time.time() * 1000))
                    one_spin_data = {
                        "gt": gt,
                        "betScore": str(min(gold_list)),
                        "tk":tk,
                        "actionType": 1,
                        "data": {"roteKey": roteKey, "roteRow": list_without12[i] + 1}}
                        # "roteKey"
                    headers = {
                        'token': tk,
                        'Content-Type': 'application/json'
                        }
                    one_spin_data = json.dumps(one_spin_data)
                    try:
                        # print(one_spin_data)
                        print(f'单次旋转里面{tk}--投入{min(gold_list)/100}---{Ngold}---单轴局数{game_one}---总局数{game_numb}')
                        response = requests.post(url = one_spin_url, data = one_spin_data, headers=headers)
                        response = response.json()
                        # time.sleep(2)
                        # print(response)
                        roteKey = response['et']['data']['roteKey']
                        if response['code'] == 20000:
                            if response['et']['data']['isFree']:
                                free += 1
                                print(response)
                                print(f"进入红利---{tk}--第{free}次---局数{free*15}")
                                return

                    except:
                        print(response['code'])
                        break
        else:
            print(response['code'])
            exit(-6)

def all_spin(i, tk, betScore):
    INDEX_LIST = [0, 1, 2, 3, 4]
    global game_numb, game_spin, free_plural
    url = "http://192.168.10.25:9000/getSlotData"
    # print('开始正常摇')
    headers = {
        'token': tk,
        'Content-Type': 'application/json'
        }

    if i == 0:    # 摇一次非红利，就最小的开始单独旋转
        gold = 0
        while True:
            global game_numb, roteKey
            game_numb += 1
            millis = int(round(time.time() * 1000))
            data = {"gt": gt, "betScore": betScore, "tk": tk, "actionType": 0}
            data = json.dumps(data)
            try:
                response = requests.post(url = url,data = data, headers=headers)
                print('putong', response.text)
                response = response.json()
                roteKey = response['et']['data']['roteKey']
                points = response['et']['data']['points']
                if response['code'] == 20000:
                    game_spin += 1
                    if response['et']['data']['isFree'] == False and response['et']['type'] == 0:
                        gold = 0
                        one_spin(response, tk)
                    else:
                        if response['et']['type'] == 1:
                            print('free...')
                            if points.count(12) > 2:
                                free_plural += 1
                                print(f'红利复利{free_plural}次，当前总局数{game_numb}')
                        a = (response['et']['gold']) / 100
                        gold += a
                        print(f'中奖金额{a}---普通场总计赢取{gold}----普通旋转{game_spin}次---总局数{game_numb}')
                elif response['code'] == 20017:
                    break

            except Exception as e:
                print(repr(e))
                print("错误了")

    if i == 1:  # 摇中一个或者两个散步，就最小的开始单独旋转
        while True:
            millis = int(round(time.time() * 1000))
            data = {"gt": gt, "betScore": betScore, "tk": tk, "actionType": 0}
            data = json.dumps(data)
            try:
                response = requests.post(url = url,data = data, headers=headers)
                print(response.text)
                response = response.json()
                if response['code'] == 20000:
                    list_with12,list_without12,gold_list = parse(response)
                    if 1 <= len(list_with12) <= 2 and response['et']['type'] == 0:
                        one_spin(response, tk)
            except Exception as e:
                print(repr(e))
                print("错误了")
    if i == 2:   #必须摇中2个散步,开始选择最小的转轴单次旋转
        while True:
            millis = int(round(time.time() * 1000))
            data = {"gt": gt, "betScore": betScore, "tk": tk, "actionType": 0}
            data = json.dumps(data)
            try:
                response = requests.post(url = url,data = data, headers=headers)
                # print(response.text)
                response = response.json()
                if response['code'] == 20000:
                    list_with12,list_without12,gold_list = parse(response)
                    if len(list_with12) == 2 and response['et']['type'] == 0:
                        one_spin(response, tk)
            except:
                pass
    if i == 3:    #普通抽奖
        while True:
            millis = int(round(time.time() * 1000))
            data = {"gt": gt, "betScore": betScore, "tk": tk, "actionType": 0}
            data = json.dumps(data)
            try:
                response = requests.post(url=url, data=data)
                print(response.text)
            except:
                pass

def register():
    url = "http://192.168.10.82:8031/registerUser"
    headers = {
        'Content-Type': 'application/json'
        }
    registerResponse = requests.get(url, headers=headers)
    username = registerResponse.json().get("username")
    password = "123456"
    if username:
        print(username, password)
        return username, password
    return None

def call(tk, gametype):
    url = "http://192.168.10.25:9000/callInitialize"
    data = {
        "gt": gametype,
        "timestamp": 45646545654,
        'actionType': '0'
        }
    headers = {
        'token': tk,
        'Content-Type': 'application/json'
        }
    data = json.dumps(data)
    response = requests.post(url=url, data=data, headers=headers)
    response = response.json()
    print("初始化", response)

def PostToken(username, password):
    headers = {
        'Content-Type': 'application/json'
    }
    url = "http://192.168.10.25:9000/login?"
    # url = "http://192.168.10.212:8002/login?"
    tokenResponse = requests.post(url = url+f'username={username}&password={password}&style=5', headers = headers)
    token = tokenResponse.json()
    token = token['et']['uid']
    # print(token)
    if token:
        return token
    return None


def Play(number, betScore, tk):
    url = "http://192.168.10.25:9000/getSlotData"
    print("第%s个线程开始运行" % number)
    for b in range(10000):
        free_num = random.randint(1, 4)
        times = time.asctime()
        # print(times)
        '''liue351 - liue363(||362)'''
        data = {"gt": gt, "betScore":betScore,"tk":tk,"actionType":0}
        # data = {"gt": gt, "betScore":betScore,"tk":tk,"actionType":0,"freeType": free_num}
        headers = {
            'token': tk,
            'Content-Type': 'application/json'
            }
        try:
            post = requests.post(url, json=data, headers=headers)
            post = post.json()
            # print(data)
            print(post)
            code = post.get("code")

        except Exception as e:
            print(repr(e))
            print("错误了")


def oneplay(tk, roteRow,betScore,roteKey):
    url = "http://192.168.10.25:9000/getSlotData"
    data = {"gt":130,"betScore":betScore,"tk":tk ,"actionType":1,"data":{"roteKey":roteKey,"roteRow":roteRow}}
    headers = {
        'token': tk,
        'Content-Type': 'application/json'
        }
    respose = requests.post(url, json=data, headers=headers)
    respose = respose.json()
    print(respose)
    nGold = respose['et']['nGold']
    gold = respose['et']['data']['gold']
    roteKe = respose['et']['data']['roteKey']
    return gold, nGold, roteKe

def pay(username, gold):
    requests.get(f'http://192.168.10.212:8001/pay/{username}/{gold*100}')

def playromance():
    username, password = register()
    pay(username, 200000)
    tk = PostToken(username, password)
    print(tk)
    call(tk, gt)


if __name__ == '__main__':
    # all_spin(0, tk, 2500)
    sss = []
    for i in range(1):
        username, password = register()
        pay(username, 20000)
        tk = PostToken(username, password)
        print(tk)
        call(tk, gt)
        print(tk)
        time.sleep(1)
        t = threading.Thread(target=Play, args=(i, 3000, tk))
        sss.append(t)
        t.start()
    for l in sss:
        l.join()





    # for i in range(1):
    #     username, password = register()
    #     pay(username, 20000000)
    #     tk = PostToken(username, password)
    #     print(tk)
    #     # call(tk, gt)
    #     print(i)
    #     threading.Thread(target=Play, args=(i, 3000)).start()

    # li = []
    # for i in range(5):
    #     li.append(PostToken(f'lius{i}', 3000))
    # print(li)








    # a, b, c = oneplay('C57B2C372EFE204896A8BE14C2F3C105F0BC', 5, 28000, '658fcecad6864fd18465f9539b64c6af')
    # for i in range(10000000):
    #     print(f'当前次数{i}-----', oneplay('C57B2C372EFE204896A8BE14C2F3C105F0BC', 5, 28000, c))




