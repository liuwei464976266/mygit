import requests, json
url = 'http://192.168.10.212:9008/getSlotData'
headers ={
'Proxy-Connection': 'keep-alive',
'Content-Length': '96',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
# 改TOKEN下面
'token': '49FFAC1B532C392F3D2C4E8F9E46C103E7AF',
'Content-Type': 'application/json',
'Accept': '*/*',
'Origin': 'http://192.168.10.212:9002',
'Referer': 'http://192.168.10.212:9002'
}

gt = 130
while True:
    # 下面发请求数据
    data = {"gt":gt,"betScore":"300","actionType": 0,"betType":0}
    post = requests.post(url=url, json=data, headers=headers)
    b = post.request.body
    post = post.json()
    print(post)
    if post['code'] == 20017:
        print('ccc', b)
        break
    if post['et']['data']['isFree']:
        # 进入红利就停止，可以注销掉
        exit(6)
        # 下面是不朽，boy选场专用的
        data = {"gt": gt, "betScore":"3000","actionType":0,"freeType":1}
        dd = requests.post(url, json=data, headers=headers)
        for i in range(10000):
            data = {"gt":gt,"betScore":"300","actionType": 0,"betType":1}
            post = requests.post(url=url, json=data, headers=headers)
            a = post.request.body
            post = post.json()
            print(post)
            if post['code'] == 20017:
                print('lll', a)
                exit(-4)
            if post['et']['data']['residue'] == 0:
                print(i)
                break
            if post['et']['data']['residue'] > 10:
                print('复利')
                # exit(7)


