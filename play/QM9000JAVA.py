# encoding:utf-8
import requests, json, threading, time, random, datetime, re, string
import operator
from functools import reduce
from queue import Queue
import logAnalysisUtil
import copy
import random

ZR_AWARD_DIC = {
    (10, 2): 7,
    (11, 2): 12,
    (12, 2): 1,
    (1, 3): 2,
    (2, 3): 2,
    (3, 3): 5,
    (4, 3): 5,
    (5, 3): 8,
    (6, 3): 8,
    (7, 3): 10,
    (8, 3): 12,
    (9, 3): 15,
    (10, 3): 20,
    (11, 3): 30,
    (12, 3): 2,
    (1, 4): 15,
    (2, 4): 15,
    (3, 4): 20,
    (4, 4): 20,
    (5, 4): 30,
    (6, 4): 30,
    (7, 4): 100,
    (8, 4): 125,
    (9, 4): 150,
    (10, 4): 200,
    (11, 4): 300,
    (12, 4): 10,
    (1, 5): 100,
    (2, 5): 100,
    (3, 5): 150,
    (4, 5): 150,
    (5, 5): 200,
    (6, 5): 200,
    (7, 5): 500,
    (8, 5): 750,
    (9, 5): 1500,
    (10, 5): 2000,
    (11, 5): 3000,
    (12, 5): 100
    }
DF_AWARD_DIC = {
    (10, 2): 5,
    (11, 2): 10,
    (12, 2): 1,
    (1, 3): 2,
    (2, 3): 2,
    (3, 3): 4,
    (4, 3): 4,
    (5, 3): 5,
    (6, 3): 5,
    (7, 3): 10,
    (8, 3): 15,
    (9, 3): 20,
    (10, 3): 25,
    (11, 3): 40,
    (12, 3): 2,
    (1, 4): 12,
    (2, 4): 12,
    (3, 4): 20,
    (4, 4): 20,
    (5, 4): 30,
    (6, 4): 30,
    (7, 4): 100,
    (8, 4): 150,
    (9, 4): 200,
    (10, 4): 250,
    (11, 4): 400,
    (12, 4): 10,
    (1, 5): 100,
    (2, 5): 100,
    (3, 5): 150,
    (4, 5): 150,
    (5, 5): 200,
    (6, 5): 200,
    (7, 5): 500,
    (8, 5): 1000,
    (9, 5): 2000,
    (10, 5): 2500,
    (11, 5): 4000,
    (12, 5): 100
    }
TW_AWARD_DIC = {
    (9, 2): 1,
    (1, 3): 5,
    (2, 3): 6,
    (3, 3): 8,
    (4, 3): 10,
    (5, 3): 20,
    (6, 3): 25,
    (7, 3): 30,
    (8, 3): 40,
    (9, 3): 2,
    (10, 3): 125,
    (11, 3): 2,
    (12, 3): 10,
    (13, 3): 15,
    (14, 3): 20,
    (15, 3): 25,
    (16, 3): 70,
    (1, 4): 10,
    (2, 4): 12,
    (3, 4): 15,
    (4, 4): 20,
    (5, 4): 50,
    (6, 4): 60,
    (7, 4): 80,
    (8, 4): 100,
    (9, 4): 10,
    (10, 4): 300,
    (1, 5): 70,
    (2, 5): 80,
    (3, 5): 90,
    (4, 5): 100,
    (5, 5): 150,
    (6, 5): 175,
    (7, 5): 200,
    (8, 5): 250,
    (9, 5): 100,
    (10, 5): 750,

    }
GT = 143
WILD = [10]
WILD_STR = ['10']
MAXPAYGOLD = 8320000
betScore = 30
session = requests.session()
SCATTER = '9'
BASEBET = 30
exchange = 'http://192.168.10.213:9002/api/Service/ExchangeInOrOut'
LOGINUIR = "http://192.168.10.213:9002/user/register"
INITURL = "http://192.168.10.213:9008/callInitialize"
GETSLOTURL = "http://192.168.10.213:9008/getSlotData"
REGISTER = "http://192.168.10.213:9000/registerUser"
DFAWARDGT = [130, 131, 132, 133, 136]
ZRAWARDGT = [134, 135]
TWAWARDGT = [143]


def filterAdpoints(adpoints, points):
    filtedAdpoints = {}
    myadpoints = copy.deepcopy(adpoints)  # 拷贝一个 myadpoints 避免后续直接修改adpoints对象
    myDicAdpoints = {}
    for key, value in myadpoints.items():
        # if key != SCATTER and key != '11':
        if key != '11':
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
            if len(col5) > 0:
                mylinepoints = [[a, b, c, d, e] for a in col1 for b in col2 for c in col3 for d in col4 for e in col5]
            elif len(col4) > 0:
                mylinepoints = [[a, b, c, d] for a in col1 for b in col2 for c in col3 for d in col4]
            elif len(col3) > 0:
                mylinepoints = [[a, b, c] for a in col1 for b in col2 for c in col3]
            elif len(col2) > 0:
                mylinepoints = [[a, b] for a in col1 for b in col2]
            else:
                mylinepoints = []
            removeLines = []
            for i in mylinepoints:
                if len([x for x in i if points[x] not in WILD]) <= 0 and key not in WILD_STR:
                    removeLines.append(i)
            for i in removeLines:
                mylinepoints.remove(i)
            myListAdpoints = []
            for i in mylinepoints:
                myListAdpoints += i
            myListAdpoints = list(set(myListAdpoints))
            myDicAdpoints[key] = myListAdpoints
        elif key == SCATTER:
            myDicAdpoints[SCATTER] = value
        elif key == '11':
            myDicAdpoints['11'] = value
    return myDicAdpoints


def checklinePoints(adpoints, linepoints, points):  # 核对LinePoints
    myadpoints = copy.deepcopy(adpoints)  # 拷贝一个 myadpoints 避免后续直接修改adpoints对象
    for key, value in myadpoints.items():
        if key != '11':
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
            # print(f'key={key}---D1={col1},D2={col2},D3={col3},D4={col4},D5={col5}')
            if len(col5) > 0:
                mylinepoints = [[a, b, c, d, e] for a in col1 for b in col2 for c in col3 for d in col4 for e in col5]
            elif len(col4) > 0:
                mylinepoints = [[a, b, c, d] for a in col1 for b in col2 for c in col3 for d in col4]
            elif len(col3) > 0:
                mylinepoints = [[a, b, c] for a in col1 for b in col2 for c in col3]
            elif len(col2) > 0:
                mylinepoints = [[a, b] for a in col1 for b in col2]
            else:
                mylinepoints = []
            removeLines = []
            for i in mylinepoints:
                if len([x for x in i if points[x] not in WILD]) <= 0 and key not in WILD_STR:
                    removeLines.append(i)
            for i in removeLines:
                mylinepoints.remove(i)
            # print(mylinepoints, linepoints)
            if sorted(mylinepoints) != sorted(linepoints[key]) and key != '11' and key != SCATTER:
                print("linepoints有误333", key, sorted(mylinepoints), sorted(linepoints[key]))
                return False
        else:
            if key in linepoints and key != SCATTER and key != '11':
                print(f"linepoints有误222包含符号{SCATTER}")
                return False
    return True


def checkFsPoints(response, colNum, lastpoints):
    mypoints = copy.deepcopy(lastpoints)
    points = response['et']['data']['points']
    for i in range(len(mypoints)):
        if i % 5 == colNum - 1:
            mypoints[i] = "randomSymbol"
    if len(mypoints) == len(points):
        for i in range(len(mypoints)):
            if mypoints[i] != "randomSymbol" and mypoints[i] != points[i]:
                print("单轴旋转points错误", points, lastpoints)
                return False
    else:
        print("points长度错误", points, lastpoints)
        return False
    return points


def checknGold(response, betScore, lastnGold):  # 核对nGold
    if GT in ZRAWARDGT:
        AWARD_DIC = ZR_AWARD_DIC
    elif GT in DFAWARDGT:
        AWARD_DIC = DF_AWARD_DIC
    elif GT in TWAWARDGT:
        AWARD_DIC = TW_AWARD_DIC
    else:
        print("无此游戏")
        exit()
    awardlins = response['et']['data']['awardLines']
    points = response['et']['data']['points']
    adPoints = response['et']['data']['adPoints']
    linePoints = response['et']['data']['linePoints']
    if response['et']['type'] == 0:  # 判断是否是红利场
        paygold = -betScore  # 如果不是红利场，则底注为-底注
        hl_num = 1  # 红利倍数为1
    else:
        paygold = 0  # 如果是红利场，则底注为0
        hl_num = 3  # 红利倍数为3
    if not checklinePoints(adPoints, linePoints, points):
        print("linePoints有误444")
        return False
    if len(awardlins) > 0:
        for key, value in awardlins.items():  # 遍历中奖符号
            if key == SCATTER or key == '11':  # 出现散布图
                paygold = paygold + (AWARD_DIC[(int(key), value)] * betScore) * hl_num  # 直接乘投注的倍数
            elif key == '10':
                paygold = paygold + AWARD_DIC[(int(key), value)] * (betScore / 30) * hl_num
            elif key not in WILD_STR:
                for i in linePoints[key]:
                    # print(key, linePoints[key])
                    if [points[X] for X in i].count(10) > 0:  # 如果包含百搭 翻倍
                        # if hl_num == 3:
                        paygold = paygold + AWARD_DIC[(int(key), len(i))] * (betScore / 30) * hl_num * 3
                        # else:
                        #     paygold = paygold + AWARD_DIC[(int(key), len(i))] * (betScore / 30) * hl_num * 3
                    else:
                        paygold = paygold + AWARD_DIC[(int(key), len(i))] * (betScore / 30) * hl_num
            else:
                for i in linePoints[key]:
                    paygold = paygold + AWARD_DIC[(int(key), len(i))] * (betScore / BASEBET) * hl_num
    if response['et']['type'] == 0:  # 判断是否是红利场
        paygold = paygold + betScore  # 如果不是红利场，则+底注
    if paygold > MAXPAYGOLD:
        paygold = MAXPAYGOLD
    if response['et']['type'] == 0:  # 判断是否是红利场
        current_gold = int(lastnGold + paygold - betScore)# 计算出current——gold
    else:
        current_gold = int(lastnGold + paygold)  # 计算出current——gold
    print('结算校验', paygold, response['et']['gold'], current_gold, response['et']['nGold'])
    if response['et']['gold'] > MAXPAYGOLD:
        print("超出最大值")
        return False
    if paygold != response['et']['gold']:
        print('gold错1误', paygold, current_gold, response['et']['nGold'])
        return False
    if current_gold != response['et']['nGold']:
        print('1筹码错误', paygold, current_gold, response['et']['nGold'])
        return False
    return current_gold


def checkFsnGold(response, betScore, lastnGold, mybetScore):  # 核对nGold
    if GT in ZRAWARDGT:
        AWARD_DIC = ZR_AWARD_DIC
    elif GT in DFAWARDGT:
        AWARD_DIC = DF_AWARD_DIC
    else:
        print("无此游戏")
        exit()
    awardlins = response['et']['data']['awardLines']
    points = response['et']['data']['points']
    adPoints = response['et']['data']['adPoints']
    linePoints = response['et']['data']['linePoints']
    if response['et']['type'] == 0:  # 判断是否是红利场
        paygold = -betScore  # 如果不是红利场，则底注为-底注
        hl_num = 1  # 红利倍数为1
    else:
        paygold = 0  # 如果是红利场，则底注为0
        hl_num = 3  # 红利倍数为3
    if not checklinePoints(adPoints, linePoints, points):
        print("linepoints有误111")
        return False
    if len(awardlins) > 0:
        for key, value in awardlins.items():  # 遍历中奖符号
            if key == SCATTER:  # 出现散布图
                paygold = paygold + (AWARD_DIC[(int(key), value)] * mybetScore) * hl_num  # 直接乘投注的倍数
            else:
                for i in linePoints[key]:
                    paygold = paygold + AWARD_DIC[(int(key), len(i))] * (mybetScore / BASEBET) * hl_num
    current_gold = int(lastnGold + paygold)  # 计算出current——gold
    if response['et']['type'] == 0:  # 判断是否是红利场
        paygold = paygold + betScore  # 如果不是红利场，则+底注
    if paygold != response['et']['gold']:
        print('gold错误', paygold, current_gold, response['et']['nGold'])
        return False
    if current_gold != response['et']['nGold']:
        print('筹码错误', paygold, current_gold, response['et']['nGold'])
        return False
    return current_gold


def checkLotteryInitialize(tk, gametype, lastresponse):  # 核对断线重连初始化
    while True:
        url = INITURL
        data = {
            "gt": str(gametype),
            "timestamp": 45646545654,
            'actionType': '0',
            'tk': tk
            }
        headers = {
            'token': tk,
            'Content-Type': 'application/json'
            }
        data = json.dumps(data)
        response = requests.post(url=url, data=data, headers=headers)
        response = response.json()
        if response['code'] == 20000:
            break
    # print("断线重连",response)
    if response['et']['data']['lastData'] != lastresponse['et']['data']:
        print('断线重连有误', "response['et']['data']['lastData']", response['et']['data']['lastData'],
              "lastresponse['et']['data']", lastresponse['et']['data'])
        return False
    return True


def getColsSymbol(points):  # 取出各列中奖位置
    symbol12_list = []
    symbol11_list = []
    col1, col2, col3, col4, col5 = {}, {}, {}, {}, {}
    for i in range(len(points)):
        if points[i] == 9:
            symbol12_list.append(i)
        elif points[i] == 11:
            symbol11_list.append(i)
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
    return col1, col2, col3, col4, col5, symbol12_list, symbol11_list


def checkAwardSymbol(response):  # 核对adPoints
    rpoints = response['et']['data']
    points = rpoints['points']
    col1, col2, col3, col4, col5, symbol12_list, symbol11_list = getColsSymbol(points)
    list_col1 = [x for x in col1.values()]
    list_col2 = [x for x in col2.values()]
    list_col3 = [x for x in col3.values()]
    list_col4 = [x for x in col4.values()]
    list_col5 = [x for x in col5.values()]
    a = True
    for i in range(5):
        if points[i] == points[i + 5] or points[i] == points[i + 10] or points[i + 10] == points[i + 5]:
            print(f"出现重复元素{i}列")
            a = False
        if i < 2:
            if points[i] == 11 or points[i + 5] == 11 or points[i + 10] == 11:
                print('小游戏符号顺序错误')
                a = False
    if not a:
        exit(-9)
    adpoints = {}
    for col1_key, col1_value in col1.items():
        if col1_value not in adpoints.keys():  # 字典里没有该符号
            if col1_value not in WILD:
                for col2_key, col2_value in col2.items():
                    if col1_value == col2_value or col2_value in WILD:
                        for col3_key, col3_value in col3.items():
                            if col1_value == col3_value or col3_value in WILD:
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
                for col2_key, col2_value in col2.items():
                    if (col1_value == col2_value) or (col2_value in WILD):
                        for col3_key, col3_value in col3.items():
                            try:
                                adpoints[col3_value].append(col1_key)
                            except:
                                adpoints[col3_value] = [col1_key]
                            adpoints[col3_value].append(col2_key)
                            adpoints[col3_value].append(col3_key)
                    else:
                        for col3_key, col3_value in col3.items():
                            if (col2_value == col3_value) or (col3_value in WILD):
                                try:
                                    adpoints[col2_value].append(col1_key)
                                except:
                                    adpoints[col2_value] = [col1_key]
                                adpoints[col2_value].append(col2_key)
                                adpoints[col2_value].append(col3_key)
        else:
            if col1_value not in WILD:
                adpoints[col1_value].append(col1_key)
    temAdpoints = copy.deepcopy(adpoints)
    for key, value in temAdpoints.items():
        if 2 in value or 7 in value or 12 in value:
            for col4_key, col4_value in col4.items():
                if key == col4_value or col4_value in WILD:
                    adpoints[key].append(col4_key)
                for col5_key, col5_value in col5.items():
                    if key in WILD:
                        if col4_value in WILD and col5_value not in WILD:
                            try:
                                adpoints[col5_value].append(col5_key)
                            except:
                                adpoints[col5_value] = [col5_key]
                            adpoints[col5_value].append(col4_key)
                            adpoints[col5_value] += value
                        if (col4_value not in WILD) and (col5_value == col4_value or col5_value in WILD):
                            try:
                                adpoints[col4_value].append(col4_key)
                            except:
                                adpoints[col4_value] = [col4_key]
                            adpoints[col4_value].append(col5_key)
                            adpoints[col5_value] += value
                        if (col4_value not in WILD) and (col5_value != col4_value and col5_value not in WILD):
                            try:
                                adpoints[col4_value].append(col4_key)
                            except:
                                adpoints[col4_value] = [col4_key]
                            adpoints[col4_value] += value
                    if key == col4_value or col4_value in WILD:
                        adpoints[key].append(col4_key)
                        if key == col5_value or col5_value in WILD:
                            adpoints[key].append(col5_key)
    for key, value in adpoints.items():
        if len([x for x in adpoints[key] if x in col5.keys()]) > 0:
            for col1_key, col1_value in col1.items():
                if col1_value in WILD:
                    adpoints[key].append(col1_key)
            for col2_key, col2_value in col2.items():
                if col2_value in WILD:
                    adpoints[key].append(col2_key)
            for col3_key, col3_value in col3.items():
                if col3_value in WILD:
                    adpoints[key].append(col3_key)
            for col4_key, col4_value in col4.items():
                if col4_value in WILD:
                    adpoints[key].append(col4_key)
            for col5_key, col5_value in col5.items():
                if col5_value in WILD:
                    adpoints[key].append(col5_key)
        elif len([x for x in adpoints[key] if x in col4.keys()]) > 0:
            for col1_key, col1_value in col1.items():
                if col1_value in WILD:
                    adpoints[key].append(col1_key)
            for col2_key, col2_value in col2.items():
                if col2_value in WILD:
                    adpoints[key].append(col2_key)
            for col3_key, col3_value in col3.items():
                if col3_value in WILD:
                    adpoints[key].append(col3_key)
            for col4_key, col4_value in col4.items():
                if col4_value in WILD:
                    adpoints[key].append(col4_key)
        elif len([x for x in adpoints[key] if x in col3.keys()]) > 0:
            for col1_key, col1_value in col1.items():
                if col1_value in WILD:
                    adpoints[key].append(col1_key)
            for col2_key, col2_value in col2.items():
                if col2_value in WILD:
                    adpoints[key].append(col2_key)
            for col3_key, col3_value in col3.items():
                if col3_value in WILD:
                    adpoints[key].append(col3_key)
        adpoints[key] = list(set(value))
    popSymbols = []
    if len(symbol12_list) >= 2:
        adpoints[9] = symbol12_list
    if len(symbol11_list) >= 3:
        adpoints[11] = symbol11_list
    if 13 in adpoints.keys():
        if len(adpoints[13]) < 3:
            popSymbols.append(13)
    for popSymbol in popSymbols:
        adpoints.pop(popSymbol)
    my_adpoints = {}
    for key, value in adpoints.items():
        my_adpoints[str(key)] = value
    # print(my_adpoints,'one')
    my_adpoints = filterAdpoints(my_adpoints, points)
    # print("my_adpoints",my_adpoints,"rpoints['adPoints']",rpoints['adPoints'])
    # print(my_adpoints,'two')
    for key in my_adpoints.keys():
        if sorted(my_adpoints[key]) != sorted(rpoints['adPoints'].get(key, [])) and key != SCATTER:
            print("adpoints有误222")
            print(key, 'my_adpoints', sorted(my_adpoints[key]), 'adpoints', sorted(rpoints['adPoints'].get(key, [])))
            return False
    print('222', rpoints['adPoints'])
    # for key in rpoints['adPoints'].keys():
    #     print(sorted(my_adpoints[key]), '计算的')
    #     print(sorted(rpoints['adPoints'].get(key, [])), '取系统的')
    #     if key == SCATTER:
    #         continue
    #     if sorted(my_adpoints[key]) != sorted(rpoints['adPoints'].get(key, [])):
    #         print("adpoints有误111")
    #         print(key, 'my_adpoints', sorted(my_adpoints[key]), 'adpoints', sorted(rpoints['adPoints'].get(key, [])))
    #         return False
    return True


def checkFsAwardSymbol(response, colNum):  # 核对adPoints
    points = response['et']['data']['points']
    col1, col2, col3, col4, col5, symbol12_list = getColsSymbol(points)
    list_col1 = [x for x in col1.values()]
    list_col2 = [x for x in col2.values()]
    list_col3 = [x for x in col3.values()]
    list_col4 = [x for x in col4.values()]
    list_col5 = [x for x in col5.values()]
    a = True
    for i in range(5):
        if points[i] == points[i + 5] or points[i] == points[i + 10] or points[i + 10] == points[i + 5]:
            print(f"出现重复元素{i}列")
            a = False
        if i < 2:
            if points[i] == 11 or points[i + 5] == 11 or points[i + 10] == 11:
                print('小游戏符号顺序错误')
                a = False
    if not a:
        exit(-9)
    adpoints = {}
    for col1_key, col1_value in col1.items():
        if col1_value not in adpoints.keys():  # 字典里没有该符号
            if col1_value not in WILD:
                for col2_key, col2_value in col2.items():
                    if col1_value == col2_value or col2_value in WILD:
                        for col3_key, col3_value in col3.items():
                            if col1_value == col3_value or col3_value in WILD:
                                try:
                                    adpoints[col1_value].append(col1_key)
                                except:
                                    adpoints[col1_value] = [col1_key]
                                adpoints[col1_value].append(col2_key)
                                adpoints[col1_value].append(col3_key)
                            elif col1_value in (11):
                                try:
                                    adpoints[col1_value].append(col1_key)
                                except:
                                    adpoints[col1_value] = [col1_key]
                                adpoints[col1_value].append(col2_key)
            else:
                for col2_key, col2_value in col2.items():
                    if (col1_value == col2_value) or (col2_value in WILD):
                        for col3_key, col3_value in col3.items():
                            try:
                                adpoints[col3_value].append(col1_key)
                            except:
                                adpoints[col3_value] = [col1_key]
                            adpoints[col3_value].append(col2_key)
                            adpoints[col3_value].append(col3_key)
                    else:
                        for col3_key, col3_value in col3.items():
                            if (col2_value == col3_value) or (col3_value in WILD):
                                try:
                                    adpoints[col2_value].append(col1_key)
                                except:
                                    adpoints[col2_value] = [col1_key]
                                adpoints[col2_value].append(col2_key)
                                adpoints[col2_value].append(col3_key)
        else:
            if col1_value not in WILD:
                adpoints[col1_value].append(col1_key)
    temAdpoints = copy.deepcopy(adpoints)
    for key, value in temAdpoints.items():
        if 2 in value or 7 in value or 12 in value:
            for col4_key, col4_value in col4.items():
                if key == col4_value or col4_value in WILD:
                    adpoints[key].append(col4_key)
                for col5_key, col5_value in col5.items():
                    if key in WILD:
                        if col4_value in WILD and col5_value not in WILD:
                            try:
                                adpoints[col5_value].append(col5_key)
                            except:
                                adpoints[col5_value] = [col5_key]
                            adpoints[col5_value].append(col4_key)
                            adpoints[col5_value] += value
                        if (col4_value not in WILD) and (col5_value == col4_value or col5_value in WILD):
                            try:
                                adpoints[col4_value].append(col4_key)
                            except:
                                adpoints[col4_value] = [col4_key]
                            adpoints[col4_value].append(col5_key)
                            adpoints[col5_value] += value
                        if (col4_value not in WILD) and (col5_value != col4_value and col5_value not in WILD):
                            try:
                                adpoints[col4_value].append(col4_key)
                            except:
                                adpoints[col4_value] = [col4_key]
                            adpoints[col4_value] += value
                    if key == col4_value or col4_value in WILD:
                        adpoints[key].append(col4_key)
                        if key == col5_value or col5_value in WILD:
                            adpoints[key].append(col5_key)
    for key, value in adpoints.items():
        if len([x for x in adpoints[key] if x in col5.keys()]) > 0:
            for col1_key, col1_value in col1.items():
                if col1_value in WILD:
                    adpoints[key].append(col1_key)
            for col2_key, col2_value in col2.items():
                if col2_value in WILD:
                    adpoints[key].append(col2_key)
            for col3_key, col3_value in col3.items():
                if col3_value in WILD:
                    adpoints[key].append(col3_key)
            for col4_key, col4_value in col4.items():
                if col4_value in WILD:
                    adpoints[key].append(col4_key)
            for col5_key, col5_value in col5.items():
                if col5_value in WILD:
                    adpoints[key].append(col5_key)
        elif len([x for x in adpoints[key] if x in col4.keys()]) > 0:
            for col1_key, col1_value in col1.items():
                if col1_value in WILD:
                    adpoints[key].append(col1_key)
            for col2_key, col2_value in col2.items():
                if col2_value in WILD:
                    adpoints[key].append(col2_key)
            for col3_key, col3_value in col3.items():
                if col3_value in WILD:
                    adpoints[key].append(col3_key)
            for col4_key, col4_value in col4.items():
                if col4_value in WILD:
                    adpoints[key].append(col4_key)
        elif len([x for x in adpoints[key] if x in col3.keys()]) > 0:
            for col1_key, col1_value in col1.items():
                if col1_value in WILD:
                    adpoints[key].append(col1_key)
            for col2_key, col2_value in col2.items():
                if col2_value in WILD:
                    adpoints[key].append(col2_key)
            for col3_key, col3_value in col3.items():
                if col3_value in WILD:
                    adpoints[key].append(col3_key)
        adpoints[key] = list(set(value))
    popSymbols = []
    if 13 in adpoints.keys():
        if len(adpoints[13]) < 3:
            popSymbols.append(13)
    for popSymbol in popSymbols:
        adpoints.pop(popSymbol)
    if len(symbol12_list) >= 2:
        adpoints[12] = symbol12_list
    my_adpoints = {}
    for key, value in adpoints.items():
        my_adpoints[str(key)] = value
    my_adPoints = filterAdpoints(my_adpoints, points)
    for key in my_adPoints.keys():
        if sorted(my_adPoints[key]) != sorted(response['et']['data']['adPoints'].get(key, [])) and len(
            [x for x in my_adPoints[key] if x % 5 == colNum - 1]) > 0:
            print("中奖点有误", my_adPoints, response)
            return False
    for key in response['et']['data']['adPoints'].keys():
        if sorted(my_adPoints[key]) != sorted(response['et']['data']['adPoints'].get(key, [])) and len(
            [x for x in my_adPoints[key] if x % 5 == colNum - 1]) > 0:
            print("中奖点有误", my_adPoints, response)
            return False
    return True


def normalPlay(tokenid, gametype, betScore):  # 正常玩模式
    url = GETSLOTURL
    millis = str(int(round(time.time() * 1000)))
    headers = {
        'token': tokenid,
        'Content-Type': 'application/json'
        }
    data = {
        "gt": str(gametype),
        "betScore": str(betScore),
        "actionType": "0",
        'token': tokenid,
        # 'betType': "0",
        }
    data = json.dumps(data)
    try:
        response = session.post(url, data=data, headers=headers)
        print(response.text)
        response = response.json()
        if response.get("code") == 20000:
            # print(response)
            return response
        elif response.get("code") == 20001:
            print(response)
            exit(-2)
        else:
            with open('error.txt', 'a')as f:
                f.write('\n' + response)
            print("error", response)
    except:
        pass
    return None


def checkachievement(response, lastachievement):
    if response['et']['data']['type'] == 0:
        achievement = copy.deepcopy(lastachievement)
        addAchievement_flag = False
        awardlins = response['et']['data']['awardLines']
        adPoints = response['et']['data']['adPoints']
        linePoints = response['et']['data']['linePoints']
        points_list = response['et']['data']['points']
        if response['et']['type'] == 0 and len(awardlins) != 0:
            for key, value in awardlins.items():
                award_symbol_index_list = []
                for i in adPoints[key]:
                    award_symbol_index_list.append(i)
                if key not in WILD_STR:
                    remove_symbol_indexs = []
                    for symbol_index in award_symbol_index_list:
                        if points_list[symbol_index] in WILD:
                            remove_symbol_indexs.append(symbol_index)
                    for remove_symbol_index in remove_symbol_indexs:
                        award_symbol_index_list.remove(remove_symbol_index)
                if len(award_symbol_index_list) >= value:
                    if key in achievement:
                        achievement_value = achievement[key]
                        award_dic_value = str(value)
                        if award_dic_value not in achievement_value:
                            achievement_value.update({award_dic_value: 1})
                            achievement[key] = achievement_value
                            if int(key) < 9:
                                if len(achievement[key]) == 3:
                                    addAchievement_flag = True
                                    if key not in response['et']['data']['addAchievement']:
                                        print("成就错误", key)
                                        return False
                            else:
                                if len(achievement[key]) == 4:
                                    addAchievement_flag = True
                                    if key not in response['et']['data']['addAchievement']:
                                        print("成就错误", key)
                                        return False
                    else:
                        achievement[key] = {str(value): 1}
        if achievement != response['et']['data']['achievement'] and lastachievement != {} and response['et']['data'][
            'achievement'] != {}:
            print("成就错误1", "myachievement", achievement, "     response", response['et']['data']['achievement'])
            return False

        if not addAchievement_flag:
            if response['et']['data']['addAchievement']:
                if len(response['et']['data']['addAchievement']) > 0:
                    print("成就错误2", response['et']['data']['addAchievement'])
                    return False
        else:
            if response['et']['data']['addAchievement']:
                if len(response['et']['data']['addAchievement']) <= 0:
                    print("成就错误2", response['et']['data']['addAchievement'])
                    return False
            if not response['et']['data']['addAchievement']:
                print("成就错误2", response['et']['data']['addAchievement'])
                return False
        return response['et']['data']['achievement']
    else:
        return lastachievement


def oneColSpin(response, tk, times, gameType, mybetScore):
    global tokenid
    oneColSpin_url = GETSLOTURL
    lastnGold = response['et']['nGold']
    lastachievement = response['et']['data']['achievement']
    lastpoints = response['et']['data']['points']
    lastachievement = response['et']['data']['achievement']
    for i in range(times):
        if response['code'] == 20000:
            roteKey = response['et']['data']['roteKey']
            rotaryBls = response['et']['data']['rotaryBls']
            colNum = random.randint(1, 5)
            millis = int(round(time.time() * 1000))
            one_spin_data = {
                "gt": gameType,
                "betScore": rotaryBls[colNum - 1],
                "actionType": 1,
                "data": {"roteKey": roteKey, "roteRow": colNum}}
            one_spin_data = json.dumps(one_spin_data)
            headers = {
                'token': tk,
                'Content-Type': 'application/json'
                }
            while True:
                # print(one_spin_data)
                response = requests.post(url=oneColSpin_url, data=one_spin_data, headers=headers)
                response = response.json()
                tim = time.asctime()
                print(f"{tim}--单轴", colNum, response)
                if response['code'] == 20000:
                    break
                elif response.get("code") == 20001:
                    print(response)
                    exit(-2)
            if not checkFsAwardSymbol(response, colNum):
                return False
            if not checkLotteryInitialize(tk=tk, gametype=gameType, lastresponse=response):  # 核对断线重连初始化
                return False
            lastnGold = checkFsnGold(response, rotaryBls[colNum - 1], lastnGold, mybetScore=mybetScore)
            lastpoints = checkFsPoints(response, colNum, lastpoints)
            # lastachievement = checkachievement(response, lastachievement)
            if lastnGold == False:
                return False
            if lastpoints == False:
                return False
            if lastachievement == False:
                return False
            if response['et']['data']['isFree']:
                print('进红利')
                return response

        elif response.get("code") == 20001:
            print(response)
            exit(-2)
        else:
            print('error', response)
    return response


def call(tk, gametype):
    url = INITURL
    data = {
        "gt": str(gametype),
        "timestamp": 45646545654,
        'actionType': '0',
        'tk': tk
        }
    headers = {
        'token': tk,
        'Content-Type': 'application/json'
        }
    data = json.dumps(data)
    print("初始化", data, headers)
    response = requests.post(url=url, data=data, headers=headers)
    response = response.json()
    print("初始化", response)


def register():
    url = REGISTER
    headers = {
        'Content-Type': 'application/json'
        }
    registerResponse = requests.get(url, headers=headers)
    print(registerResponse.json())
    tokenId = registerResponse.json()['et'].get("uid")
    username = registerResponse.json()['et'].get("username")
    if tokenId:
        print(tokenId, username)
        return tokenId, username
    return None


def login(Url):
    currency = random.randint(1, 2)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '65',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': '192.168.10.213:9002',
        'Origin': 'http://192.168.10.212:9002',
        'Referer': 'http://192.168.10.212:9002/index.html?l=zh_CN&type=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
        }
    # userName = ''.join(random.sample(string.ascii_letters + string.digits, 5))
    userName = 'liu' + (''.join(random.sample(string.digits, 3)))+(''.join(random.sample(string.ascii_letters, 3)))
    payload = dict(userName=userName, password='111111', currency=currency, style='7', nickName='', sex=0)
    # payload = 'userName=li11&password=111111&currency=1&style=1&nickName=&sex=0'
    response = requests.post(Url, headers=headers, data=payload, allow_redirects=False)
    location = response.headers['location']
    # print(location)
    if len(location) > 52:
        uid_list = re.findall(r'uid=(.*)&changeurl', location)
        uid = uid_list[0]
        print(userName)
        return uid, location


def Exchange(tk, gt, type, location):
    headers = {
        'Content-Type': 'application/json',
        'Host': '192.168.10.213:9002',
        'Origin': 'http://192.168.10.213:9002',
        'Proxy-Connection': 'keep-alive',
        'Referer': str(location),
}
    data = {"tk": tk, "gameType": gt, "actionType": type}
    response = requests.post(exchange, headers=headers, json=data)
    response = json.loads(response.text)
    gold = response['et']['gold']
    money = response['et']['money']
    return gold, money


def Bounsgame(tokenid, gametype, betScore, specialKey, selectPoint):  # 小游戏
    url = GETSLOTURL
    millis = str(int(round(time.time() * 1000)))
    headers = {
        'token': tokenid,
        'Content-Type': 'application/json'
        }
    data = {
        "gt": str(gametype),
        "betScore": str(betScore),
        "actionType": "2",
        "specialKey": specialKey,
        'token': tokenid,
        "selectPoint": selectPoint
        }
    data = json.dumps(data)
    try:
        response = session.post(url, data=data, headers=headers)
        response = response.json()
        print(response, '1111')
        if response.get("code") == 20000:
            # print(response)
            return response
        elif response.get("code") == 20001:
            print(response)
            exit(-2)
        else:
            with open('error.txt', 'a')as f:
                f.write('\n' + response)
            print("error", response)
    except:
        pass
    return


def Bounsverfiy(lis, betScore, gold):
    a = False
    mygold = 0
    dic = {12: 0, 13: 0, 14: 0, 15: 0, 16: 0}
    for i in lis:
        if i == 16:
            for key, valus in dic.items():
                dic[key] += 1
            # print(dic)
        elif i == 0:
            continue
        else:
            dic[i] += 1
        print(dic)
    if dic[16] > 2:
        mygold = TW_AWARD_DIC[(16, 3)] * betScore
    else:
        for x in dic.keys():
            if dic[x] > 2:
                print(x, '号中奖', dic[x])
                mygold += TW_AWARD_DIC[(x, 3)] * betScore
    print('aaaaa', mygold, gold)
    if mygold != gold:
        print('gold错误')
        exit(-6)
    if mygold and gold > 0:
        return True
    else:
        return False


def ran(num):
    while True:
        item = random.randint(0, 15)
        if item in num:
            continue
        else:
            num.append(item)
            return item


def Bounscheck(tokenid, specialKey):
    global xyx
    if specialKey is not None:
        xyx += 1
        print(f'当前小游戏次数{xyx}--红利场||||当前红利次数{hl}')
        num = []
        for i in range(15):
            item = ran(num)
            response = Bounsgame(tokenid, GT, betScore, specialKey, item)
            specialKey = response['et']['data']['specialKey']
            lis = response['et']['data']['specialPoints']
            gold = response['et']['data']['gold']
            print('ffff', gold)
            a = Bounsverfiy(lis, betScore, gold)
            if a:
                lastnGold = response['et']['nGold']
                break
        return lastnGold
    else:
        return 0


def getToken(username, password):
    data = {
        "userName": username,
        "password": password
        }
    headers = {
        'Content-Type': 'application/json'
        }
    data = json.dumps(data)
    url = "http://192.168.10.212:8002/callToken"
    tokenResponse = requests.post(url=url, data=data, headers=headers)
    token = tokenResponse.json().get("ms")
    if token:
        return token
    return None


def main():  # 主函数 程序入口
    game = logAnalysisUtil.Record('Y002', '111', '', '', '')
    global xyx, hl
    xyx = 0
    hl = 0
    gold1 = 0
    # tokenid, username = register()
    gameType = GT
    # tokenid = '7D409574415907CDBE70DFF1D1878882999A'
    tokenid, location = login(LOGINUIR)
    requests.get(f'http://192.168.10.212:8080/user/pay?uid={tokenid}&gold=100000000000')
    call(tokenid, gameType)
    gold2 = 0
    while True:
        response = normalPlay(tokenid=tokenid, gametype=gameType, betScore=betScore)
        # time.sleep(0.5)
        specialKey = response['et']['data']['specialKey']
        if not checkAwardSymbol(response):
            return
        if specialKey is not None:
            xyx += 1
            print(f'当前小游戏次数{xyx}--普通场||||当前红利次数{hl}')
            nGold = response['et']['data']['nGold']
            num = []
            for i in range(15):
                item = ran(num)
                response1 = Bounsgame(tokenid, GT, betScore, specialKey, item)
                specialKey = response1['et']['data']['specialKey']
                lis = response1['et']['data']['specialPoints']
                gold = response1['et']['data']['gold']
                Bounsverfiy(lis, betScore, gold)
                if response1['et']['data']['specialKey'] is None:
                    lastnGold = response1['et']['data']['nGold']
                    if lastnGold == nGold+gold:
                        print('小游戏筹码正常')
                    else:
                        return
                    break
            continue

        if response:
            if response['et']['type'] == 0 and response['et']['data']['isFree'] == False:
                if not checkAwardSymbol(response):
                    return
                if not checkLotteryInitialize(tk=tokenid, gametype=gameType, lastresponse=response):  # 核对断线重连初始化
                    return
                if 'lastnGold' not in dir():  # 如果是第一次运行脚本
                    lastnGold = response['et']['nGold']
                    lastachievement = response['et']['data']['achievement']
                else:
                    lastnGold = checknGold(response, betScore, lastnGold)
                    # lastachievement = checkachievement(response, lastachievement)
                    if lastnGold == False:
                        return
                    # if lastachievement == False:
                    #     return
                    if GT in ZRAWARDGT:
                        times = random.randint(0, 999)
                    else:
                        times = random.randint(60, 999)
                    if times > 50:
                        times = 0
                    if times > 0:
                        response = oneColSpin(response=response, tk=tokenid, times=times, gameType=gameType,
                                              mybetScore=betScore)
                        if response == False:
                            return
                        else:
                            lastnGold = response['et']['nGold']
                            lastachievement = response['et']['data']['achievement']


            else:
                if response['et']['data']['bonusGold'] == 0:
                    print("bonusGold有误", response['et']['data']['bonusGold'])
                    return
                myfreegold = response['et']['data']['freeGold']
                if not checkAwardSymbol(response):
                    return
                if not checkLotteryInitialize(tk=tokenid, gametype=gameType, lastresponse=response):  # 核对断线重连初始化
                    return
                if 'lastnGold' not in dir():  # 如果是第一次运行脚本
                    lastnGold = response['et']['nGold']
                    print(lastnGold)
                    # lastachievement = response['et']['data']['achievement']
                else:
                    lastnGold = checknGold(response, betScore, lastnGold)
                    # lastachievement = checkachievement(response,lastachievement)
                    if lastnGold == False:
                        return
                    # if lastachievement == False:
                    #     return
                if response['et']['type'] == 1:
                    fsTimes = response['et']['data']['residue']
                elif response['et']['data']['isFree'] == True:
                    hl += 1
                    print(f'当前小游戏次数{xyx}||||当前红利次数{hl}')
                    fsTimes = 13
                playedTimes = 1
                specialKey = response['et']['data']['specialKey']
                while playedTimes <= fsTimes:
                    # print(specialKey,'two')
                    if specialKey is not None:
                        print('红利进入小游戏模式了')
                        for i in range(15):
                            response = Bounsgame(tokenid, GT, betScore, specialKey, i)
                            specialKey = response['et']['data']['specialKey']
                            lis = response['et']['data']['specialPoints']
                            gold1 = response['et']['data']['gold']
                            Bounsverfiy(lis, betScore, gold1)
                            print(response)
                            if response['et']['data']['specialKey'] is None:
                                lastnGold = response['et']['nGold']
                                break
                        gold1 = response['et']['data']['gold']
                        continue
                    response = normalPlay(tokenid=tokenid, gametype=gameType, betScore=betScore)
                    if response:
                        specialKey = response['et']['data']['specialKey']
                        print('cut', myfreegold, gold1, response['et']['data']['gold'])
                        myfreegold = response['et']['data']['gold'] + myfreegold + gold1
                        gold1 = 0
                        if myfreegold != response['et']['data']['freeGold']:
                            print("freegold错误", myfreegold, response['et']['data']['freeGold'])
                            return
                        if not checkAwardSymbol(response):
                            return
                        if not checkLotteryInitialize(tk=tokenid, gametype=gameType,
                                                      lastresponse=response):  # 核对断线重连初始化
                            return
                        if response['et']['type'] != 1:
                            print("红利错误", playedTimes, fsTimes)
                            return
                        fsTimes += response['et']['data']['plan']
                        if 'lastnGold' not in dir():  # 如果是第一次运行脚本
                            print('lllllll')
                            lastnGold = response['et']['nGold']

                        else:
                            lastnGold = checknGold(response, betScore, lastnGold)
                            # lastachievement = checkachievement(response,lastachievement)
                            if lastnGold == False:
                                return
                            # if lastachievement == False:
                            #     return
                        if response['et']['data']['residue'] + playedTimes != fsTimes:
                            print("红利错误", playedTimes, fsTimes)
                            return
                        playedTimes += 1
                        # specialKey = response['et']['data']['specialKey']
                c = Bounscheck(specialKey=specialKey, tokenid=tokenid)
                if c != 0:
                    lastnGold = c


if __name__ == '__main__':
    for i in range(1):
        threading.Thread(target=main).start()
        time.sleep(5)

