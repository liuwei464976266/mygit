# encoding:utf-8
import requests, json, threading, time, random, datetime, string, re

MAXPAYGOLD = 970000
SCATTER = '11'
session = requests.session()
BET = 3000
pattern = 2
LOGINUIR = "http://192.168.10.213:9002/user/register"
INITURL = 'http://192.168.10.213:9008/callInitialize'
SLOTURL = 'http://192.168.10.213:9008/getSlotData'
REGISTERURL = 'http://192.168.10.213:9000/registerUser'
exchange = 'http://192.168.10.213:9002/api/Service/ExchangeInOrOut'


def addGold(tk, money):
    url = 'http://192.168.10.213:9002/api/UserCore/AddPlayerGold'

    headers = {
        'Content-Type': 'application/json',
        'Host': '192.168.10.213:9002',
        'Origin': 'http://192.168.10.213:9002'
        }

    data = {"tk": tk, "type": 1, "money": money * 100, "timestamp": "1638779262282"}
    response = requests.post(url, headers=headers, json=data)
    print('加钱', response.text)


def normalPlay(tokenid, gametype, betScore, Type=0):  # 正常玩模式
    url = SLOTURL
    millis = str(int(round(time.time() * 1000)))
    headers = {
        'token': tokenid,
        'Content-Type': 'application/json'
        }
    data = {
        "gt": str(gametype),
        "betScore": str(betScore),
        "actionType": '0',
        "timestamp": millis,
        'role': pattern,
        'betType': Type
        }
    data = json.dumps(data)
    try:
        respon = session.post(url, data=data, headers=headers)
        response = respon.json()
        # print(response)
        if response.get("code") == 20000:
            return response
        elif response.get("code") == 20001:
            print(response)
            exit(-2)
        else:
            with open('error.txt', 'a')as f:
                f.write('\n' + response)
            print("error", response)
    except:
        pass
    return None


def call(tk, gametype):
    url = INITURL
    data = {
        "gt": gametype,
        "timestamp": 45646545654,
        'actionType': '0',
        'tk': tk

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
    url = REGISTERURL
    headers = {
        'Content-Type': 'application/json'
        }
    registerResponse = requests.get(url, headers=headers)
    print(registerResponse.json())
    tokenId = registerResponse.json()['et'].get("uid")
    username = registerResponse.json()['et'].get("username")
    if tokenId:
        print(tokenId, username)
        return tokenId, username
    return None


def getToken(username, password):
    data = {
        "userName": username,
        "password": password
        }
    headers = {
        'Content-Type': 'application/json'
        }
    data = json.dumps(data)
    url = "http://192.168.10.212:8002/callToken"
    tokenResponse = requests.post(url=url, data=data, headers=headers)
    token = tokenResponse.json().get("ms")
    print(token)
    if token:
        return token
    return None


def java_login(username, password, style=5):
    while True:
        url = f"http://192.168.10.212:8001/login?username={username}&password={password}&style={style}"
        headers = {
            'Content-Type': 'application/json;charset=UTF-8'
            }
        loginResponse = session.post(url, headers)
        loginResponse = loginResponse.json()
        print("登录", loginResponse)
        if loginResponse['code'] == 20000:
            url = 'http://192.168.10.212:8001/selectGame'
            token = loginResponse['et']['uid']
            headers = {
                'token': token,
                'Content-Type': 'application/json;charset=UTF-8'
                }
            selectResponse = session.post(url=url, headers=headers)
            url = 'http://192.168.10.212:8001/getUserInfo'
            headers = {
                'token': token,
                }
            infoResponse = session.get(url=url, headers=headers)
            infoResponse = infoResponse.json()
            print("获取用户信息", infoResponse)
            return token


def login(Url):
    currency = random.randint(1, 2)
    headers = {
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '65',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': '192.168.10.213:9002',
        'Origin': 'http://192.168.10.213:9002',
        'Referer': 'http://192.168.10.213:9002/index.html?l=zh_CN&type=0',
        'Upgrade-Insecure-Requests': '1',

        }
    # userName = ''.join(random.sample(string.ascii_letters + string.digits, 5))
    userName = 'liuw' + (''.join(random.sample(string.digits, 3))) + (''.join(random.sample(string.ascii_letters, 3)))
    payload = dict(userName=userName, password='111111', currency=currency, style='7', nickName='', sex=0)
    # payload = 'userName=li11&password=111111&currency=1&style=1&nickName=&sex=0'
    response = requests.post(Url, headers=headers, data=payload, allow_redirects=False)
    location = response.headers['location']
    # print(location)
    if len(location) > 70:
        uid_list = re.findall(r'uid=(.*)&changeurl', location)
        uid = uid_list[0]
        print(userName)
    else:
        print('账号失败', userName)
        return login(LOGINUIR)
    return uid, location


def Exchange(tk, gt, type, location):
    headers = {
        'Content-Type': 'application/json',
        'Host': '192.168.10.213:9002',
        'Origin': 'http://192.168.10.213:9002',
        'Proxy-Connection': 'keep-alive',
        'Referer': str(location),
        }
    data = {"tk": tk, "gameType": gt, "actionType": type}
    response = requests.post(exchange, headers=headers, json=data)
    response = json.loads(response.text)
    gold = response['et']['gold']
    money = response['et']['money']
    return gold, money


def main(gt):  # 主函数 程序入口
    gameType = gt
    tokenid, location = login(LOGINUIR)
    betScore = BET
    call(tokenid, gameType)
    requests.get(f'http://192.168.10.212:8080/user/pay?uid={tokenid}&gold=100000000000')
    # addGold(tokenid, 10000000)
    for i in range(15000):
        # thread.acquire()
        response = normalPlay(tokenid=tokenid, gametype=gameType, betScore=betScore)
        # thread.release()
        try:
            if response:
                if response['et']['type'] == 0 and response['et']['data']['isFree'] == False:  # 纯普通场
                    print(gt, f'次数={i}', threading.current_thread(), response)
                else:
                    print('进红利')
                    for m in range(50):
                        try:
                            response = normalPlay(tokenid=tokenid, gametype=gameType, betScore=betScore, Type=1)
                            print(response)
                            if response['et']['data']['residue'] == 0:
                                print('wan......')
                                break
                        except:
                            print(1)
        except:
            print(2)


thread = threading.Lock()

if __name__ == '__main__':
    a = []
    game = [130, 131, 132, 133, 134, 135, 136]
    # game = [134]
    for t in game:
        for i in range(6):
            c = threading.Thread(target=main, args=(t,))
            a.append(c)
            c.start()
        for x in a:
            x.join()
            print('结束', x)
