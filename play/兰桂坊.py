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
    # global tj
    print("第%s个线程开始运行" % number)
    c = 0


    for b in range(2000000):
        # file2 = open(r'E:\金流\数组\统计%s.csv' % number, 'a')
        times = time.asctime()
        # print(times)
        nun = random.randint(1, 4)
        if nun == 3:
            nun = random.randint(1, 2)
            # print(nun)
        '''liue351 - liue363(||362)'''
        list_Id = ['8C2F1E14A9A373DA4EF5D48526342B16B62C',
                   '91042905F54E21BF9965C2BB4244C929D8FD',
                   '25F260976373F10C10244B9529356B939E33',
                   'EACA25321E79F4AA6A01374414B49456E99C',
                   'F8796E9F187ED6FB3F9FA5C323621E5BFB95',
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
        data = {"tk": list_Id[number],
                "gt": "128",
                "betScore": "3000",
                "timestamp": "15976259898985"
                }
        data1 = json.dumps({"tk": list_Id[number], "type": 1, "gold": 10000000,
                            "timestamp": "1600914417600"})
        # data1 = {"tk": list_Id[number],
        #          "gt": "125",
        #          "type": str(nun),
        #          "timestamp": "1597628895465"
        #          }
        data = json.dumps(data)
        # data1 = json.dumps(data1)
        try:
            # global log
            post = requests.post(url, data=data, timeout=5)

            log = post.text
            print(log)
            post = post.json()
            code = post.get("code")
            if code == 20000:
                line = (post['et']['Data']['Lines'])
                # threadLock.acquire()  #加互斥锁
                print(threading.current_thread())  #查看那个线程中奖了
                # print(line)
                Points = []
                threadLock.acquire()
                for m in line:
                    Po = m['Points']
                    # print(i['Points'])
                    Points.append(Po)
                # print(Points)
                threadLock.release()
                # print(Points)
                lens = (len(Points))
                if lens > 2:
                    for i in range(len(Points)):
                        c = i + 1
                        # print(c)
                        # print(Points[i])
                        if c < lens:
                            # print(c)
                            # print('DI',Points[i][0:4], Points[c][1:5])
                            # print('D2',Points[i][5:9], Points[c][6:10])
                            # print('D3',Points[i][10:14], Points[c][11:])

                            if Points[i][0:4] == Points[c][1:5] and Points[i][5:9] == Points[c][6:10] and Points[i][
                                                                                                          10:14] == \
                                    Points[c][
                                    11:]:
                                print('yes=', number)
                            else:
                                threadLock.acquire()
                                print('不等于')
                                print(log)
                                file = open(r'E:\金流\log.txt', 'a')
                                file.write(times)
                                file.write(log+'\n')
                                file.close()
                                # with open(r'E:\金流\tset.csv', 'a')as f:
                                #     f.write(log+'\n')
                                print(Points[i], Points[c])
                                threadLock.release()


                # file2 .write(str(Points)+",,,"+str(Ap)+','+'\n')
                # file2.close()
                # print("写完关闭", number)
                # threadLock.release ()  # 释放锁
                # print(Points.count(13))
                # if Points.count(13) > 2:
                #     po = requests.post(HL_url, data=data1)
                #     po.json()
                #     # print(po.text)
                #     print('进入第%s次红利' % c, number)
                #     c += 1
                # else:
                #     pass


        except Exception as e:

            print(repr(e))
            print("错误了")
            file1 = open(r'E:\金流\log.txt', 'a')
            file1.close()
            file1.write('\n'+log)
            file1.close()

            if threadLock.acquire() == True:
                # print("有锁")
                threadLock.release()  # 释放锁
                # print("释放成功")
            else:
                pass



if __name__ == '__main__':

    for i in range(15):
        # print(i)
        threading.Thread(target=ceshi, args=(i,)).start()
