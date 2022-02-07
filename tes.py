import json
import requests
import threading
import time


def call(tk,gametype):
    url = "http://192.168.10.212:8002/callInitialize"
    data = {
            "gt":gametype,
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
# url = "192.168.10.82:8031/registerUser "
# tk = requests.get(url).json().get('tk')
# tokenid = tk
# print(tokenid)
def call2(tk,gametype):
    url = "http://192.168.10.82:8031/getSlotData"
    data = {
            "gt":gametype,
            "timestamp": 45646545654,
            'actionType': '0',
            "betScore": 25,
            }
    headers = {
        'token': tk,
        'Content-Type': 'application/json',
        }
    data = json.dumps(data)
    response = requests.post(url=url, data=data, headers=headers)
    response = response.json()
    print("正常", response)


# gameType = 136
# betScore = 2500
tk = '4EB40E44E28449E61940E09B14C92C8D63FA'







# url = "http://192.168.10.82:8031/getSlotData"
# HL_url = "http://43.231.7.174:8001//api/UserCore/CallLotteryFree"

threadLock = threading.Lock()

def ceshi(number):
    url = "http://192.168.10.82:8031/getSlotData"
    print("第%s个线程开始运行" % number)
    for b in range(2000000):
        times = time.asctime()
        # print(times)
        '''liue351 - liue363(||362)'''
        list_Id = ['1F6215DFB4044F6F3522D664D1E7EDFB7C43',
                   '8EBE0D4B677FB273764B95576552263CFEBC',
                   '69AD1BAF29C02CF6D093B429BD077B73E20F',
                   '1CD1230C20878FE9031857F4AE91E6CD9A58',
                   '3E3B4E8E25567F7B2B559D3127323068C962',


                   '57238B0246932EAB5254E2C8CE518AE11C0D',
                   'E1E09749EDD925D290E4FD8EB7E8A9283B2D',
                   'DD3DBD8A7F7983E7FEC32BBC90705C516956',
                   'DA6C09C16D300E4D19C2E07226804E8BA700',
                   'E91A31B86A6CF20381E97D23D3A31189625F',
                   '68D10518B566C40C99C8C2025F261A40012E',
                   'A51CCA91C9BFBA4C6D629D815CF0EC198027',
                   '43D2086576665F79DCF28746A736C475CD85',
                   '53B222F5AEEC7671DDDDEE2BE09253DAC8CE',
                   '605D15895432BC60CAF2B6EFB6D3D55B9E15',
                   '53B222F5AEEC7671DDDDEE2BE09253DAC8CE',
                   '605D15895432BC60CAF2B6EFB6D3D55B9E15',

                   ]
        data = {
            "gt": 134,
            "timestamp": 45646545654,
            'actionType': '0',
            "betScore": 2500,
            }
        headers = {
            'token': list_Id[number],
            'Content-Type': 'application/json'
            }

        data = json.dumps(data)

        try:
            post = requests.post(url, data=data, headers=headers, timeout=5)
            log = post.text
            print(log)
            post = post.json()
            code = post.get("code")
            # if code == 20000:
            #     line = (post['et']['Data']['Lines'])
            #     # threadLock.acquire()  #加互斥锁
            #     print(threading.current_thread())  #查看那个线程中奖了
            #     # print(line)
            #     Points = []
            #     threadLock.acquire()
            #     for m in line:
            #         Po = m['Points']
            #         # print(i['Points'])
            #         Points.append(Po)
            #     # print(Points)
            #     threadLock.release()
            #     # print(Points)
            #     lens = (len(Points))
            #     if lens > 2:
            #         for i in range(len(Points)):
            #             c = i + 1
            #             # print(c)
            #             # print(Points[i])
            #             if c < lens:
            #                 # print(c)
            #                 # print('DI',Points[i][0:4], Points[c][1:5])
            #                 # print('D2',Points[i][5:9], Points[c][6:10])
            #                 # print('D3',Points[i][10:14], Points[c][11:])
            #
            #                 if Points[i][0:4] == Points[c][1:5] and Points[i][5:9] == Points[c][6:10] and Points[i][
            #                                                                                               10:14] == \
            #                         Points[c][
            #                         11:]:
            #                     print('yes=', number)
            #                 else:
            #                     threadLock.acquire()
            #                     print('不等于')
            #                     print(log)
            #                     file = open(r'E:\金流\log.txt', 'a')
            #                     file.write(times)
            #                     file.write(log+'\n')
            #                     file.close()
            #                     # with open(r'E:\金流\tset.csv', 'a')as f:
            #                     #     f.write(log+'\n')
            #                     print(Points[i], Points[c])
            #                     threadLock.release()
            #
            #
            #     # file2 .write(str(Points)+",,,"+str(Ap)+','+'\n')
            #     # file2.close()
            #     # print("写完关闭", number)
            #     # threadLock.release ()  # 释放锁
            #     # print(Points.count(13))
            #     # if Points.count(13) > 2:
            #     #     po = requests.post(HL_url, data=data1)
            #     #     po.json()
            #     #     # print(po.text)
            #     #     print('进入第%s次红利' % c, number)
            #     #     c += 1
            #     # else:
            #     #     pass

        except Exception as e:
            print(repr(e))
            print("错误了")
            file1 = open(r'E:\金流\log.txt', 'a')
            file1.write('\n'+log)
            file1.close()
            if threadLock.acquire() == True:
                # print("有锁")
                threadLock.release()  # 释放锁
                # print("释放成功")
            else:
                pass


if __name__ == '__main__':
    for i in range(5):
        # print(i)
        threading.Thread(target=ceshi, args=(i,)).start()
