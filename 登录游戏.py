import requests, random, string, re, webbrowser, time, json, win32gui
from play.mangoCount import logAnalysisUtil
# from Hot_key import hotKey
MSSQL = logAnalysisUtil.MSSQL

def login(Url, num):
    currency = random.randint(1, 2)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': LOGINUIR[7:],
        'Origin': 'http://192.168.10.213:9002',
        'Referer': 'http://192.168.10.213:9002',
    }
    # userName = '我爱我家我爱我家'
    userName = 'liu' + (''.join(random.sample(string.digits, 3))) + (''.join(random.sample(string.ascii_letters, 3)))
    payload = dict(userName=userName, password='111111', currency=1, style=style, nickName='', sex=0)
    response = requests.post(Url + "/user/register", headers=headers, data=payload, allow_redirects=False)
    location = response.headers['location']
    location1 = location.replace(f'h/0', f'h/{num}')
    if len(location) > 70:
        uid_list = re.findall(r'uid=(.*)&changeurl', location)
        uid = uid_list[0]
        print(userName, uid)
    else:
        print('账号失败', userName, location1)
        return login(LOGINUIR, Type)
    return uid, location1, userName

def get_handles_id(title):
    '''
    根据标题找句柄
    :param title: 标题
    :return:返回句柄所对应的ID
    '''
    jh = []
    hwnd_title = dict()
    def get_all_hwnd(hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})
    win32gui.EnumWindows(get_all_hwnd, 0)
    for h, t in hwnd_title.items():
        if t != "":
            if title in t:
                jh.append(h)
    if len(jh) == 0:
        return []
    else:
        return jh

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


def login1(id, Cy, type=0):
    userName = 'liu' + (''.join(random.sample(string.digits, 3))) + (''.join(random.sample(string.ascii_letters, 3)))
    if type == 0:
        url = f"http://192.168.10.213:8000/api/login?password=111111&CurrencyType=1&userName={id}_{userName}"
    else:
        url = f"http://18.167.1.28:8043/api/login?password=111111&CurrencyType={Cy}&userName={id}_{userName}"

    response = requests.get(url)
    response = json.loads(response.text)
    response = response.get('url')
    uid_list = re.findall(r'uid=(.*)&changeurl', response)
    uid = uid_list[0]
    userName = str(id) + '_' + userName
    return response, userName


def To(tk):
    for i in range(6):
        url = f'http://192.168.10.213:9002/api/GameConfiger/callGame?tk={tk}&timestamp=11546545667'
        headers = {'token': tk}
        response = requests.get(url, headers=headers)
        print(response.text)


def updateGold(userName,money):
    ms = MSSQL(host='192.168.10.199', user='test', pwd='123456', db="OverseasGameV1", port=1433)
    ms.GetConnect()
    sql = f"UPDATE [dbo].[Game_UserInfo] SET [money] = {money*1000000} WHERE [uid] = (SELECT id FROM dbo.Game_UserInfoBase WHERE userName = '{userName}')"
    ms.ExecNonQuery(sql)

x = 0

if x == 0:
    LOGINUIR = "http://18.167.1.28:8031"
elif x == 5:
    LOGINUIR = f"http://192.168.10.25:9002"
else:
    LOGINUIR = f"http://192.168.10.21{x}:9002"

game = logAnalysisUtil.Record('admin', '123456', '', '', '')

for i in range(3):
    nick = {}
    style = "2"
    Type = 0
    c = i % 2+1
    a, b, userName = login(LOGINUIR, Type)
    num = 2000
    # updateGold(userName, num)
    data = dict(userName=userName, style=style, num=str(num), moneyType="1", actionType="3")  ## actionType="3"是加钱
    game.AddGold(data, 0)
    if Type == 46:
        webbrowser.open("http://192.168.10.88:5618/index.html?uid=" + a, 1)
    else:
        webbrowser.open(b, 1)
    time.sleep(1)
##    handles = []
##    handles += get_handles_id("MG Asia - Google Chrome")
##    handles += get_handles_id("Egret - Google Chrome")
##    handles += get_handles_id("Bobao Gaming - Google Chrome")
##    handles += get_handles_id("MG Asia - Google Chrome")
##    handle = handles[0]
##    nick.update({handle: userName})
##    print(nick)



