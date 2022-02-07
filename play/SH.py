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
def ceshi(number):
    # global freecount
    winning = []
    global tj
    print("第%s个线程开始运行" % number)
    for num in range(2000000):
        file2 = open(r'E:\金流\数组\统计%s.csv' % number, 'a')
        times = time.asctime()
        nun = random.randint(1, 3)
        # print(nun)

        list_Id = ['04E5B19069085B7E7F0E4A75A75635D86E74',
                   ]
        data = {"tk": list_Id[number],
                "gt": "123",
                "betScore": "3000",
                "betSum": '1500',
                "wire": '5',
                "timestamp": "15976259898985",
                "Count": '0'
                }
        data = json.dumps(data)
        try:
            post = requests.post(url, data=data, timeout=5)
            # print(post.text)
            time.sleep(1)
            post = post.json()
            code = post.get("code")
            if code == 20000:
                threadLock.acquire()  #加互斥锁
                print(threading.current_thread())  #查看那个线程中奖了
                # print(b)
                et = post.get("et")
                # print(et)
                orderId = et.get('orderId')
                imG = et.get('img')
                img = reduce(operator.add, imG) #img 分解写入文档—开奖牌数据
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
                # file2 .write(str(Points)+",,,"+str(Ap)+','+'\n')
                # file2.close()
                # print("写完关闭", number)
                print('winning=', winning) #可以在此处写入局号 ，牌，中奖信息了
                winning = []
                threadLock.release ()  # 释放锁
                freecount = et.get("freecount")
                # print(Points.count(13))
                vu3 = {'1': '16', '2': '8', '3': '16'}
                data1 = {"tk": list_Id[number],
                         "gt": "123",
                         "freeType": str(nun),
                         "freeCount": str(freecount),
                         "timestamp": "1597628895465"
                         }
                data1 = json.dumps(data1)
                if freecount >= 3:
                    print(f'红利为{freecount}连')
                    nun3 = (int(vu3[str(nun)]) * (freecount - 2))
                    data2 = {"tk": list_Id[number],
                             "gt": "123",
                             "betScore": "3000",
                             "betSum": '1500',
                             "wire": '5',
                             "timestamp": "15976259898985",
                             "Count": str(nun3)
                             }
                    data2 = json.dumps(data2)
                    po1 = requests.post(HL_url, data=data1)
                    print(po1.text)
                    if code == 20000:
                        print(nun3)
                        for x in range(nun3):
                            po = requests.post(HL_url, data=data2)
                            po.json()
                            print(po.text)
                else:
                    pass

            if num > 10 and num % 500 == 0:
                threadLock.acquire()  # 加互斥锁
                file = open(r'E:\金流\统计%s.csv' % number, 'a')
                file.write(str(times) + ',' + "开奖点" + ',' + "次数" + ',' + "\n")
                for x in range(1, 15):
                    tj = (winning.count(x))
                    print(tj)
                    file.write("开奖点" + ',' + str(x) + "," + str(tj) + "," + "红利" + ',' + str(c) + ',' "\n")
                file.close()
                print("打印列表", number)
                threadLock.release()  # 释放锁
                pass
            elif num > 1000000:
                # file2.close()
                print("跳出循环", number)
                break

        except Exception as e:
            print(repr(e))
            print("错误了")
            file = open(r'E:\金流\错误\统计%s.csv' % number, 'a')
            file.write(str(times) + ',' + "序号" + ',' + "次数" + ',' + "\n")
            for x in range(1, 15):
                tj = (winning.count(x))
                # print(tj)
                file.write("序号" + ',' + str(x) + "," + str(tj) + "," + "红利" + ',' + str(num) + ',' "\n")
            file.close()
            pass
        num += 1


if __name__ == '__main__':

    for i in range(1):
        print(i)
        threading.Thread(target=ceshi, args=(i,)).start()
