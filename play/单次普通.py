import json
import threading

import requests


threadLock = threading.Lock()


def ceshi(number):
    url = "http://192.168.10.25:8001/api/usercore/CallLotteryRoteRow"

    for b in range(200000):
        list_Id = ['25D0D42D9F2972A75BDF544C107B43D7FBB3',
                   'F80780E9E869447074EAFA8F9CF8B84F4A60',
                   'F93133D8CB02F63CFD5FA72023DE501A150F',
                   ]
        try:
            data1 = {"tk": list_Id[number],
                     "gt": "136",
                     "betScore": "2300",
                     "timestamp": 46456456,
                     "RoteKey": 'ghjghjgddd12',
                     "RoteRow": 3,
                     }
            # print(data1.get("RoteRow"))

            data1 = json.dumps(data1)
            post = requests.post(url, data=data1, timeout=5)
            log = post.text
            post = post.json()
            # print(post)
            code = post.get("code")
            Points = post['et']['Data']['Points']
            if code == 20000:
                # print(log)
                # threadLock.acquire()  #加互斥锁
                # print(threading.current_thread())  #查看那个线程中奖了
                # line = (post['et']['Data']['RoteKey'])
                gold = (post['et']['Gold']) / 100
                Ngold = (post['et']['NGold']) / 100
                go = (f'第{b}次--赢取{gold}     --剩余{Ngold}')
                print(go)
                if 6 == Points[2] or 6 == Points[7] or 6 == Points[12]:
                    if 12 == Points[2] or 12 == Points[7] or 12 == Points[12]:
                        print('摇出来了')
                        input(post)
                # print(line)
            else:
                print(post)
                break

        except Exception as e:
            print(repr(e))
            print("错误了")


if __name__ == '__main__':

    for i in range(1):
        # print(i)
        threading.Thread(target=ceshi, args=(i,)).start()
