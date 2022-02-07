import operator
from functools import reduce

import json
import random
import requests
import threading
import time

url = "http://43.231.7.174:8001/api/Usercore/callShzbet"
HL_url = "http://43.231.7.174:8001/api/Usercore/callShzFree"

threadLock = threading.Lock()
ll = 54
def ceshi(number):
    # global freecount
    winning = []
    # global tj
    print("第%s个线程开始运行" % number)
    for num in range(2000000):
        # file2 = open (r'E:\金流\数组\普通场%s.csv' % number, 'a')
        times = time.asctime()
        nun = random.randint(1, 3)
        # print(nun)
        list_Id = ['4C22727E8E34AB2C01D00F24FABC6183A919',
                   '7C4EF7674A1986056D65DA4EAF597FBDF056',
                   '0F27AC3F43C3E8DF49EA37ABF640CBEC0601',
                   'D872E4E4D14866C8895D19AFE1697D3B9A12',
                   'B83D7B40E97029DBBF34D898CC1B7C7FEAC2',
                   'E3CE64069FC3A9BB14D360E4F60CEF822ED5',
                   '68B8E0D487EFA42BB7027FE93AD511D26F9B',
                   'C3E11068C83ED174192F44B30CB0764FF360',
                   '434EE1EE57550A95AFCA2A5E65EABC993A89',
                   'D03D9154B40829F9F3D8A8769B079E67A139',
                   '2EC893A4B821F17CBB79F7A81A357A10187B',
                   '53606E633AF7927A54967E52AF189EDD6143',


                   ]
        data = json.dumps({"tk": list_Id[number],
                "gt": "123",
                "betScore": "100",
                "betSum": '900',
                "wire": '9',
                "timestamp": "15976259898985",
                "Count": '0'
                })

        try:

            post = requests.post(url, data=data, timeout=5)
            # print(post.request.body)
            time.sleep(1)
            post = post.json()
            # print(type(post))
            code = post.get("code")
            if code == 20000:
                threadLock.acquire()  #加互斥锁
                file2 = open(r'E:\金流\数组\普通场.csv', 'a')
                print(threading.current_thread())  #查看那个线程中奖了
                # print(b)
                et = post.get("et")
                # print(et)
                orderId = et.get('orderId')
                imG = et.get('img')
                img = reduce(operator.add, imG)   #img 分解写入文档—开奖牌数据
                # print(img)
                imgdetails = et.get('imgdetails')
                # print('libiao=', imgdetails)
                for list_imgdetails in imgdetails:  #遍历
                    if list_imgdetails.get('gold') > 0:
                        # print('中奖序列=', list_imgdetails)
                        winning.append(list_imgdetails)
                    # gold = list_imgdetails.get("gold")
                    # print(gold)

                    # for key, value in list_imgdetails.items():
                    #     print(key, value)
                # gold = et.get('gold')
                # print(gold)
                file2 .write("liue"+str(number+ll)+","+str(orderId)+'a'+",,"+str(img)+',,,'+str(winning)+'\n')
                file2.close()

                # print('winning=', winning) #可以在此处写入局号 ，牌，中奖信息了
                winning = []
                threadLock.release()  # 释放锁
                freecount = et.get("freecount")
                # print(Points.count(13))
                vu3 = {'1': '16', '2': '8', '3': '5'}
                if freecount >= 3:
                    times1 = int(time.time() * 1000)
                    data1 = {"tk": list_Id[number],
                                        "freeType": nun,
                                        "freeCount": freecount,
                                        "timestamp": str(times1)
                                        }
                    print(f'红利为{freecount}连')
                    nun3 = (int(vu3[str(nun)]) * (freecount - 2))
                    # data2 = json.dumps({"tk": list_Id[number],
                    #          "gt": "123",
                    #          "betScore": "100",
                    #          "betSum": '900',
                    #          "wire": '9',
                    #          "timestamp": "15976259898985",
                    #          "Count": str(nun3)
                    #          })
                    # data2 = json.dumps(data2)
                    po1 = requests.post(HL_url, data=json.dumps(data1), timeout=5)
                    # print(type(po1))
                    # print("小游戏选择", po1.text)
                    if code == 20000:
                        threadLock.acquire()  # 加互斥锁
                        for x in range(nun3):
                            win = []
                            data2 = json.dumps({"tk": list_Id[number],
                                                "gt": "123",
                                                "betScore": "100",
                                                "betSum": '900',
                                                "wire": '9',
                                                "timestamp": "15976259898985",
                                                "Count": str(nun3)
                                                })
                            try:
                                po = requests.post(url, data=data2, timeout=5)
                                sat = json.loads(po.text)
                                et1 = sat.get("et")
                                orderId1 = et1.get('orderId')
                                imG1 = et1.get('img')
                                img1 = reduce(operator.add, imG1)
                                imgdetails1 = et1.get('imgdetails')
                                # print('libiao=', imgdetails)
                                for list_imgdetails1 in imgdetails1:  # 遍历
                                    if list_imgdetails1.get('gold') > 0:
                                        # print('中奖序列=', list_imgdetails)
                                        win.append(list_imgdetails1)
                                file = open(r'E:\金流\数组\红利.csv', 'a')
                                file.write("liue" + str(number + ll) + "," + str(orderId1) + 'a' + ",," + str(
                                    img1) + ',,,' + str(win) + '\n')
                                # print(po.request.body)
                                print("小游戏里面", nun3)
                                nun3 -= 1
                            except:
                                print("小游戏超时...........")
                                pass

                        threadLock.release()  # 释放锁

                else:
                    pass

            # if num > 10 and num % 500 == 0:
            #     threadLock.acquire()  # 加互斥锁
            #     file = open(r'E:\金流\统计%s.csv' % number, 'a')
            #     file.write(str(times) + ',' + "开奖点" + ',' + "次数" + ',' + "\n")
            #     for x in range(1, 15):
            #         tj = (winning.count(x))
            #         print(tj)
            #         file.write("开奖点" + ',' + str(x) + "," + str(tj) + "," + "红利" + ',' + str(c) + ',' "\n")
            #     file.close()
            #     print("打印列表", number)
            #     threadLock.release()  # 释放锁
            #     pass
            # elif num > 1000000:
            #     # file2.close()
            #     print("跳出循环", number)
            #     break

        except Exception as e:
            print(repr(e))
            print("错误了")
            if threadLock.acquire()==True:
                # print("有锁")
                threadLock.release()  # 释放锁
                # print("释放成功")
            else:
                pass

        #     file = open(r'E:\金流\错误\统计%s.csv' % number, 'a')
        #     file.write(str(times) + ',' + "序号" + ',' + "次数" + ',' + "\n")
        #     for x in range(1, 15):
        #         tj = (winning.count(x))
        #         # print(tj)
        #         file.write("序号" + ',' + str(x) + "," + str(tj) + "," + "红利" + ',' + str(num) + ',' "\n")
        #     file.close()
        #     pass
        # num += 1


if __name__ == '__main__':

    for i in range(12):
        print(i)
        threading.Thread(target=ceshi, args=(i,)).start()
