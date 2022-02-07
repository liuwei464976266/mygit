import json
import random
import threading
import time

import requests

# global url, HL_url
url = "http://192.168.10.25:8001//api/UserCore/CallLotteryModel"  # 小游戏接口
# HL_url = "http://43.231.7.174:8001//api/UserCore/CallLotteryFree"
url1 = "http://192.168.10.25:8001/api/UserCore/AddPlayerGold"  # 金币接口

threadLock = threading.Lock()


def wirte(file):
    with open(r'E:\金流\log.txt', 'a')as f:
        f.write(time.ctime() + '\n'*2)
        f.write(file)

def read1(Achievement, gametype):
    keys = []
    valus = []
    # print("进入判断成就方法了")
    for key, valu in Achievement.items():
        keys.append(key)
        for key1, valu1 in valu.items():
            valus.append(key1)
            # print(valus)
        # print("编号", keys)`
        keys.append(valus)
        valus = []
    # keys = (list(map(int, keys)))
    # print(keys)
    # keys.sort()
    # print(keys)
    if len(keys) >= 39:
        cl = f'完成全部解锁{gametype}'
        print(cl)
        nu2 = 0
        for x in range(1, 24, 2):
            nu1 = (len(keys[x]))
            nu2 = nu2 + nu1
        print(nu2)
        if nu2 > 39:
            print(f"{gametype}全部解锁", keys)
            input('dengdai')


def ceshi(number, gametype):
    print("第%s个线程开始运行" % number)
    a = threading.current_thread() # 查看那个线程中奖了
    c = 0
    for b in range(100):
        # time.sleep(1)
        # file2 = open(r'E:\金流\数组\统计%s.csv' % number, 'a')
        nun = random.randint(1, 4)
        if nun == 3:
            nun = random.randint(1, 2)
            # print(nun).
        '''liue351 - liue363(||362)'''
        list_Id = ['264BA58BAD563225D421B6B33A2DA8A713D5', '3828711C4353A737792BAF7BD06EE93F7C66', '53B222F5AEEC7671DDDDEE2BE09253DAC8CE', 'EF51C6643384A024915589A039F53664F0E4', '7B5C6B540F01CE8984579F11F2FB1AF7C088', 'FD3998A4E61BDFD26B859AB16DF0E009E302', 'E91A31B86A6CF20381E97D23D3A31189625F', 'EACA25321E79F4AA6A01374414B49456E99C', '700529AA38DD9BB4B0190856B5EAF4EB8F4A', '1AED0EE98AD4155222DF3766AE909E051C32', '68D10518B566C40C99C8C2025F261A40012E', 'FC1D15163485300795499743A9793458B760', '189A3B516B4CE8CD3463599E1E1C01F0621D', 'A51CCA91C9BFBA4C6D629D815CF0EC198027', 'F3EBB0C9F79C22A4F9BD106F1E9EFB680AAE', 'DA6C09C16D300E4D19C2E07226804E8BA700', 'E1E09749EDD925D290E4FD8EB7E8A9283B2D', 'DD6C620C2E34C7CD61DEBEA9ABAFD6AC545F', 'F8796E9F187ED6FB3F9FA5C323621E5BFB95', '77D8636D37F6C61EFA8F59CFC217BEDEB9CC', '5D8D5117ED6E29453950152AFDBCB0675479', '8C2F1E14A9A373DA4EF5D48526342B16B62C', 'BA889F7DDA9EEABA8F78FD113F1A9D159503', '43D2086576665F79DCF28746A736C475CD85', 'BCF0579533CACBDEF5A81BE959062F93DEB4', '659CB6F2B4066B902D3EED9D4130D69F0938', '57238B0246932EAB5254E2C8CE518AE11C0D', 'DD3DBD8A7F7983E7FEC32BBC90705C516956', 'BED30D50A98EFC185CC3B8C1C03B4150A496', '59C74B5504AC43F3FA595B9EA40C2D72CC10', '86C007A86E559AD99D7E2CA7263A2E0D4C3B', '9A5678E15008542526BBFFF61BB33F13B024', '268B62F56B0F78D6C511C1356CC0DFC7C4E3', 'EF564D5DF8BAC1B627A427E19A8B49038FB5', '704B71B00C361B4E16567CF983372D9FBBE3', '8ADA6E18641C9CF858732DD36DBDD899A7CC', '91042905F54E21BF9965C2BB4244C929D8FD', '4F50BFB370ED44FEA0FFA20957B6E5E6E86E', '25F260976373F10C10244B9529356B939E33', 'B43C241FF49884ECEF3A7D938930AEC60152', '605D15895432BC60CAF2B6EFB6D3D55B9E15', '534479D912937AA4DB19785B5CD957AE9A90']
        data = {"tk": list_Id[number],
                "gt": gametype,
                "betScore": "2500",
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
        log = ''
        try:
            # global log
            post = requests.post(url, data=data, timeout=5)
            log = post.text
            # print(gametype, log)
            post = post.json()
            code = post.get("code")
            print(a, f'次数{b}', post)
            if code == 20000:
                li = post['et']['Data']['Points']
                if li.count(12) > 2:
                    print('红利')
                    # input('请输入')

                '''li = (post['et']['Data']['Points'])
                # li = (post['et']['Data']['Lines'])
                isFree = (post['et']['Data']['isFree'])
                # print(isFree)
                Achievement = (post['et']['Data']['Achievement'])

                gold = (post['et']['Gold']) / 100
                Ngold = (post['et']['NGold']) / 100

                print(f'{number}号玩家--第{b}次=', Ngold, 'win', gold)

                if gametype != 134 and gametype != 135:
                    read1(Achievement, gametype)
                # print(li, "红利判断", isFree)
                # li = (line[0]['Points'])
                for i in range(5):
                    if li[i] != li[i + 5] != li[i + 10] != li[i]:
                        x = 3
                    else:
                        print(f"第{i + 1}轴错误了，刘wei遭起")
                        wirte(log)
                        print(log)
                        input('凉凉')
                    if i == 1 or i == 3:
                        continue
                    # print('此时的i=', i)
                    if li[i] == 13 or li[i + 5] == 13 or li[i + 10] == 13:
                        # print(li[i], li[i+5], li[i+10])
                        # print(f"{i+1}列出现多个百搭")
                        # print(log)
                        wirte(log)
                        input("是否继续请输入")'''
            elif code == 20017:
                po = requests.post(url1, data=data1, timeout=5)
                print(po.text)

        except Exception as e:
            print(repr(e))
            print("错误了")
            print(gametype, log)
            # file1 = open(r'E:\金流\log.txt', 'a')
            # file1.write(log + '\n')
            # file1.close()

            if threadLock.acquire() == True:
                print("有锁")
                threadLock.release()  # 释放锁
                print("释放成功")
            else:
                pass


if __name__ == '__main__':
    times = time.asctime()
    list_o = [127, 128, 130, 131, 132, 133, 134, 135, 136]
    for i in range(10):
        ga = list_o[6]
        print(111111)
        a = threading.Thread(target=ceshi, args=(i, ga)).start()
        print(a)

