import requests, random, string, re, webbrowser, time, os, json, re
from urllib.parse import urlparse, parse_qs
import logAnalysisUtil
import configparser
import win32gui, addGold


def login(loginUrl, style, userName, gameType=0, currencyType=1, language=1, money=100, actionType='3', url_type=1,
          open_browser=False):
    url_type = int(url_type)
    if url_type == 2:
        userName = userName.split('_')[-1]
        style = style
        loginUrl = 'http://18.167.1.28:8031/user/register'
        # userName = "s" + str(random.randint(100000, 99999999))
        data = {
            'userName': userName,
            'password': '123456',
            'currency': currencyType,
            'style': style,
            'sex': 0,
            'nickName': ''
        }
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Host': '18.167.1.28:8031',
            'Origin': 'http://18.167.1.28:8031',
            'Referer': 'http://18.167.1.28:8031/'
        }

        actionType = '3'
        response = requests.post(url=loginUrl, headers=headers, data=data, allow_redirects=False)
        if response.status_code == 302:
            url = response.headers['Location']
        else:
            return -2
            url = backStageUrl
        if url == "http://18.167.1.28:8031/index.html?l=zh_CN&type=0":
            return -2
        backStageUrl = "http://18.167.1.28:8032"
        record = logAnalysisUtil.Record('admin', '123456', '', '', '')
        data = dict(userName=userName, style=str(style), num=str(money), moneyType="1", actionType=actionType)
        record.AddGold(data, url=backStageUrl, style=style)
    else:
        # data = {
        #     'style':style,
        #     'userName':userName,
        #     'gameType':gameType,
        #     'currencyType':currencyType,
        #     'language':language
        # }
        data = {
            'userName': userName,
            'password': '123456',
            'currency': currencyType,
            'style': style,
            'sex': 0,
            'nickName': style + userName
        }
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Host': HOST,
            'Origin': "http://" + HOST,
            'Referer': "http://" + HOST
        }
        # response = requests.post(loginUrl,data)
        response = requests.post(url=loginUrl, headers=headers, data=data, allow_redirects=False)
        # response = response.json()
        if response.status_code == 302:
            url = response.headers['Location']
        # if response.get('code') == 1:
        #     url = response.get('url')
        backStageUrl = BACK_STAGE_URL
        try:
            tk = getTokenByUrl(url)[0]
        except:
            return -2
        try:
            addGold.userGoldControl(target_gold=money, userName=userName, style=style)
        except:
            pass
        url = url.replace('/0/', f'/{GAMETYPE}/')
        # url = 'http://192.168.10.102:5612/index.html?uid=' + tk
        # url = 'http://192.168.10.88:5618/index.html?uid=' + tk
        if open_browser:
            opens_browser(url, userName)
        else:
            init_user(tk)
    return tk


def init_user(tk):
    url = f"http://{HOST}/api/UserCore/callCore?tk={tk}&timestamp=1655101591671"
    headers = get_headers(tk)
    response = requests.get(url, headers=headers)


def get_headers(tk):  # 获取一个通用请求头
    headers = {'token': tk,
               'Content-Type': 'application/json'}
    return headers


def opens_browser(url, userName):
    global userName_handle
    chromePath = CHROMEPATH
    webbrowser.register('chrome', None,
                        webbrowser.BackgroundBrowser(chromePath))  # 这里的'chrome'可以用其它任意名字，如testB，这里将想打开的浏览器保存到'chrome'
    webbrowser.get('chrome').open(url, new=1, autoraise=True)
    time.sleep(5)
    handles = []
    handles += get_handles_id("MG Asia - Google Chrome")
    handles += get_handles_id("Egret - Google Chrome")
    handles += get_handles_id("Bobao Gaming - Google Chrome")
    handles += get_handles_id("MG Asia - Google Chrome")
    handle = handles[0]
    userName_handle.update({handle: userName})


def getTokenByUrl(url):
    o = urlparse(url)
    query = parse_qs(o.query)
    tk = query.get('uid')
    return tk


def loadConfig():
    cf = configparser.ConfigParser()
    cf.read('login.config')
    loginConfig = cf.options('config')
    HOST = cf.get('config', 'HOST')
    LOGIN_URL = cf.get('config', 'LOGIN_URL')
    STYLE = cf.get('config', 'STYLE')
    NICK_FIRST_NAME = cf.get('config', 'NICK_FIRST_NAME')
    URL_TYPE = cf.get('config', 'URL_TYPE')
    CURRENCY_TYPE = cf.get('config', 'CURRENCY_TYPE')
    BACK_STAGE_URL = cf.get('config', 'BACK_STAGE_URL')
    MONEY = cf.get('config', 'MONEY')
    GAMETYPE = cf.get('config', 'GAMETYPE')
    CHROMEPATH = cf.get('config', 'CHROMEPATH')
    return HOST, LOGIN_URL, STYLE, NICK_FIRST_NAME, URL_TYPE, CURRENCY_TYPE, BACK_STAGE_URL, MONEY, GAMETYPE, CHROMEPATH


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


def register_user(userName=None, open_browser=False):
    global HOST, LOGIN_URL, STYLE, NICK_FIRST_NAME, URL_TYPE, CURRENCY_TYPE, BACK_STAGE_URL, MONEY, GAMETYPE, CHROMEPATH
    HOST, LOGIN_URL, STYLE, NICK_FIRST_NAME, URL_TYPE, CURRENCY_TYPE, BACK_STAGE_URL, MONEY, GAMETYPE, CHROMEPATH = loadConfig()
    loginUrl = LOGIN_URL
    style = STYLE
    userName_like = NICK_FIRST_NAME + '%'
    userName_max = logAnalysisUtil.get_userName_max_by_userName_like(userName_like)
    userName_num_list = re.findall(r'\d+', userName_max)
    if len(userName_num_list) == 0:
        userName_num = userName_max + '1'
    else:
        userName_num = userName_num_list[-1]
    while True:
        try:
            userName_num = str(int(userName_num) + 1)
        except:
            userName_num = userName_num + "1"
        userName = NICK_FIRST_NAME + userName_num
        tk = login(loginUrl, style, userName, url_type=URL_TYPE, currencyType=CURRENCY_TYPE, money=MONEY,
                   open_browser=open_browser)
        if tk != -2:
            return tk


def main():
    global userName_handle
    userName_handle = {}
    for i in range(1):
        register_user(open_browser=True)
    print(userName_handle)


if __name__ == '__main__':
    main()
