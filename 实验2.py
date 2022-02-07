import requests, random, string, re, webbrowser, sys, io
Url = "http://192.168.10.212:9003/user/register"


def login(userName, nickName):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '65',
        'Host': '192.168.10.212:9003',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'http://192.168.10.212:9003',
        'Referer': 'http://192.168.10.212:9003/index.html?l=zh_CN&type=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
        }

    payload = dict(userName=userName, password='111111', currency=1, style='7', nickName=nickName, sex=0)
    # payload = 'userName=li11&password=111111&currency=1&style=1&nickName=&sex=0'
    response = requests.post(Url, headers=headers, data=payload, allow_redirects=False)
    location = response.headers['location']
    print(location)
    if len(location) > 62:
        print('错误注册成功', userName, nickName)
        with open('error2.txt', 'a', encoding='utf-8') as f:
            f.write(userName +'----'+ nickName + '\n')
            return
    elif len(location) == 52:
        print('已注册了', userName, nickName)
        with open('error.txt', 'a', encoding='utf-8') as f:
            f.write(userName + '\n')


def main():
    with open("blacklist.txt", "r", encoding='utf-8') as f:
        JJ = 0
        for i in f.readlines():
            Name = (''.join(random.sample(string.ascii_letters + string.digits, 9)))
            JJ += 1
            line = i.strip()
            print(line)
            if int(JJ) > 0:
                login(line, Name)
                print(JJ)

# main()
# login('YsdY.org','jshdshq855')

