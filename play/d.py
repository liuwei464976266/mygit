import json
import requests
import threading

url = "http://192.168.10.25:8001//api/UserCore/CallLotteryModel" #  小游戏接口
url1 = "http://192.168.10.25:8001/api/UserCore/AddPlayerGold"  #  金币接口
url2 = "http://192.168.10.25:8001/api/usercore/CallLotteryRoteRow" # 单次旋转接口

threadLock = threading.Lock()

def wirte(file):
    with open(r'E:\金流\log.txt', 'a')as f:
        f.write(file + '\n'*2)

def read1(Achievement, gametype):
    keys = []
    valus = []
    # print("进入判断成就方法了")
    for key, valu in Achievement.items():
        keys.append(key)
        for key1, valu1 in valu.items():
            valus.append(key1)
            # print(valus)
        # print("编号", keys)
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
            nu2 = nu2+nu1
        print(nu2)
        if nu2 > 39:
            print(f"{gametype}全部解锁", keys)
            input('dengdai')


def ceshi(number, gametype):

    print("第%s个线程开始运行" % number)
    for b in range(1000000):

        '''liue351 - liue363(||362)'''
        list_Id = ['216EF4A83F9E837C3D612D2E24BF813642F8',
                   'BCF0579533CACBDEF5A81BE959062F93DEB4',
                   'EF564D5DF8BAC1B627A427E19A8B49038FB5',
                   'BA889F7DDA9EEABA8F78FD113F1A9D159503',
                   '5D8D5117ED6E29453950152AFDBCB0675479',
                   '659CB6F2B4066B902D3EED9D4130D69F0938',
                   '38F6112BC230DB14121E170C7B7804F7CA3E',
                   'FD3998A4E61BDFD26B859AB16DF0E009E302',
                   '86C007A86E559AD99D7E2CA7263A2E0D4C3B',
                   '7B5C6B540F01CE8984579F11F2FB1AF7C088',
                   '4F50BFB370ED44FEA0FFA20957B6E5E6E86E',
                   '8ADA6E18641C9CF858732DD36DBDD899A7CC',
                   '43D2086576665F79DCF28746A736C475CD85',
                   '53B222F5AEEC7671DDDDEE2BE09253DAC8CE',
                   '605D15895432BC60CAF2B6EFB6D3D55B9E15',
                   '53B222F5AEEC7671DDDDEE2BE09253DAC8CE',
                   '605D15895432BC60CAF2B6EFB6D3D55B9E15',
                   '9A5678E15008542526BBFFF61BB33F13B024',
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
                   '27103A380CFAA7E3A8A8FB42B6B42E005F47',

                   ]
        data = {"tk": list_Id[number],
                "gt": gametype,
                "betScore": "3000",
                "timestamp": "15976259898985"
                }
        data1 = json.dumps({"tk": list_Id[number], "type": 1, "gold": 10000000,
                 "timestamp": "1600914417600"})

        data = json.dumps(data)
        log = ''
        try:
            post = requests.post(url, data=data, timeout=5)
            log = post.text
            print(gametype, log)
            post = post.json()
            code = post.get("code")

            if code == 20000:
                li = (post['et']['Data']['Points'])
                isFree = (post['et']['Data']['isFree'])
                RotaryBls = (post['et']['Data']['RotaryBls'])
                Type = (post['et']['Type'])
                print(li.count(12))
                # print(li, "红利判断", isFree)
                print(RotaryBls)

                for k in range(5):
                    print(f"第{k+1}次旋转")
                    while not isFree and Type != 1:
                       b += 1
                       if li[k] != 12 and li[k+5] != 12 and li[k+10] != 12:

                           data2 = json.dumps({"tk": list_Id[number],
                                               "gt": gametype,
                                               "betScore": "3000",
                                               "timestamp": 4645645,
                                               "RoteRow": k+1,
                                               'RoteKey': 'ddd',
                                               })
                           pi = requests.post(url2, data2, timeout=5)
                           # print(pi.request.body)
                           log1=json.loads(pi.text)
                           code1 = log1.get("code")
                           if code1 == 20000:

                               li = (log1['et']['Data']['Points'])
                               isFree = (log1['et']['Data']['isFree'])
                               RotaryBl = (log1['et']['Data']['RotaryBls'])
                               print(li)
                               gold = (log1['et']['Gold']) / 100
                               Ngold = (log1['et']['NGold']) / 100
                               # print(gold)
                               print(f'{number}号玩家--{b}局{k+1}轴旋转=', Ngold, 'win', gold)
                               # k = RotaryBl.index(min(RotaryBl))

                           # elif code1 == 20017:
                           #     po  = requests.post(url1, data=data1, timeout=5)
                           #     print(po.text)

                           else:
                                print(log1)
                       else:
                           print(f'第{k+1}轴已经有12了，下一列开始旋转')
                           break
                print("进入红利了")

                # li = (line[0]['Points'])
                for i in range(5):
                    if li[i] != li[i+5] != li[i+10] != li[i]:
                        x = 3
                    else:
                        print(f"第{i+1}轴错误了，刘wei遭起")
                        wirte(log)
                        print(log)
                        input('凉凉')
                    if i == 1 or i == 3:
                        continue
                    # print('此时的i=', i)
                    if li[i] == 13 or li[i+5] == 13 or li[i+10] == 13:
                        print(li[i], li[i+5], li[i+10])
                        print(f"{i+1}列出现多个百搭")
                        # print(log)
                        wirte(log)
                        input("是否继续请输入")
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
                # print("有锁")
                threadLock.release()  # 释放锁
                # print("释放成功")
            else:
                pass


if __name__ == '__main__':

    list_o = [130, 131, 132, 133, 134, 135]
    for i in range(1):
        ga = list_o[(i % 6)]
        # print(ga)
        threading.Thread(target=ceshi, args=(i, ga)).start()