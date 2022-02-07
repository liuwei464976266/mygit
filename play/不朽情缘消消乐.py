#encoding:utf-8
import requests, json, threading, time, random,datetime
import operator
from functools import reduce
from queue import Queue
import copy
def checkLinePoints(adpoints,linepoints):#核对LinePoints
    myadpoints = copy.deepcopy(adpoints)#拷贝一个 myadpoints 避免后续直接修改adpoints对象
    for key,value in myadpoints.items():
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
                mylinepoints = [[a,b,c,d,e] for a in col1 for b in col2 for c in col3 for d in col4 for e in col5]
            elif len(col4) > 0:
                mylinepoints = [[a, b, c, d] for a in col1 for b in col2 for c in col3 for d in col4]
            elif len(col3) > 0:
                mylinepoints = [[a, b, c] for a in col1 for b in col2 for c in col3]
            else:
                mylinepoints = []
            if sorted(mylinepoints) != sorted(linepoints[key]):
                print("linepoints有误",sorted(mylinepoints),sorted(linepoints[key]))
                return False
        else:
            if key in linepoints:
                print("linepoints有误包含符号13")
                return False
    return True
def getCurrentGold(Rpoints,type):
    pass
def checkNgold(response,betScore,lastNgold):#核对Ngold
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
    if response['et']['Type'] == 3:  # 判断是否是红利场
        Rpoints = response['et']['Data']['Rpoints']
        if len(Rpoints) > 1:#如果有中奖
            paygold = 0
            for rpointIndex in range(len(Rpoints)):
                if rpointIndex + 1 <= 5:#如果是1-4次掉落中奖
                    hl_num = rpointIndex + 1
                else:
                    hl_num = 5
                awardlins = Rpoints[rpointIndex]['AwardLins']
                Points = Rpoints[rpointIndex]['Points']
                AdPoints = Rpoints[rpointIndex]['AdPoints']
                LinePoints = Rpoints[rpointIndex]['LinePoints']
                if not checkLinePoints(AdPoints,LinePoints):
                    return False
                for key, value in awardlins.items():  # 遍历中奖符号
                    if key == '13':  # 出现散布图
                        paygold = paygold + (award_dic[(int(key), value)] * betScore) * hl_num  # 直接乘投注的倍数
                    else:
                        for i in LinePoints[key]:
                            if [Points[X] for X in i].count(14) > 0:#如果包含百搭 翻倍
                                paygold = paygold + award_dic[(int(key), len(i))] * (betScore / 30) * hl_num * 2
                            else:
                                paygold = paygold + award_dic[(int(key), len(i))] * (betScore / 30) * hl_num
            current_gold = int(lastNgold + paygold)  # 计算出current——gold
        else:
            current_gold = lastNgold
    elif response['et']['Type'] == 0:
        Rpoints = response['et']['Data']
        AdPoints = Rpoints['AdPoints']
        LinePoints = Rpoints['LinePoints']
        if len(Rpoints['AwardLins']) > 0:  # 如果有中奖
            paygold = 0
            hl_num = 1
            awardlins = Rpoints['AwardLins']
            Points = Rpoints['Points']
            if not checkLinePoints(AdPoints, LinePoints):
                return False
            for key, value in awardlins.items():  # 遍历中奖符号
                if key == '13':  # 出现散布图
                    paygold = paygold + (award_dic[(int(key), value)] * betScore) * hl_num  # 直接乘投注的倍数
                    # print(paygold)
                else:
                    for i in LinePoints[key]:
                        if [Points[X] for X in i].count(14) > 0:
                            paygold = paygold + award_dic[(int(key), len(i))] * (betScore / 30) * hl_num * 2
                        else:
                            paygold = paygold + award_dic[(int(key), len(i))] * (betScore / 30) * hl_num
            current_gold = int(lastNgold + paygold - betScore) # 计算出current——gold
        else:
            current_gold = int(lastNgold - betScore)
    if current_gold != response['et']['NGold']:
        print('筹码错误',paygold,current_gold,response['et']['NGold'])
        return False
    return current_gold
def checkLotteryInitialize(tk,gametype,lastresponse):#核对断线重连初始化
    while True:
        url = "http://192.168.10.25:8001//api/UserCore/CallLotteryInitialize"
        millis = int(round(time.time() * 1000))
        data = {"tk":tk,
                "gt":gametype,
                "timestamp":millis
                }
        data = json.dumps(data)
        response = requests.post(url = url, data = data)
        response = response.json()
        if response['code'] == 20000:
            break
    print(response['et']['Data']['LastData'])
    print(lastresponse['et']['Data'])
    if response['et']['Data']['LastData'] != lastresponse['et']['Data']:
        print("response['et']['Data']['LastData']",response['et']['Data']['LastData'],"lastresponse['et']['Data']",lastresponse['et']['Data'])
        return False
    return True
def getColsSymbol(points):#取出各列中奖位置
    symbol13_list = []
    col1, col2, col3, col4, col5 = {}, {}, {}, {}, {}
    for i in range(len(points)):
        if points[i] == 13:
            symbol13_list.append(i)
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
    return col1,col2,col3,col4,col5,symbol13_list
def checkAwardSymbol(rpoints):#核对adpoints
    points = rpoints['Points']
    col1, col2, col3, col4, col5, symbol13_list = getColsSymbol(points)
    adpoints = {}
    for col1_key, col1_value in col1.items():
        if col1_value not in adpoints.keys():  # 字典里没有该符号
            if col1_value != 14:
                for col2_key, col2_value in col2.items():
                    if col1_value == col2_value or col2_value == 14:
                        for col3_key, col3_value in col3.items():
                            if col1_value == col3_value or col3_value == 14:
                                try:
                                    adpoints[col1_value].append(col1_key)
                                except:
                                    adpoints[col1_value] = [col1_key]
                                adpoints[col1_value].append(col2_key)
                                adpoints[col1_value].append(col3_key)
            else:
                for col2_key, col2_value in col2.items():
                    if col1_value == col2_value:
                        for col3_key, col3_value in col3.items():
                            try:
                                adpoints[col3_value].append(col1_key)
                            except:
                                adpoints[col3_value] = [col1_key]
                            adpoints[col3_value].append(col2_key)
                            adpoints[col3_value].append(col3_key)
                    else:
                        for col3_key, col3_value in col3.items():
                            if col2_value == col3_value or col3_value == 14:
                                try:
                                    adpoints[col2_value].append(col1_key)
                                except:
                                    adpoints[col2_value] = [col1_key]
                                adpoints[col2_value].append(col2_key)
                                adpoints[col2_value].append(col3_key)
        else:
            if col1_value != 14:
                adpoints[col1_value].append(col1_key)
    for key, value in adpoints.items():
        if 2 in value or 7 in value or 12 in value:
            for col4_key, col4_value in col4.items():
                if key == col4_value or col4_value == 14:
                    adpoints[key].append(col4_key)
                    for col5_key, col5_value in col5.items():
                        if key == col5_value or col5_value == 14:
                            adpoints[key].append(col5_key)
    for key, value in adpoints.items():
        adpoints[key] = list(set(value))
    if len(symbol13_list) >= 2:
        adpoints[13] = symbol13_list
    my_adpoints = {}
    for key, value in adpoints.items():
        my_adpoints[str(key)] = value
    # print("my_adpoints",my_adpoints,"rpoints['AdPoints']",rpoints['AdPoints'])
    # print('my_adpoints',my_adpoints,"rpoints['AdPoints']",rpoints['AdPoints'])
    for key in my_adpoints.keys():
        if sorted(my_adpoints[key]) != sorted(rpoints['AdPoints'].get(key,[])):
            print("+++++++++++++++++++++++++++++++", my_adpoints)
            return False
    for key in rpoints['AdPoints'].keys():
        if sorted(my_adpoints[key]) != sorted(rpoints['AdPoints'].get(key,[])):
            print("+++++++++++++++++++++++++++++++", my_adpoints)
            return False
    return True
def checkAdpoints(response):#核对points
    # print(type(response['et']['Data']['Rpoints']))
    for rpoints in response['et']['Data']['Rpoints']:
        if not checkAwardSymbol(rpoints):
            return False
        # print(rpoints)
        points = copy.deepcopy(rpoints['Points'])
        adPoints = rpoints['AdPoints']
        if 'myPoints' not in dir():  # myPoints变量未定义
            myPoints = []
            for Symbols in points:
                myPoints.append(Symbols)
            # print(myPoints,"=",points)
        if len(myPoints) != 15 or len(points) != 15:
            print(myPoints,rpoints['Points'])
            print("个数不正确")
            return False
        # print("myPoints", myPoints)
        # print("points", points)
        for i in range(len(myPoints)):
            if myPoints[i] != 'randomSymbol' and myPoints[i] != points[i]:
                print("结果错误","myPoints", myPoints,"points", points)
                return False
        # print(rpoints)
        myPoints = points
        award_index_list = []
        for index_list in adPoints.values():
            award_index_list = award_index_list + index_list
        award_index_list = list(set(award_index_list))#中奖下标列表去重
        award_index_list = sorted(award_index_list)#中奖下标列表排序
        for award_index in award_index_list:
            if award_index < 5:
                myPoints[award_index] = "randomSymbol"#如果第一行有中奖，该位置为随机符号
            elif 5 <= award_index < 10 :
                if myPoints[award_index - 5] == "randomSymbol":#如果第一行有随机符号
                    myPoints[award_index] = "randomSymbol"#第二行该位置为随机符号
                else:#如果第一列不为随机符号
                    myPoints[award_index] = myPoints[award_index - 5]#该位置为第一行符号
                    myPoints[award_index - 5] = "randomSymbol"#第一行为随机符号
            elif 10 <= award_index <= 14 :
                if myPoints[award_index - 5] == "randomSymbol":#如果第二行为随机符号，
                    myPoints[award_index] = "randomSymbol"#第三行该位置为随机符号
                else:#如果第二列不为随机符号
                    myPoints[award_index] = myPoints[award_index - 5]#第三行为第二行符号
                    myPoints[award_index - 5] = myPoints[award_index - 10]#第二行为第一行符号
                    myPoints[award_index - 10] = "randomSymbol"#第一行为随机符号
    return True
def normalPlay(tokenid,gametype):#正常玩模式
    url = "http://192.168.10.25:8001//api/UserCore/CallLotteryModel"
    millis = int(round(time.time() * 1000))
    data = {
        "tk": tokenid,
        "gt": gametype,
        "timestamp": millis,
        "betScore": 30
    }
    data = json.dumps(data)
    try:
        response = requests.post(url, data=data)
        response = response.json()
        if response.get("code") == 20000:
            # print(response)
            return response
        else:
            print(response)
    except:
        pass
    return None
def freeSpin4(tokenid,gametype):#选择红利4
    while True:
        url = "http://192.168.10.25:8001//api/UserCore/CallLotteryFree"
        millis = int(round(time.time() * 1000))
        data = {
            "tk": tokenid,
            "gt": gametype,
            "timestamp": millis,
            "type":"3"
        }
        data = json.dumps(data)
        try:
            response = requests.post(url, data=data)
            response = response.json()
            if response.get("code") == 20000:
                break
        except:
            pass
def main():#主函数 程序入口
    while True:
        # tokenid = "A9FB9B30752B679D174F70E08941782F89D4"
        tokenid = "25E1A6E1E01EF4A24BF947284880FC31CE23"
        gameType = 125
        response = normalPlay(tokenid = tokenid,gametype= gameType)
        print(response)
        if response:
            if 'lastNgold' not in dir():  # 如果是第一次运行脚本
                lastNgold = response['et']['NGold']
                if response['et']['Data'].get('isFree', False):
                    freeSpin4(tokenid,gametype = gameType)
                elif response['et']['Type'] == 3:
                    if not checkAdpoints(response):
                        break
            else:
            # if not checkLotteryInitialize(tk=tokenid, gametype=gameType,lastresponse = response):#核对断线重连初始化
            #     break
                if response['et']['Data'].get('isFree',False):
                    freeSpin4(tokenid,gametype = gameType)
                elif response['et']['Type'] == 3:
                    if not checkAdpoints(response):
                        break
                lastNgold = checkNgold(response,30,lastNgold)
                if lastNgold == False:
                    break

if __name__ == '__main__':
    main()

