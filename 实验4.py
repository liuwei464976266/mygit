# import json
# text = open(r"C:\Users\Administrator\Desktop\A1.txt", "r")
# x = 0
# for line in text.readlines():
#     if line[0] == '{':
#         a = eval(line)
#         b = json.dumps(a)
#         c = json.loads(b)
#         x += c['et']['gold']
#         print(c)
#         print(c['et']['gold'], c['et']['data']['bonusGold'], c['et']['data']['freeGold'], c['et']['nGold'])
#         # print(x)
#         if x != c['et']['data']['bonusGold']+c['et']['data']['freeGold']:
#             print('cuowu')

# encoding:utf-8
import requests, json, threading, time, random, datetime, string, re
import operator
from functools import reduce
from queue import Queue
import copy

WILD = [12]
WILD_STR = ['12']
MAXPAYGOLD = 970000
SCATTER = '11'
session = requests.session()
GT = 144
BET = 3000
pattern = 2
LOGINUIR = "http://192.168.10.213:9002/user/register"
INITURL = 'http://192.168.10.213:9008/callInitialize'
SLOTURL = 'http://192.168.10.213:9008/getSlotData'
REGISTERURL = 'http://192.168.10.213:9000/registerUser'
exchange = 'http://192.168.10.213:9002/api/Service/ExchangeInOrOut'
PLAY_BOY_AWARD = {
    (11, 1): 0,
    (11, 2): 1,
    (1, 3): 2,
    (2, 3): 3,
    (3, 3): 4,
    (4, 3): 5,
    (5, 3): 6,
    (6, 3): 10,
    (7, 3): 15,
    (8, 3): 20,
    (9, 3): 25,
    (10, 3): 30,
    (11, 3): 2,
    (12, 3): 35,
    (1, 4): 10,
    (2, 4): 10,
    (3, 4): 12,
    (4, 4): 15,
    (5, 4): 15,
    (6, 4): 25,
    (7, 4): 30,
    (8, 4): 40,
    (9, 4): 50,
    (10, 4): 60,
    (11, 4): 10,
    (12, 4): 100,
    (1, 5): 40,
    (2, 5): 45,
    (3, 5): 50,
    (4, 5): 55,
    (5, 5): 60,
    (6, 5): 100,
    (7, 5): 125,
    (8, 5): 150,
    (9, 5): 200,
    (10, 5): 250,
    (11, 5): 50,
    (12, 5): 300,
    }


def filterAdpoints(adpoints, points):  # 自己计算adpoints
    filtedAdpoints = {}
    myadpoints = copy.deepcopy(adpoints)  # 拷贝一个 myadpoints 避免后续直接修改adpoints对象
    myDicAdpoints = {}
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
            if len(col5) > 0:
                mylinepoints = [[a, b, c, d, e] for a in col1 for b in col2 for c in col3 for d in col4 for e in col5]
            elif len(col4) > 0:
                mylinepoints = [[a, b, c, d] for a in col1 for b in col2 for c in col3 for d in col4]
            elif len(col3) > 0:
                mylinepoints = [[a, b, c] for a in col1 for b in col2 for c in col3]
            else:
                mylinepoints = []
            removeLines = []
            for i in mylinepoints:
                if len([x for x in i if points[x] not in WILD]) <= 0 and key not in WILD_STR:
                    removeLines.append(i)
            print(key, 'removeLines filter', removeLines)
            for i in removeLines:
                mylinepoints.remove(i)
            myListAdpoints = []
            for i in mylinepoints:
                myListAdpoints += i
            myListAdpoints = list(set(myListAdpoints))
            myDicAdpoints[key] = myListAdpoints

        else:
            myDicAdpoints['11'] = value
    print("过滤后返回adpoints", myDicAdpoints)
    return myDicAdpoints


def getColsSymbol(points):  # 取出各列中奖位置
    symbol13_list = []
    col1, col2, col3, col4, col5 = {}, {}, {}, {}, {}
    for i in range(len(points)):
        if points[i] == 11:
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
    return col1, col2, col3, col4, col5, symbol13_list


def checkAwardSymbol(rpoints):  # 核对adpoints
    points = rpoints['points']
    col1, col2, col3, col4, col5, symbol13_list = getColsSymbol(points)
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
    if 15 in adpoints.keys():
        adpoints[14] = adpoints[15]
        adpoints.pop(15)
    if 14 in adpoints.keys():
        if len(adpoints[14]) < 3:
            popSymbols.append(14)
    for popSymbol in popSymbols:
        adpoints.pop(popSymbol)
    if len(symbol13_list) >= 2:
        adpoints[11] = symbol13_list
    if len(symbol13_list) == 1 and rpoints['specialType'] == 2:  # 封锁红利的时候1个散步也要计算获奖
        adpoints[11] = symbol13_list
    my_adpoints = {}
    for key, value in adpoints.items():
        my_adpoints[str(key)] = value
        print('kkk', my_adpoints)
    my_adpoints = filterAdpoints(my_adpoints, points)
    # print("my_adpoints",my_adpoints,"rpoints['adPoints']",rpoints['adPoints'])
    for key in my_adpoints.keys():
        if sorted(my_adpoints[key]) != sorted(rpoints['adPoints'].get(key, [])):
            print("adpoints有误")
            print(key, 'my_adpoints', sorted(my_adpoints[key]), 'adpoints', sorted(rpoints['adPoints'].get(key, [])))
            return False
    for key in rpoints['adPoints'].keys():
        if sorted(my_adpoints[key]) != sorted(rpoints['adPoints'].get(key, [])):
            print("adpoints有误")
            print(key, 'my_adpoints', sorted(my_adpoints[key]), 'adpoints', sorted(rpoints['adPoints'].get(key, [])))
            return False
    return True


def checkAdpoints(response):  # 幸存者红利模式消消乐专属
    for rpoints in response['et']['data']['lines']:
        print('消消乐分线', rpoints)
        if not checkAwardSymbol(rpoints):
            return False
        points = copy.deepcopy(rpoints['points'])
        adPoints = rpoints['adPoints']
        if 'myPoints' not in dir():  # myPoints变量未定义
            myPoints = []
            for Symbols in points:
                myPoints.append(Symbols)
            # print(myPoints,"=",points)
        if len(myPoints) != 15 or len(points) != 15:
            print(myPoints, rpoints['points'])
            print("个数不正确")
            return False
        for i in range(len(myPoints)):
            if myPoints[i] != 'randomSymbol' and myPoints[i] != points[i]:
                print("结果错误", "myPoints", myPoints, "points", points)
                return False
        myPoints = points
        award_index_list = []
        for i in range(len(points)):
            if points[i] < 6:
                award_index_list.append(i)
                if str(i) not in rpoints['specialEvent'].keys():
                    print('specialEvent 点位错误')
                    return

        # for index_list in adPoints.values():
        #     award_index_list = award_index_list + index_list
        # award_index_list = list(set(award_index_list))#中奖下标列表去重
        # award_index_list = sorted(award_index_list)#中奖下标列表排序
        for award_index in award_index_list:
            if award_index < 5:
                myPoints[award_index] = "randomSymbol"  # 如果第一行有中奖，该位置为随机符号
            elif 5 <= award_index < 10:
                if myPoints[award_index - 5] == "randomSymbol":  # 如果第一行有随机符号
                    myPoints[award_index] = "randomSymbol"  # 第二行该位置为随机符号
                else:  # 如果第一列不为随机符号
                    myPoints[award_index] = myPoints[award_index - 5]  # 该位置为第一行符号
                    myPoints[award_index - 5] = "randomSymbol"  # 第一行为随机符号
            elif 10 <= award_index <= 14:
                if myPoints[award_index - 5] == "randomSymbol":  # 如果第二行为随机符号，
                    myPoints[award_index] = "randomSymbol"  # 第三行该位置为随机符号
                else:  # 如果第二列不为随机符号
                    myPoints[award_index] = myPoints[award_index - 5]  # 第三行为第二行符号
                    myPoints[award_index - 5] = myPoints[award_index - 10]  # 第二行为第一行符号
                    myPoints[award_index - 10] = "randomSymbol"  # 第一行为随机符号
    return True


def checkLinePoints(adpoints, linepoints, points):  # 核对LinePoints，具体赢赏分线
    print("开始检查linepoints")
    myadpoints = copy.deepcopy(adpoints)  # 拷贝一个 myadpoints 避免后续直接修改adpoints对象
    for key, value in myadpoints.items():
        if key != SCATTER:
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
            else:
                mylinepoints = []
            removeLines = []
            for i in mylinepoints:
                if len([x for x in i if points[x] not in WILD]) <= 0 and key not in WILD_STR:
                    removeLines.append(i)
            print(key, 'removeLines', removeLines)
            for i in removeLines:
                mylinepoints.remove(i)
            if sorted(mylinepoints) != sorted(linepoints[key]):
                print("linepoints有误", key, sorted(mylinepoints), sorted(linepoints[key]))
                return False
        else:
            if key in linepoints:
                print("linepoints有误包含符号散步")
                return False
    return True


def checkNgold(response, betScore, lastNgold):  # 核对Ngold
    pp = '默认'
    award_dic = PLAY_BOY_AWARD
    if response['et']['type'] == 2:
        if 11 in response['et']['data']['points']:
            return
    if response['et']['type'] == 1:
        for rx in response['et']['data']['lines']:
            if 11 in rx['points']:
                return
    if response['et']['type'] == 1:  # 幸存者红利模式
        Rpoints = response['et']['data']['lines']
        if len(Rpoints) > 1:  # 如果有消消乐
            pp = '红利1有消消乐奖'
            if not checkAdpoints(response):
                return False
            paygold = 0
            for rpointIndex in range(len(Rpoints)):
                awardLines = Rpoints[rpointIndex]['awardLines']
                Points = Rpoints[rpointIndex]['points']
                AdPoints = Rpoints[rpointIndex]['adPoints']
                LinePoints = Rpoints[rpointIndex]['linePoints']
                specialEvent = Rpoints[rpointIndex]['specialEvent']
                # if not checkLinePoints(AdPoints, LinePoints, Points):
                #     return False
                if specialEvent:
                    paygold += sum(specialEvent.values())
                    for key, values in specialEvent.items():
                        if (Points[int(key)]) < 1 or (Points[int(key)]) > 5:
                            exit(-11)
                        if values > betScore:
                            print("爆点超出底注了")
                            return
                for key, value in awardLines.items():  # 遍历中奖符号
                    if key == SCATTER:  # 出现散布图
                        paygold = paygold + (award_dic[(int(key), value)] * betScore) * 1  # 直接乘投注的倍数
                    else:
                        for i in LinePoints[key]:
                            paygold = paygold + award_dic[(int(key), len(i))] * (betScore / 30) * 1
                    print(key, paygold)
            if Points == [15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15]:
                paygold = MAXPAYGOLD * betScore / 30
            if Points == [14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14]:
                paygold = MAXPAYGOLD * betScore / 30
            if paygold > MAXPAYGOLD * betScore / 30:
                paygold = MAXPAYGOLD * betScore / 30
            current_gold = int(lastNgold + paygold)  # 计算出current——gold
        elif len(Rpoints) == 1 and Rpoints[0]['awardLines']:  # 没有消消乐但是中奖了
            pp = '红利1没有消消乐有普通奖'
            AdPoints = Rpoints[0]['adPoints']
            LinePoints = Rpoints[0]['linePoints']
            paygold = 0
            hl_num = 1
            awardLines = Rpoints[0]['awardLines']
            Points = Rpoints[0]['points']
            if not checkAdpoints(response):
                return False
            if not checkLinePoints(AdPoints, LinePoints, Points):
                return False
            for key, value in awardLines.items():  # 遍历中奖符号
                if key == SCATTER:  # 出现散布图
                    paygold = paygold + (award_dic[(int(key), value)] * betScore) * hl_num  # 直接乘投注的倍数
                else:
                    for i in LinePoints[key]:
                        paygold = paygold + award_dic[(int(key), len(i))] * (betScore / 30) * hl_num
                print(key, paygold)

            if Points == [15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15]:
                paygold = MAXPAYGOLD * betScore / 30
            if Points == [14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14]:
                paygold = MAXPAYGOLD * betScore / 30
            if paygold > MAXPAYGOLD * betScore / 30:
                paygold = MAXPAYGOLD * betScore / 30
            current_gold = int(lastNgold + paygold)  # 计算出current——gold
        else:  # 没有奖，也没有消消乐
            pp = '红利1被白嫖了'
            if not checkAdpoints(response):
                return False
            current_gold = lastNgold
    elif response['et']['type'] == 2:  # 僵尸红利模式
        pp = '红利模式2'
        Rpoints = response['et']['data']
        points = Rpoints['points']
        col1, col2, col3, col4, col5, symbol13_list = getColsSymbol(points)
        list_col1 = [x for x in col1.values()]
        list_col2 = [x for x in col2.values()]
        list_col3 = [x for x in col3.values()]
        list_col4 = [x for x in col4.values()]
        list_col5 = [x for x in col5.values()]
        list_allcols = [list_col1, list_col2, list_col3, list_col4, list_col5]
        # for i in range(5):
        #     if points[i] == points[i + 5] or points[i] == points[i + 10] or points[i + 10] == points[i + 5]:
        #         print(f"出现重复元素{i}列")
        #         exit(-10)
        AdPoints = Rpoints['adPoints']
        LinePoints = Rpoints['linePoints']
        if len(Rpoints['awardLines']) > 0:  # 如果有中奖
            paygold = 0
            hl_num = 1
            awardLines = Rpoints['awardLines']
            Points = Rpoints['points']
            if points.count(11) >= 1:
                print("免费场中免费场有误")
                exit(-4)
            if not checkLinePoints(AdPoints, LinePoints, Points):
                return False
            for key, value in awardLines.items():  # 遍历中奖符号
                if key == SCATTER:  # 出现散布图
                    print('错误结算')
                    return
                    # paygold = paygold + (award_dic[(int(key), value)] * betScore) * hl_num  # 直接乘投注的倍数
                else:
                    for i in LinePoints[key]:
                        paygold = paygold + award_dic[(int(key), len(i))] * (betScore / 30) * hl_num
                print(key, paygold)
            if Points == [15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15]:
                paygold = MAXPAYGOLD * betScore / 30
            if Points == [14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14]:
                paygold = MAXPAYGOLD * betScore / 30
            if paygold > MAXPAYGOLD * betScore / 30:
                paygold = MAXPAYGOLD * betScore / 30
            current_gold = int(lastNgold + paygold)  # 计算出current——gold
        else:
            current_gold = int(lastNgold)
    else:  # 普通模式下验证金流
        Rpoints = response['et']['data']
        points = Rpoints['points']
        col1, col2, col3, col4, col5, symbol13_list = getColsSymbol(points)
        list_col1 = [x for x in col1.values()]
        list_col2 = [x for x in col2.values()]
        list_col3 = [x for x in col3.values()]
        list_col4 = [x for x in col4.values()]
        list_col5 = [x for x in col5.values()]
        list_allcols = [list_col1, list_col2, list_col3, list_col4, list_col5]
        for i in list_allcols:
            if len(i) > len(list(set(i))) and i.count(12) <= 1:
                print("出现重复元素1")
                return False
        for i in range(5):
            if points[i] == points[i + 5] or points[i] == points[i + 10] or points[i + 10] == points[i + 5]:
                if points[i] == points[i + 5] and points[i] != 12:
                    print(f"出现重复元素{i}列{points[i]}号重复")
                    return
                elif points[i] == points[i + 10] and points[i] != 12:
                    print(f"出现重复元素{i}列{points[i]}号重复")
                    return
                elif points[i + 10] == points[i + 5] and points[i + 5] != 12:
                    print(f"出现重复元素{i}列{points[i + 5]}号重复")
                    return
                else:
                    pass
        AdPoints = Rpoints['adPoints']
        LinePoints = Rpoints['linePoints']
        if len(Rpoints['awardLines']) > 0:  # 如果有中奖
            paygold = 0
            hl_num = 1
            awardLines = Rpoints['awardLines']
            Points = Rpoints['points']
            if not checkLinePoints(AdPoints, LinePoints, Points):
                return False
            for key, value in awardLines.items():  # 遍历中奖符号
                if key == SCATTER:  # 出现散布图
                    paygold = paygold + (award_dic[(int(key), value)] * betScore) * hl_num  # 直接乘投注的倍数
                else:
                    for i in LinePoints[key]:
                        paygold = paygold + award_dic[(int(key), len(i))] * (betScore / 30) * hl_num
                print(key, paygold)

            if Points == [15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15]:
                paygold = MAXPAYGOLD * betScore / 30
            if Points == [14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14]:
                paygold = MAXPAYGOLD * betScore / 30
            if paygold > MAXPAYGOLD * betScore / 30:
                paygold = MAXPAYGOLD * betScore / 30
            if '11' in Rpoints['awardLines'].keys() and len(Rpoints['awardLines']) == 1 and Rpoints['awardLines'][
                '11'] == 1 and Rpoints['specialType'] != 0:
                specialEvent = Rpoints['specialEvent']
                if Rpoints['specialType'] == 1:  # 普通场僵尸之拳
                    print("僵尸之拳来了")
                    paygold = paygold + specialEvent
                elif Rpoints['specialType'] == 2:  # 普通场封锁红利
                    paygold = sum(specialEvent.values())
                    print(f"封锁红利来了,总赢赏{paygold}")
                    for key, values in specialEvent.items():
                        if Rpoints['points'][int(key)] < 6 or Rpoints['points'][int(key)] > 10:
                            exit(-11)
                        if values % betScore != 0:
                            print("封锁筹码倍数错误")
                            return
            current_gold = int(lastNgold + paygold - betScore)  # 计算出current——gold

        elif len(Rpoints['awardLines']) < 1 and Rpoints['specialType'] != 0:
            # elif (Rpoints['awardLines'] is not True or Rpoints['awardLines'].keys == 11) and Rpoints['specialType'] != 0:   # 没有中奖并且有小游戏
            paygold = 0
            specialEvent = Rpoints['specialEvent']
            if Rpoints['specialType'] == 1:  # 普通场僵尸之拳
                print("僵尸之拳来了")
                paygold = paygold + specialEvent

            elif Rpoints['specialType'] == 2:  # 普通场封锁红利
                paygold = sum(specialEvent.values())
                print(f"封锁红利来了,总赢赏{paygold}")
                for key, values in specialEvent.items():
                    if Rpoints['points'][int(key)] < 6 or Rpoints['points'][int(key)] > 10:
                        exit(-11)
                    if values % betScore != 0:
                        print("封锁筹码倍数错误")
                        return
            current_gold = int(lastNgold + paygold - betScore)
        else:
            # paygold = 0
            current_gold = int(lastNgold - betScore)
    # if paygold != response['et']['gold']:
    #     print('allgold错误','paygold',paygold,'gold',response['et']['gold'])
    #     return False
    if current_gold != response['et']['nGold']:
        print(f'游戏模式==={pp},=====筹码错误', current_gold, response['et']['nGold'])
        print(paygold)
        return False
    else:
        print(f'游戏模式==={pp},=====筹码正确')
    return current_gold


def checkachievement(response, lastachievement):
    # print('1111lastachievement', lastachievement)
    if response['et']['data']['type'] == 0:
        achievement = copy.deepcopy(lastachievement)
        addAchievement_flag = False
        awardlins = response['et']['data']['awardLines']
        adPoints = response['et']['data']['adPoints']
        linePoints = response['et']['data']['linePoints']
        points_list = response['et']['data']['points']
        if response['et']['type'] == 0 and len(awardlins) != 0:
            for key, value in awardlins.items():
                if value >= 2:
                    award_symbol_index_list = []
                    for i in adPoints[key]:
                        award_symbol_index_list.append(i)
                    if key not in WILD_STR:
                        remove_symbol_indexs = []
                        for symbol_index in award_symbol_index_list:
                            print("开始验证时候为百搭", key, value, symbol_index, points_list[symbol_index],
                                  type(points_list[symbol_index]))
                            if points_list[symbol_index] in WILD:
                                print("确定有百搭", key, value, symbol_index, points_list[symbol_index], WILD)
                                remove_symbol_indexs.append(symbol_index)
                        for remove_symbol_index in remove_symbol_indexs:
                            award_symbol_index_list.remove(remove_symbol_index)
                        print(key, "验证完毕", award_symbol_index_list, len(award_symbol_index_list), value)
                    if len(award_symbol_index_list) >= value:
                        if key in achievement:
                            achievement_value = achievement[key]
                            award_dic_value = str(value)
                            if award_dic_value not in achievement_value:
                                achievement_value.update({award_dic_value: 1})
                                achievement[key] = achievement_value
                                if int(key) != int(SCATTER):
                                    if len(achievement[key]) == 3:
                                        addAchievement_flag = True
                                        if key not in response['et']['data']['addAchievement']:
                                            print("成就错误", key)
                                            return False
                                else:
                                    if len(achievement[key]) == 4:
                                        print(achievement)
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
                    print("成就错误3", response['et']['data']['addAchievement'])
                    return False
            if not response['et']['data']['addAchievement']:
                print("成就错误4", response['et']['data']['addAchievement'])
                return False
        return response['et']['data']['achievement']
    else:
        # print('返回lastachievement', lastachievement)
        return lastachievement


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
    # print('核对断线重连', response)
    if response['et']['data']['lastData'] != lastresponse['et']['data']:
        print('断线重连有误', "response['et']['data']['lastData']", response['et']['data']['lastData'],
              "lastresponse['et']['data']", lastresponse['et']['data'])
        return False
    if response['et']['data']['lineNumber'] != 30:
        print('线数错误', "response['et']['data']['lineNumber']", response['et']['data']['lineNumber'])
        return False
    if response['et']['data']['parValue'] != [0.01, 0.02, 0.05, 0.1]:
        print('面额错误', "response['et']['data']['parValue']", response['et']['data']['parValue'])
        return False
    if response['et']['data']['quantityData'] != [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]:
        print('数量错误', "response['et']['data']['quantityData']", response['et']['data']['quantityData'])
        return False
    # if response['et']['data']['lastData']['residue']+1 != response['et']['data']['freeCount']:
    #     print('免费次数错误', "response['et']['data']['lastData']['residue']", response['et']['data']['lastData']['residue'])
    #     print("response['et']['data']['freeCount']", response['et']['data']['freeCount'])
    #     return False
    if response['et']['data']['lastData']['freeGold'] != response['et']['data']['freeGold']:
        print('freegold错误', "response['et']['data']['lastData']['freeGold']",
              response['et']['data']['lastData']['freeGold'])
        print("response['et']['data']['freeGold']", response['et']['data']['freeGold'])
        return False
    if response['et']['data']['initQuantity'] != BET:
        print('初始筹码错误', "response['et']['data']['initQuantity']", response['et']['data']['initQuantity'])
        return False
    # if response['et']['data']['lastData']['bonusGold'] != response['et']['data']['bonusGold']:
    #     print('bonusGold错误', "response['et']['data']['lastData']['bonusGold']",
    #           response['et']['data']['lastData']['bonusGold'])
        print("response['et']['data']['bonusGold']", response['et']['data']['bonusGold'])
        return False
    # if response['et']['data']['type'] != 1:
    #     if response['et']['data']['bonusGold'] > 0 and (
    #         response['et']['data']['lastData']['isFree'] == False and response['et']['data']['lastData']['type'] == 0):
    #         print('bonusGold错误1')
    #         return False
    if response['et']['data']['bonusGold'] == 0 and (
        response['et']['data']['lastData']['isFree'] == True or response['et']['data']['lastData']['type'] != 0):
        print('bonusGold错误2')
        return False
    if response['et']['data']['type'] != response['et']['data']['lastData']['type'] and (
        response['et']['data']['lastData']['isFree'] == False and (
        (response['et']['data']['lastData']['residue'] != 0 and response['et']['data']['lastData']['type'] == 1) or (
        response['et']['data']['lastData']['residue'] == 0 and response['et']['data']['lastData']['type'] == 0))):
        print('type错误')
        return False
    if response['et']['data']['type'] == 0:
        if response['et']['data']['lastData']['achievement'] != response['et']['data']['achievement']:
            if response['et']['data']['lastData']['achievement']:
                print('断线重连成就错误')
                return False
    return True


def normalPlay(tokenid, gametype, betScore):  # 正常玩模式
    url = SLOTURL
    millis = str(int(round(time.time() * 1000)))
    headers = {
        'token': tokenid,
        'Content-Type': 'application/json'
        }
    data = {
        "gt": str(gametype),
        "betScore": str(betScore),
        "actionType": '0',
        "timestamp": millis,
        'role': pattern
        }
    data = json.dumps(data)
    try:
        respon = session.post(url, data=data, headers=headers)
        response = respon.json()
        # print('请求数据', respon.request.headers, respon.request.body)
        print(response)
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


def call(tk, gametype):
    url = INITURL
    data = {
        "gt": gametype,
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
    url = REGISTERURL
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
    print(token)
    if token:
        return token
    return None


def java_login(username, password, style=5):
    while True:
        url = f"http://192.168.10.212:8001/login?username={username}&password={password}&style={style}"
        headers = {
            'Content-Type': 'application/json;charset=UTF-8'
            }
        loginResponse = session.post(url, headers)
        loginResponse = loginResponse.json()
        print("登录", loginResponse)
        if loginResponse['code'] == 20000:
            url = 'http://192.168.10.212:8001/selectGame'
            token = loginResponse['et']['uid']
            headers = {
                'token': token,
                'Content-Type': 'application/json;charset=UTF-8'
                }
            selectResponse = session.post(url=url, headers=headers)
            url = 'http://192.168.10.212:8001/getUserInfo'
            headers = {
                'token': token,
                }
            infoResponse = session.get(url=url, headers=headers)
            infoResponse = infoResponse.json()
            print("获取用户信息", infoResponse)
            return token


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
        'Origin': 'http://192.168.10.213:9002',
        'Referer': 'http://192.168.10.213:9002/index.html?l=zh_CN&type=0',
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


def main():  # 主函数 程序入口
    # tokenid, username = register()
    gameType = GT
    # tokenid = '5C3C6B48C0CC517D127A3A327E97C3CE8576'
    tokenid, location = login(LOGINUIR)
    gold, money = Exchange(tokenid, 130, 1, location)
    print(gold, money)
    betScore = BET
    call(tokenid, gameType)
    while True:
        response = normalPlay(tokenid=tokenid, gametype=gameType, betScore=betScore)
        if response:
            if response['et']['type'] == 0 and response['et']['data']['isFree'] == False:  # 纯普通场
                if not checkAwardSymbol(response['et']['data']):
                    return
                if not checkLotteryInitialize(tk=tokenid, gametype=gameType, lastresponse=response):  # 核对断线重连初始化
                    return
                if 'lastnGold' not in dir():  # 如果是第一次运行脚本
                    lastnGold = response['et']['nGold']
                    lastachievement = response['et']['data']['achievement']
                    print('aaaaa', lastachievement)
                else:
                    lastnGold = checkNgold(response, betScore, lastnGold)
                    lastachievement = checkachievement(response, lastachievement)
                    if lastnGold == False:
                        return
                    if lastachievement == False:
                        return
                    if response == False:
                        return
                    else:
                        lastnGold = response['et']['nGold']
                        lastachievement = response['et']['data']['achievement']
            else:
                myfreegold = response['et']['data']['freeGold']
                bonusGold = response['et']['data']['bonusGold']
                nGold = response['et']['nGold']
                print('进红利当局', nGold)
                bouns = response['et']['data']['bonusGold']
                gold = 0
                if not checkLotteryInitialize(tk=tokenid, gametype=gameType, lastresponse=response):  # 核对断线重连初始化
                    return
                if 'lastnGold' not in dir():  # 如果是第一次运行脚本
                    lastnGold = response['et']['nGold']
                    lastachievement = response['et']['data']['achievement']
                else:
                    lastnGold = checkNgold(response, betScore, lastnGold)
                    lastachievement = checkachievement(response, lastachievement)
                    if lastnGold == False:
                        return
                    if lastachievement == False:
                        return
                if response['et']['type'] == 0 and response['et']['data']['isFree']:
                    print('准备红利')
                    if bonusGold == 0 or myfreegold != 0:
                        print("bonusGold有误", bonusGold, myfreegold)
                        return
                    if response['et']['data']['isFree'] == True and pattern == 1:
                    # if response['et']['data']['isFree']:
                        print('待进入1')
                        fsTimes = 25
                        playedTimes = 0
                        num = 0
                        j = response['et']['gold']
                        while playedTimes < fsTimes:
                            response = normalPlay(tokenid=tokenid, gametype=gameType, betScore=betScore)
                            # a = response['et']['gold']
                            gold += response['et']['gold']
                            x = gold + j
                            num += 1
                            if response['et']['type'] != 1 or num > 50:
                                print('红利1错误')
                                # return
                            if response:
                                if not checkLotteryInitialize(tk=tokenid, gametype=gameType,
                                                              lastresponse=response):  # 核对断线重连初始化
                                    print('cccc')
                                    return
                                if x != response['et']['data']['bonusGold'] + response['et']['data']['freeGold']:
                                    print(response)
                                    print('cuo', x, response['et']['data']['bonusGold'], response['et']['data']['freeGold'])
                                    return

                                if response['et']['type'] != 1:
                                    print("红利错误1", playedTimes, fsTimes)
                                    return
                                if 'lastnGold' not in dir():  # 如果是第一次运行脚本
                                    lastnGold = response['et']['nGold']
                                    lastachievement = response['et']['data']['achievement']

                                else:
                                    lastnGold = checkNgold(response, betScore, lastnGold)
                                    lastachievement = checkachievement(response, lastachievement)

                                    if lastnGold == False:
                                        return
                                    if lastachievement == False:
                                        return

                                for x in response['et']['data']['lines']:
                                    playedTimes += sum(i < 6 for i in x['points'])
                                print(f'红利1消消乐爆掉的个数是--{playedTimes}--已玩局数{num}')
                                # if response['et']['data']['residue'] + playedTimes < fsTimes:
                                #     print("红利1错误2", playedTimes, fsTimes)
                                #     return
                                if playedTimes > 21:
                                    return
                                print(playedTimes,type(playedTimes))
                        print(response['et']['nGold'], nGold)
                        myfreegold = response['et']['data']['freeGold']
                        bonusGold = response['et']['data']['bonusGold']
                        nGold = response['et']['nGold'] - nGold
                        if nGold != gold:
                            print('2222', nGold, gold)
                            return
                        if myfreegold+bonusGold != nGold+bouns:
                            print('1111', myfreegold+bonusGold, nGold, bouns)
                            return


                    else:
                        print('待进入2', response)
                        if bonusGold == 0:
                            print("bonusGold有误", bonusGold, myfreegold)
                            return
                        playedTimes = 1
                        myfregold = 0
                        while playedTimes <= 50:
                            response = normalPlay(tokenid=tokenid, gametype=gameType, betScore=betScore)
                            myfregold += response['et']['data']['gold']
                            if myfregold != response['et']['data']['freeGold']:
                                print("freegold错误", myfregold, response['et']['data']['freeGold'])
                                return
                            specialEvent = sum(response['et']['data']['specialEvent'])
                            print('specialEvent=', specialEvent)
                            if response:
                                gold += response['et']['gold']
                                myfreegold += response['et']['data']['gold']

                                if not checkAwardSymbol(response['et']['data']):
                                    return
                                if not checkLotteryInitialize(tk=tokenid, gametype=gameType,
                                                              lastresponse=response):  # 核对断线重连初始化
                                    return
                                if response['et']['type'] != 2:
                                    print("红利错误3", playedTimes)
                                    return
                                if 'lastnGold' not in dir():  # 如果是第一次运行脚本
                                    lastnGold = response['et']['nGold']
                                    lastachievement = response['et']['data']['achievement']

                                else:
                                    lastnGold = checkNgold(response, betScore, lastnGold)
                                    lastachievement = checkachievement(response, lastachievement)
                                    if lastnGold == False:
                                        return
                                    if lastachievement == False:
                                        return
                                if response['et']['data']['residue'] != playedTimes or playedTimes > 50:
                                    print("红利2错误", playedTimes, response['et']['data']['residue'])
                                    return
                                print(f'当前红利游戏局数{playedTimes}')
                                playedTimes += 1
                                if specialEvent > 4:
                                    print('结束')
                                    break
                        print(response['et']['nGold'], nGold)
                        myfreegold = response['et']['data']['freeGold']
                        bonusGold = response['et']['data']['bonusGold']
                        nGold = response['et']['nGold'] - nGold
                        print('差值', nGold)
                        if nGold != gold:
                            print('aaa', nGold, gold)
                            return
                        if myfreegold != nGold:
                            print('bbb', myfreegold, nGold)
                            return
        else:
            return


if __name__ == '__main__':
    for i in range(5):
        threading.Thread(target=main).start()
        time.sleep(2)
    # main()




