import requests, random, string, re, webbrowser, time, json
import logAnalysisUtil


def login(Url, num):
    currency = random.randint(1, 2)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': LOGINUIR[7:],
        'Origin': 'http://192.168.10.213:9002',
        'Referer': 'http://192.168.10.213:9002',
        }
    userName = 'DOOOOXDD'
    userName = 'liu' + (''.join(random.sample(string.digits, 3))) + (''.join(random.sample(string.ascii_letters, 3)))
    payload = dict(userName=userName, password='111111', currency=1, style=style, nickName='', sex=0)
    response = requests.post(Url + "/user/register", headers=headers, data=payload, allow_redirects=False)
    location = response.headers['location']
    location1 = location.replace(f'h/0', f'h/{num}')
    if len(location) > 70:
        uid_list = re.findall(r'uid=(.*)&changeurl', location)
        uid = uid_list[0]
        print(uid)
        print(userName)
    else:
        print('账号失败', userName, location1)
        return login(LOGINUIR, Type)
    return uid, location1, userName


def addGold(tk, money):
    url = 'http://192.168.10.213:9002/api/UserCore/AddPlayerGold'

    headers = {'Accept': '*/*',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Connection': 'keep-alive',
               'Content-Length': '94',
               'Content-Type': 'application/json',
               'Cookie': 'JSESSIONID=743BC1FF039FDA3E54A9ECB3FB44D617',
               'Host': "192.168.10.213:9002",
               'Origin': 'http://192.168.10.213:9002',
               'Referer': 'http://192.168.10.213:9002/LoadClient/h/0/bin-release/index.html?uid=5729B379523808E3B40AE60B3DE3C0B7E1D0&changeurl=1AA31C7B0F4D09D9739F39A3B95558C3&gameType=0&noLobby=0&homePage=0&language=0',
               }

    data = {"tk": tk, "type": 1, "money": money * 100, "timestamp": "1638779262282"}
    response = requests.post(url, headers=headers, json=data)
    print(response.text)


def login1():
    id = 241
    userName = 'liu' + (''.join(random.sample(string.digits, 3))) + (''.join(random.sample(string.ascii_letters, 3)))
    url = f"http://192.168.10.213:9000/api/login?password=111111&CurrencyType=1&userName={id}_{userName}"
    response = requests.get(url)
    response = json.loads(response.text)
    response = response.get('url')
    uid_list = re.findall(r'uid=(.*)&changeurl', response)
    uid = uid_list[0]

    return response, '241_' + userName


def To(tk):
    for i in range(1):
        url = f'http://192.168.10.213:9002/api/GameConfiger/callGame?tk={tk}&timestamp=11546545667'
        headers = {'token': tk}
        response = requests.get(url, headers=headers)
        print(response.text)


x = 3
if x == 0:
    LOGINUIR = "http://18.167.1.28:8031"
elif x == 1:
    LOGINUIR = f"http://192.168.10.25:9002"
else:
    LOGINUIR = f"http://192.168.10.21{x}:9002"

game = logAnalysisUtil.Record('admin', '123456', '', '', '')

for i in range(1):
    style = "241"
    Type = 43
    a, b, userName = login(LOGINUIR, Type)
    # b, userName = login1()
    num = str(400)
    data = dict(userName=userName, style=style, num=num, moneyType="1", actionType="13")  ## actionType="3"是加钱
    game.AddGold(data)
    webbrowser.open(b, 1)
    time.sleep(2)
