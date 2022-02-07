import requests, re, json
import random
import string

url = "http://192.168.10.213:9002/user/register"
exchange = 'http://192.168.10.213:9002/api/Service/ExchangeInOrOut'


def login(Url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '65',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': '192.168.10.213:9002',
        'Origin': 'http://192.168.10.213:9002',
        'Referer': 'http://192.168.10.213:9002/index.html?l=zh_CN&type=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
        }
    userName = ''.join(random.sample(string.ascii_letters + string.digits, 5))
    payload = dict(userName=userName, password='111111', currency='1', style='1', nickName='', sex=0)
    # payload = 'userName=li11&password=111111&currency=1&style=1&nickName=&sex=0'
    response = requests.post(Url, headers=headers, data=payload, allow_redirects=False)
    location = response.headers['location']
    print(location)
    if len(location) > 52:
        uid_list = re.findall(r'uid=(.*)&changeurl', location)
        uid = uid_list[0]
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


tk, location = login(url)
gold, money = Exchange(tk, 130, 1, location)

print(tk, gold)

