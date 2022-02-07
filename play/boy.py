import operator
from functools import reduce
import json
import random
import requests
import threading
import time, copy

# global url, HL_url
url = "http://192.168.10.25:8001//api/UserCore/CallLotteryModel"
HL_url = "http://192.168.10.25:8001//api/UserCore/CallLotteryFree"

threadLock = threading.Lock()


def Add_gold(tk, type=1):
    url = "http://192.168.10.25:8001/api/UserCore/AddPlayerGold"
    data = {"tk": tk, "type": type, "gold": 1000000, "timestamp": "1600914417600"}
    po = requests.post(url, json=data, timeout=5)
    print('改变筹码。。。', po.text)


# Add_gold('2BE7319031958CBFB94C04770B7BE7B8C138', 1)


def checkNgold(response, betScore):  # 核对Ngold
    award_dic = {
        (13, 2): 1,
        (1, 3): 5,
        (2, 3): 5,
        (3, 3): 7,
        (4, 3): 7,
        (5, 3): 10,
        (6, 3): 10,
        (7, 3): 15,
        (8, 3): 15,
        (9, 3): 20,
        (10, 3): 20,
        (11, 3): 30,
        (12, 3): 30,
        (13, 3): 2,
        (14, 3): 100,
        (1, 4): 15,
        (2, 4): 15,
        (3, 4): 20,
        (4, 4): 20,
        (5, 4): 25,
        (6, 4): 25,
        (7, 4): 60,
        (8, 4): 60,
        (9, 4): 80,
        (10, 4): 80,
        (11, 4): 100,
        (12, 4): 100,
        (13, 4): 20,
        (14, 4): 250,
        (1, 5): 100,
        (2, 5): 100,
        (3, 5): 125,
        (4, 5): 125,
        (5, 5): 150,
        (6, 5): 150,
        (7, 5): 250,
        (8, 5): 300,
        (9, 5): 350,
        (10, 5): 400,
        (11, 5): 450,
        (12, 5): 500,
        (13, 5): 200,
        (14, 5): 1500
    }
    awardlins = response['et']['Data']['AwardLins']
    MuitNumber = response.get('et').get('Data').get('MuitNumber')
    if MuitNumber is None:
        MuitNumber = 1
    print(MuitNumber)
    Points = response['et']['Data']['Points']
    AdPoints = response['et']['Data']['AdPoints']
    LinePoints = response['et']['Data']['LinePoints']
    SpecIndex = response.get('et').get('Data').get('SpecIndex')
    if not checkLinePoints(AdPoints, LinePoints):
        return False
    gold = 0
    if len(awardlins) > 0:
        for key, value in awardlins.items():  # 遍历中奖符号
            if key == '13':  # 出现散布图
                playgold = (award_dic[(int(key), value)] * betScore)   # 直接乘投注的倍数
                for i in LinePoints[key]:
                    if SpecIndex in i:
                        playgold = playgold * MuitNumber
                    else:
                        pass
                print(playgold)
                gold += playgold

            else:
                for i in LinePoints[key]:
                    if [Points[X] for X in i].count(14) > 0:  # 如果包含百搭 翻倍
                        playgold = award_dic[(int(key), len(i))] * 200 * betScore/3000

                    else:
                        playgold = award_dic[(int(key), len(i))] * 100 * betScore/3000

                    if SpecIndex in i:
                        playgold = playgold * MuitNumber

                    print('不是散步', playgold)
                    gold += playgold
        print(gold)
    if gold != response['et']['Gold']:
        with open('cuowu.txt', 'r') as f:
            print('出错了')
            f.write('\n'+'金币错误')
            f.write(json.load(response))

def checkLinePoints(adpoints, linepoints):  # 核对LinePoints
    myadpoints = copy.deepcopy(adpoints)  # 拷贝一个 myadpoints 避免后续直接修改adpoints对象
    for key, value in myadpoints.items():
        if key != '13':
            col1, col2, col3, col4, col5 = [], [], [], [], []
            for i in value:
                if i % 5 == 0:
                    col1.append(i)
                elif i % 5 == 1:
                    col2.append(i)
                elif i % 5 == 2:
                    col3.append(i)
                elif i % 5 == 3:
                    col4.append(i)
                elif i % 5 == 4:
                    col5.append(i)
            # print("col",col1,col2,col3,col4,col5)
            if len(col5) > 0:
                mylinepoints = [[a, b, c, d, e] for a in col1 for b in col2 for c in col3 for d in col4 for e in col5]
            elif len(col4) > 0:
                mylinepoints = [[a, b, c, d] for a in col1 for b in col2 for c in col3 for d in col4]
                print(mylinepoints)
            elif len(col3) > 0:
                mylinepoints = [[a, b, c] for a in col1 for b in col2 for c in col3]
                print(mylinepoints)
            elif len(col2) > 0:
                mylinepoints = [[a, b] for a in col1 for b in col2]
                print(mylinepoints)
            else:
                mylinepoints = []
            print(mylinepoints)
            print(linepoints[key])
            if sorted(mylinepoints) != sorted(linepoints[key]):
                print("linepoints有误", sorted(mylinepoints), sorted(linepoints[key]))
                return False
        else:
            if key in linepoints:
                print("linepoints有误包含符号13")
                return False
    return True

def getColsSymbol(points):  # 取出各列中奖位置
    symbol12_list = []
    col1, col2, col3, col4, col5 = {}, {}, {}, {}, {}
    for i in range(len(points)):
        if points[i] == 12:
            symbol12_list.append(i)
        elif i % 5 == 0:
            col1[i] = points[i]
        elif i % 5 == 1:
            col2[i] = points[i]
        elif i % 5 == 2:
            col3[i] = points[i]
        elif i % 5 == 3:
            col4[i] = points[i]
        elif i % 5 == 4:
            col5[i] = points[i]
    return col1, col2, col3, col4, col5, symbol12_list

def checkAwardSymbol(response):  # 核对adpoints
    points = response['et']['Data']['Points']
    col1, col2, col3, col4, col5, symbol12_list = getColsSymbol(points)
    adpoints = {}
    for col1_key, col1_value in col1.items():
        if col1_value not in adpoints.keys():  # 字典里没有该符号
            for col2_key, col2_value in col2.items():
                if col1_value == col2_value or col2_value == 13:
                    for col3_key, col3_value in col3.items():
                        if col1_value == col3_value:
                            try:
                                adpoints[col1_value].append(col1_key)
                            except:
                                adpoints[col1_value] = [col1_key]
                            adpoints[col1_value].append(col2_key)
                            adpoints[col1_value].append(col3_key)
                        elif col1_value in (10, 11):
                            try:
                                adpoints[col1_value].append(col1_key)
                            except:
                                adpoints[col1_value] = [col1_key]
                            adpoints[col1_value].append(col2_key)
        else:
            adpoints[col1_value].append(col1_key)
    for key, value in adpoints.items():
        if 2 in value or 7 in value or 12 in value:  # 这
            for col4_key, col4_value in col4.items():
                if key == col4_value or col4_value == 13:
                    # print("加入",col4_value)
                    adpoints[key].append(col4_key)
                    for col5_key, col5_value in col5.items():
                        if key == col5_value:
                            # print("加入", col5_value)
                            adpoints[key].append(col5_key)
    for key, value in adpoints.items():
        adpoints[key] = list(set(value))
    if len(symbol12_list) >= 2:
        adpoints[12] = symbol12_list
    my_adpoints = {}
    for key, value in adpoints.items():
        my_adpoints[str(key)] = value
    for key in my_adpoints.keys():
        if sorted(my_adpoints[key]) != sorted(response['et']['Data']['AdPoints'].get(key, [])):
            print("中奖点有误", my_adpoints, response)
            return False
    for key in response['et']['Data']['AdPoints'].keys():
        if sorted(my_adpoints[key]) != sorted(response['et']['Data']['AdPoints'].get(key, [])):
            print("中奖点有误", my_adpoints, response)
            return False
    return True


def ceshi(number):
    winning = []
    global tj
    print("第%s个线程开始运行" % number)
    c = 0


    for b in range(2000000):
        # file2 = open(r'E:\金流\数组\统计%s.csv' % number, 'a')
        times = time.asctime()
        nun = 2
        # nun = random.randint(1, 4)
        # if nun == 3:
        #     nun = random.randint(1, 2)
            # print(nun)
        '''liue351 - liue363(||362)'''
        list_Id = ['38F6112BC230DB14121E170C7B7804F7CA3E', '3828711C4353A737792BAF7BD06EE93F7C66', '53B222F5AEEC7671DDDDEE2BE09253DAC8CE', 'EF51C6643384A024915589A039F53664F0E4', '7B5C6B540F01CE8984579F11F2FB1AF7C088', 'FD3998A4E61BDFD26B859AB16DF0E009E302', 'E91A31B86A6CF20381E97D23D3A31189625F', 'EACA25321E79F4AA6A01374414B49456E99C', '700529AA38DD9BB4B0190856B5EAF4EB8F4A', '1AED0EE98AD4155222DF3766AE909E051C32', '68D10518B566C40C99C8C2025F261A40012E', 'FC1D15163485300795499743A9793458B760', '189A3B516B4CE8CD3463599E1E1C01F0621D', 'A51CCA91C9BFBA4C6D629D815CF0EC198027', 'F3EBB0C9F79C22A4F9BD106F1E9EFB680AAE', 'DA6C09C16D300E4D19C2E07226804E8BA700', 'E1E09749EDD925D290E4FD8EB7E8A9283B2D', 'DD6C620C2E34C7CD61DEBEA9ABAFD6AC545F', 'F8796E9F187ED6FB3F9FA5C323621E5BFB95', '77D8636D37F6C61EFA8F59CFC217BEDEB9CC', '5D8D5117ED6E29453950152AFDBCB0675479', '8C2F1E14A9A373DA4EF5D48526342B16B62C', 'BA889F7DDA9EEABA8F78FD113F1A9D159503', '43D2086576665F79DCF28746A736C475CD85', 'BCF0579533CACBDEF5A81BE959062F93DEB4', '659CB6F2B4066B902D3EED9D4130D69F0938', '57238B0246932EAB5254E2C8CE518AE11C0D', 'DD3DBD8A7F7983E7FEC32BBC90705C516956', 'BED30D50A98EFC185CC3B8C1C03B4150A496', '59C74B5504AC43F3FA595B9EA40C2D72CC10', '86C007A86E559AD99D7E2CA7263A2E0D4C3B', '9A5678E15008542526BBFFF61BB33F13B024', '268B62F56B0F78D6C511C1356CC0DFC7C4E3', 'EF564D5DF8BAC1B627A427E19A8B49038FB5', '704B71B00C361B4E16567CF983372D9FBBE3', '8ADA6E18641C9CF858732DD36DBDD899A7CC', '91042905F54E21BF9965C2BB4244C929D8FD', '4F50BFB370ED44FEA0FFA20957B6E5E6E86E', '25F260976373F10C10244B9529356B939E33', 'B43C241FF49884ECEF3A7D938930AEC60152', '605D15895432BC60CAF2B6EFB6D3D55B9E15', '534479D912937AA4DB19785B5CD957AE9A90']

        data = {"tk": list_Id[number],
                "gt": "125",
                "betScore": "3000",
                "timestamp": "15976259898985"
                }
        data1 = {"tk": list_Id[number],
                 "gt": "125",
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
            Points = post['et']['Data']['Points']

            if code == 20000:
                type = post['et']['Type']
                if type == nun and post['et']['Gold'] != 0:
                    print(f'红利{nun}--局数{b}---', post)
                    checkNgold(post, 3000)

                if Points.count(14) > 2:
                    lis = getColsSymbol(Points)
                    for it in range(5):
                        ca = list(lis[it].values())
                        if ca[0]==14 and ca[1]==14 and ca[2]==14:
                            print(f'模式{type}出现WILD了', post)
                            checkAwardSymbol(post)
                            checkNgold(post, 3000)









                # print(post.text)
                # threadLock.acquire()  #加互斥锁
                # print(threading.current_thread())  #查看那个线程中奖了
                # print(b)
                et = post.get("et")
                Data = et.get('Data')
                # print(Data)
                AdPoints = Data.get('AdPoints')
                ApiPoints = Data.get('ApiPoints')
                # print(AdPoints)
                # print(ApiPoints)
                Ap = reduce(operator.add, ApiPoints)

                for key, nume in AdPoints.items():
                    # print(key)
                    winning.append(int(key))
                # print(winning)

                Points = Data.get("Points")
                # file2 .write(str(Points)+",,,"+str(Ap)+','+'\n')
                # file2.close()
                # print("写完关闭", number)
                # threadLock.release ()  # 释放锁
                # print(Points.count(13))

                if Points.count(13) > 2:
                    po = requests.post(HL_url, data=data1)
                    po.json()
                    # print(po.text)
                    print('进入第%s次红利' % c, number)
                    c += 1
                else:
                    pass
            if code == 20017:
                print(post)
                Add_gold(list_Id[number])


            lens = len(winning)
            if lens > 10 and lens % 50000 == 0 or b > 199998:
                # threadLock.acquire()  # 加互斥锁
                file = open(r'E:\金流\统计%s.csv' % number, 'a')
                file.write(str(times) + ',' + "开奖点" + ',' + "次数" + ',' + "\n")
                for x in range(1, 15):
                    tj = (winning.count(x))
                    # print(tj)
                    file.write("开奖点" + ',' + str(x) + "," + str(tj) + "," + "红利" + ',' + str(c) + ',' "\n")
                file.close()
                print("打印列表", number)
                # threadLock.release()  # 释放锁
                pass
            elif lens > 1000000:
                # file2.close()
                print("跳出循环", number)
                break

        except Exception as e:
            print(repr(e))
            print(e.__traceback__.tb_lineno)
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

    for i in range(40):
        print(i)
        threading.Thread(target=ceshi, args=(i,)).start()
