import json
import requests
import threading
import time, random

gt = 141
game_numb = 0
game_one = 0
free = 0
game_spin = 0
free_plural = 0

# url = "http://192.168.10.212:8001/getSlotData"
# url = "http://192.168.10.25:9000/getSlotData"


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
    one_spin_url = "http://192.168.10.212:8001/getSlotData"
    while True:
        global game_numb, game_one, free, roteKey
        game_numb += 1
        game_one += 1
        # print('跳出循环')
        gold = (response['et']['gold']) / 100
        Ngold = (response['et']['nGold']) / 100

        if response['code'] == 20000:
            list_with12,list_without12, gold_list = parse(response)
            # print(list_with12,list_without12, gold_list)
            # print(list_without12, list_without12, gold_list)
            for i in range(len(gold_list)):
                if gold_list[i] == min(gold_list):
                    # print(list_without12[i] + 1)
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
    url = "http://192.168.10.212:8001/getSlotData"
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

def call(tk, gametype):
    url = "http://192.168.10.213:8002/callInitialize"
    data = {
        "gt": str(gametype),
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

def register():
    url = "http://192.168.10.25:9000/registerUser"
    headers = {
        'Content-Type': 'application/json'
        }
    registerResponse = requests.get(url, headers=headers)
    username = registerResponse.json().get('et').get("username")
    password = "123456"
    tk = registerResponse.json().get('newID')
    if username:
        print(username, password)
        return username, password
    return None

def PostToken(username, password):
    headers = {
        'Content-Type': 'application/json',
        }
    url = "http://192.168.10.213:8002/login?"

    tokenResponse = requests.post(url=url + f'username={username}&password={password}&style=5')
    token = tokenResponse.json()
    token = token['et']['uid']
    print(token)
    if token:
        return token
    return None

def pay(username, gold):
    if requests.get(f'http://192.168.10.213:8001/pay/{username}/{gold*100}').json()['code']==20000:
        return True
    else:
        return False


def Play(tk, gt, betScore, number):
    url = "http://192.168.10.213:8002/getSlotData"
    print("第%s个线程开始运行" % number)
    for b in range(10000):
        free_num = 3
        # data = {
        #     "gt": str(gt),
        #     "betScore": str(betScore),
        #     "actionType": "0",
        #     "timestamp": 1115556,
        #     'token': tk,
        #     'freeType': "0"
        #     }
        data = {"gt": gt, "betScore": betScore, "tk": tk, "actionType": 0}
        data1 = {"gt": gt, "betScore":betScore,"actionType":0, "freeType": free_num}
        headers = {
            'token': tk,
            'Content-Type': 'application/json'
            }
        try:
            post = requests.post(url, json=data, headers=headers)
            # time.sleep(0.05)
            log = post.text
            body = post.request.body
            header = post.request.body
            print(threading.current_thread(), str(b)+'次', log)
            # print(header,body)
            post = post.json()


            # points = post['et']['data']['points']
            # isFree = post['et']['data']['isFree']
            # code = post.get("code")
            # if code == 20000:
            #     if points.count(13) > 2 and isFree != False:
            #         print(f'进入红利{free_num}')
            #         post = requests.post(url, json=data1, headers=headers)
            #         print(post.json())
            #
            # else:
            #     print(header, body)

        except Exception as e:
            print(repr(e))
            print("错误了")

def common(tk,gt,betScore):
    data = {"gt": gt, "betScore": betScore, "tk": tk, "actionType": 0}
    headers = {
        'token': tk,
        'Content-Type': 'application/json'
        }
    response = requests.post(url, json=data, headers=headers).json()
    if response['code'] == 20000:
        return response
    else:
        print(response)
        exit(-2)


def if_free(response):
    if response['et']['data']['isFree'] == False and response['et']['type'] == 0:
        return True

def oneplaymax(response, ico):
    points = response['et']['data']['points']
    for i in range(5):
        if points[i] == ico or points[i+5] == ico or points[i+10] == ico:
            continue
        else:
            roteRow = i+1
            return roteRow
    return -1

def oneplay(tk, betScore, roteRow, gt):
    global roteKey
    data = {"gt":gt,"betScore":betScore,"tk":"null","actionType":1,
            "data":{"roteKey":roteKey,"roteRow":roteRow}}
    headers = {
        'token': tk,
        'Content-Type': 'application/json'
        }
    response = requests.post(url, json=data, headers=headers)
    response = response.json()
    print(data)
    roteKey = response['et']['data']['roteKey']
    if response['code'] == 20000:
        nGold = response['et']['nGold']/100
        gold = response['et']['data']['gold']/100
        return gold, nGold, response
    else:
        print(response)
        exit()

def oneplay_tow(tk,gt,betScore):

    roteRow = 5
    url = "http://192.168.10.212:8001/getSlotData"
    data = {"gt":gt,"betScore":betScore,"tk":"null","actionType":1,
            "data":{"roteKey":"71ed54b0-18ca-40cb-b970-10512998802e","roteRow":roteRow}}
    headers = {
        'token': tk,
        'Content-Type': 'application/json'
        }
    response = requests.post(url, json=data, headers=headers)
    response = response.json()
    Points = response['et']['data']['points']
    nGold = response['et']['nGold']/100
    gold = response['et']['data']['gold']/100
    return gold, nGold

def getToken(username,password):
    data = {
            "userName": username,
            "password": password
    }
    headers = {
        'Content-Type': 'application/json'
    }
    data = json.dumps(data)
    url = "http://192.168.10.212:8002/callToken"
    tokenResponse = requests.post(url = url, data = data, headers = headers)
    token = tokenResponse.json().get("ms")
    print(token)
    if token:
        return token
    return None

def main():
    # global nGold, gold
    global roteKey
    x = 0
    i = 0
    ico = 12
    gt = 132
    betScore = 2500
    username, password = register()
    pay(username, 10000)
    print(username)
    tk = PostToken(username, password)
    call(tk, gt)
    response = common(tk, gt, 2500)
    roteKey = response['et']['data']['roteKey']
    while True:
        x+=1
        if if_free(response):
            roteRow = oneplaymax(response, ico)
            if roteRow != -1:
                gold, nGold, response = oneplay(tk, betScore, roteRow, gt)
                print(f'单轴中---{gold, nGold}---总局数{x}')

            else:
                i += 1
                rotaryBls = response['et']['data']['rotaryBls']
                roteRow = 3
                # roteRow = rotaryBls.index(max(rotaryBls))+1
                # print(roteRow)
                print(f'当前次数{i}-----', oneplay(tk, betScore, roteRow, gt))

        else:
            print(f'进入红利了---总局数{x}', response)
            response = common(tk, gt, 2500)


if __name__ == '__main__':

    lis = [141]
    for x in lis:
        print(x)
        gt = x
        betScore = 3000
        times = time.asctime()
        sss = []
        for i in range(30):
            username, password = register()
            tk = PostToken(username, password)
            for j in lis:
                call(tk, j)
            time.sleep(2)
            t = threading.Thread(target=Play, args=(tk, gt, betScore, i))
            sss.append(t)
            t.start()
        for l in sss:
            l.join()

    # for i in range(10000000):
    #     print(f'当前次数{i}-----', oneplay('8A27BA5C827A8BCC8159BE605E063930F6B0', 28000))
    #     print(f'当前次数{i}-----', oneplay_tow('3284A8F739CE601F2DCAF699A58D56E00B95', 47400))



