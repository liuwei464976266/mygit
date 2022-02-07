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
        list_Id = ['9A5678E15008542526BBFFF61BB33F13B024',
                   'B43C241FF49884ECEF3A7D938930AEC60152',
                   '534479D912937AA4DB19785B5CD957AE9A90',
                   'BED30D50A98EFC185CC3B8C1C03B4150A496',
                   '268B62F56B0F78D6C511C1356CC0DFC7C4E3',
                   'DD6C620C2E34C7CD61DEBEA9ABAFD6AC545F',
                   '77D8636D37F6C61EFA8F59CFC217BEDEB9CC',
                   '704B71B00C361B4E16567CF983372D9FBBE3',
                   'FC1D15163485300795499743A9793458B760',
                   '700529AA38DD9BB4B0190856B5EAF4EB8F4A',
                   '1AED0EE98AD4155222DF3766AE909E051C32',
                   '59C74B5504AC43F3FA595B9EA40C2D72CC10',
                   'F3EBB0C9F79C22A4F9BD106F1E9EFB680AAE',
                   '189A3B516B4CE8CD3463599E1E1C01F0621D',
                   '3828711C4353A737792BAF7BD06EE93F7C66',


                   ]
        data = {"tk": list_Id[number],
                "gt": "127",
                "betScore": "2500",
                "timestamp": "15976259898985"
                }
        data1 = {"tk": list_Id[number],
                 "gt": "130",
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
            # print(post)
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
