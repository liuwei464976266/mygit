import operator
from functools import reduce

import json
import random
import requests
import threading
import time

# global url, HL_url
url = "http://192.168.10.25:8001//api/UserCore/CallLotteryModel"
# HL_url = "http://43.231.7.174:8001//api/UserCore/CallLotteryFree"

threadLock = threading.Lock()

def ceshi(number):
    # winning = []
    global tj
    print("第%s个线程开始运行" % number)
    c = 0


    for b in range(2000000):
        # file2 = open(r'E:\金流\数组\统计%s.csv' % number, 'a')
        times = time.asctime()
        nun = random.randint(1, 4)
        if nun == 3:
            nun = random.randint(1, 2)
            # print(nun)
        '''liue351 - liue363(||362)'''
        list_Id = ['',
                   '',
                   '',
                   # '8C2F1E14A9A373DA4EF5D48526342B16B62C',
                   # '91042905F54E21BF9965C2BB4244C929D8FD',
                   # '25F260976373F10C10244B9529356B939E33',
                   # 'EACA25321E79F4AA6A01374414B49456E99C',
                   # 'F8796E9F187ED6FB3F9FA5C323621E5BFB95',
                   # '57238B0246932EAB5254E2C8CE518AE11C0D',
                   # 'E1E09749EDD925D290E4FD8EB7E8A9283B2D',
                   # 'DD3DBD8A7F7983E7FEC32BBC90705C516956',
                   # 'DA6C09C16D300E4D19C2E07226804E8BA700',
                   # 'E91A31B86A6CF20381E97D23D3A31189625F',
                   # '68D10518B566C40C99C8C2025F261A40012E',
                   # 'A51CCA91C9BFBA4C6D629D815CF0EC198027',
                   # '43D2086576665F79DCF28746A736C475CD85',
                   # '53B222F5AEEC7671DDDDEE2BE09253DAC8CE',
                   # '605D15895432BC60CAF2B6EFB6D3D55B9E15',
                   # '53B222F5AEEC7671DDDDEE2BE09253DAC8CE',
                   # '605D15895432BC60CAF2B6EFB6D3D55B9E15',

                   ]
        data = {"tk": list_Id[number],
                "gt": "127",
                "betScore": "3000",
                "timestamp": "15976259898985"
                }
        data1 = {"tk": list_Id[number],
                 "gt": "127",
                 "type": str(nun),
                 "timestamp": "1597628895465"
                 }
        data = json.dumps(data)
        data1 = json.dumps(data1)
        try:
            post = requests.post(url, data=data, timeout=5)
            # print(post.text)
            post = post.json()
            code = post.get("code")
            if code == 20000:
                # threadLock.acquire()  #加互斥锁
                print(threading.current_thread())  #查看那个线程中奖了
                # print(b)
                et = post.get("et")
                Data = et.get('Data')
                # print(Data)
                AdPoints = Data.get('AdPoints')
                ApiPoints = Data.get('ApiPoints')
                # print(AdPoints)
                # print(ApiPoints)
                Ap = reduce(operator.add, ApiPoints)

                # for key, nume in AdPoints.items():
                #     # print(key)
                #     winning.append(int(key))
                # print(winning)

                Points = Data.get("Points")
                # file2 .write(str(Points)+",,,"+str(Ap)+','+'\n')
                # file2.close()
                # print("写完关闭", number)
                # threadLock.release ()  # 释放锁
                # print(Points.count(13))
                if Points.count(12) > 2:
                    # po = requests.post(url, data=data)
                    # po.json()
                    # print(po.text)
                    print('进入第%s次红利' % c, number)
                    c += 1
                else:
                    pass

            # lens = len(winning)
            # if lens > 10 and lens % 50000 == 0 or b > 199998:
            #     # threadLock.acquire()  # 加互斥锁
            #     file = open(r'E:\金流\统计%s.csv' % number, 'a')
            #     file.write(str(times) + ',' + "开奖点" + ',' + "次数" + ',' + "\n")
            #     for x in range(1, 15):
            #         tj = (winning.count(x))
            #         # print(tj)
            #         file.write("开奖点" + ',' + str(x) + "," + str(tj) + "," + "红利" + ',' + str(c) + ',' "\n")
            #     file.close()
            #     print("打印列表", number)
            #     # threadLock.release()  # 释放锁
            #     pass
            # elif lens > 1000000:
            #     # file2.close()
            #     print("跳出循环", number)
            #     break

        except Exception as e:
            print(repr(e))
            print("错误了")
            # file = open(r'E:\金流\错误\统计%s.csv' % number, 'a')
            # file.write(str(times) + ',' + "序号" + ',' + "次数" + ',' + "\n")
            # for x in range(1, 15):
            #     tj = (winning.count(x))
            #     # print(tj)
            #     file.write("序号" + ',' + str(x) + "," + str(tj) + "," + "红利" + ',' + str(c) + ',' "\n")
            # file.close()
            pass
    # file2.close()
    # print("写完关闭", number)


if __name__ == '__main__':

    for i in range(15):
        print(i)
        threading.Thread(target=ceshi, args=(i,)).start()
