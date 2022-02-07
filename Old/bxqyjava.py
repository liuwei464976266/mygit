#encoding:utf-8
import requests, json, threading, time, random,datetime
import operator
from functools import reduce
from queue import Queue
import copy
WILD = [14,15]
WILD_STR = ['14','15']
MAXPAYGOLD = 364500
session = requests.session()
GT = 125
def filterAdpoints(adpoints,points):
    filtedAdpoints = {}
    myadpoints = copy.deepcopy(adpoints)  # 拷贝一个 myadpoints 避免后续直接修改adpoints对象
    myDicAdpoints = {}
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
            myDicAdpoints['13'] = value
    print("返回adpoints",myDicAdpoints)
    return myDicAdpoints
def checkachievement(response,lastachievement):
    print('lastachievement',lastachievement)
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
                        print("开始验证时候为百搭",key,value,symbol_index,points_list[symbol_index],type(points_list[symbol_index]))
                        if points_list[symbol_index] in WILD:
                            print("确定有百搭",key,value,symbol_index,points_list[symbol_index],WILD)
                            remove_symbol_indexs.append(symbol_index)
                    for remove_symbol_index in remove_symbol_indexs:
                        award_symbol_index_list.remove(remove_symbol_index)
                    print(key,"验证完毕",award_symbol_index_list,len(award_symbol_index_list),value)
                if len(award_symbol_index_list) >= value:
                    if key in achievement:
                        achievement_value = achievement[key]
                        award_dic_value = str(value)
                        if award_dic_value not in achievement_value:
                            achievement_value.update({award_dic_value: 1})
                            achievement[key] = achievement_value
                            if int(key) != 13:
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
        if achievement != response['et']['data']['achievement'] and lastachievement != {} and response['et']['data']['achievement'] != {}:
            print("成就错误1", "myachievement",achievement,"     response",response['et']['data']['achievement'])
            return False
        if addAchievement_flag == False:
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
def checkLinePoints(adpoints,linepoints,points):#核对LinePoints
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
            if len(col5) > 0:
                mylinepoints = [[a,b,c,d,e] for a in col1 for b in col2 for c in col3 for d in col4 for e in col5]
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
            for i in removeLines:
                mylinepoints.remove(i)
            if sorted(mylinepoints) != sorted(linepoints[key]):
                print("linepoints有误",key,sorted(mylinepoints),sorted(linepoints[key]))
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
    if response['et']['type'] == 3:  # 判断是否是红利场
        Rpoints = response['et']['data']['lines']
        if len(Rpoints) > 1:#如果有中奖
            paygold = 0
            for rpointIndex in range(len(Rpoints)):
                if rpointIndex + 1 <= 5:#如果是1-4次掉落中奖
                    hl_num = rpointIndex + 1
                else:
                    hl_num = 5
                awardLines = Rpoints[rpointIndex]['awardLines']
                Points = Rpoints[rpointIndex]['points']
                AdPoints = Rpoints[rpointIndex]['adPoints']
                LinePoints = Rpoints[rpointIndex]['linePoints']
                if not checkLinePoints(AdPoints, LinePoints,Points):
                    return False
                for key, value in awardLines.items():  # 遍历中奖符号
                    if key == '13':  # 出现散布图
                        paygold = paygold + (award_dic[(int(key), value)] * betScore) * hl_num  # 直接乘投注的倍数
                    elif key not in WILD_STR:
                        for i in LinePoints[key]:
                            if [Points[X] for X in i].count(14) > 0:#如果包含百搭 翻倍
                                paygold = paygold + award_dic[(int(key), len(i))] * (betScore / 30) * hl_num * 2
                            else:
                                paygold = paygold + award_dic[(int(key), len(i))] * (betScore / 30) * hl_num
                    else:
                        for i in LinePoints[key]:
                            paygold = paygold + award_dic[(int(key), len(i))] * (betScore / 30) * hl_num
                    print(key,paygold)
            if Points == [15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15]:
                paygold = MAXPAYGOLD * betScore/30
            if Points == [14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14]:
                paygold = MAXPAYGOLD * betScore/30
            if paygold > MAXPAYGOLD * betScore/30:
                paygold = MAXPAYGOLD * betScore/30
            current_gold = int(lastNgold + paygold)  # 计算出current——gold
        else:
            current_gold = lastNgold
    elif response['et']['type'] == 1:
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
            if len(i) > len(list(set(i))) and i.count(14) <= 1:
                print("出现重复元素")
                # return False
        AdPoints = Rpoints['adPoints']
        LinePoints = Rpoints['linePoints']
        if len(Rpoints['awardLines']) > 0:  # 如果有中奖
            paygold = 0
            hl_num = 5
            awardLines = Rpoints['awardLines']
            Points = Rpoints['points']
            if not checkLinePoints(AdPoints, LinePoints,Points):
                return False
            for key, value in awardLines.items():  # 遍历中奖符号
                if key == '13':  # 出现散布图
                    paygold = paygold + (award_dic[(int(key), value)] * betScore) * hl_num  # 直接乘投注的倍数
                    # print(paygold)
                elif key not in WILD_STR:
                    for i in LinePoints[key]:
                        if [Points[X] for X in i].count(14) > 0:
                            paygold = paygold + award_dic[(int(key), len(i))] * (betScore / 30) * hl_num * 2
                        else:
                            paygold = paygold + award_dic[(int(key), len(i))] * (betScore / 30) * hl_num
                else:
                    for i in LinePoints[key]:
                        paygold = paygold + award_dic[(int(key), len(i))] * (betScore / 30) * hl_num
                print(key, paygold)
            if Points == [15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15]:
                paygold = MAXPAYGOLD * betScore/30
            if Points == [14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14]:
                paygold = MAXPAYGOLD * betScore/30
            if paygold > MAXPAYGOLD * betScore/30:
                paygold = MAXPAYGOLD * betScore/30
            current_gold = int(lastNgold + paygold)  # 计算出current——gold
        else:
            current_gold = int(lastNgold)
    elif response['et']['type'] == 2:
        Rpoints = response['et']['data']
        points = Rpoints['points']
        if points.count(13) >= 3 or response['et']['data']['isFree']:
            print("免费场中免费场有误")
            exit(-4)
        specMuitNumber = Rpoints['specMuitNumber']
        hl_num = 1
        col1, col2, col3, col4, col5, symbol13_list = getColsSymbol(points)
        list_col1 = [x for x in col1.values()]
        list_col2 = [x for x in col2.values()]
        list_col3 = [x for x in col3.values()]
        list_col4 = [x for x in col4.values()]
        list_col5 = [x for x in col5.values()]
        list_allcols = [list_col1, list_col2, list_col3, list_col4, list_col5]
        for i in list_allcols:
            if len(i) > len(list(set(i))) and i.count(14) <= 1 and i.count(15) <= 1:
                print("出现重复元素")
                # return False
        AdPoints = Rpoints['adPoints']
        LinePoints = Rpoints['linePoints']
        if len(Rpoints['awardLines']) > 0:  # 如果有中奖
            paygold = 0
            awardLines = Rpoints['awardLines']
            Points = Rpoints['points']
            if not checkLinePoints(AdPoints, LinePoints,Points):
                return False
            for key, value in awardLines.items():  # 遍历中奖符号
                if key == '13':  # 出现散布图
                    paygold = paygold + (award_dic[(int(key), value)] * betScore) * hl_num  # 直接乘投注的倍数
                    # print(paygold)
                elif key not in WILD_STR:
                    for i in LinePoints[key]:
                        hl_num = 1
                        for specMuitNumber_value in i:
                            hl_num = hl_num * specMuitNumber.get(str(specMuitNumber_value),1)
                        if [Points[X] for X in i].count(14) > 0:
                            paygold = paygold + award_dic[(int(key), len(i))] * (betScore / 30) * hl_num * 2
                        else:
                            paygold = paygold + award_dic[(int(key), len(i))] * (betScore / 30) * hl_num
                else:
                    for i in LinePoints[key]:
                        hl_num = 1
                        for specMuitNumber_value in i:
                            hl_num = hl_num * specMuitNumber.get(str(specMuitNumber_value),1)
                        paygold = paygold + award_dic[(int(key), len(i))] * (betScore / 30) * hl_num
                print(key, paygold)
            if Points == [15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15]:
                paygold = MAXPAYGOLD * betScore/30
            if Points == [14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14]:
                paygold = MAXPAYGOLD * betScore/30
            if paygold > MAXPAYGOLD * betScore/30:
                paygold = MAXPAYGOLD * betScore/30
            current_gold = int(lastNgold + paygold)  # 计算出current——gold
        else:
            current_gold = int(lastNgold)
    elif response['et']['type'] == 4:
        Rpoints = response['et']['data']
        points = Rpoints['points']
        AdPoints = Rpoints['adPoints']
        LinePoints = Rpoints['linePoints']
        if len(Rpoints['awardLines']) > 0:  # 如果有中奖
            paygold = 0
            hl_num = 1
            awardLines = Rpoints['awardLines']
            Points = Rpoints['points']
            if not checkLinePoints(AdPoints, LinePoints,Points):
                return False
            for key, value in awardLines.items():  # 遍历中奖符号
                if key == '13':  # 出现散布图
                    paygold = paygold + (award_dic[(int(key), value)] * betScore) * hl_num  # 直接乘投注的倍数
                    # print(paygold)
                elif key not in WILD_STR:
                    for i in LinePoints[key]:
                        if [Points[X] for X in i].count(14) > 0:
                            paygold = paygold + award_dic[(int(key), len(i))] * (betScore / 30) * hl_num * 2
                        else:
                            paygold = paygold + award_dic[(int(key), len(i))] * (betScore / 30) * hl_num
                else:
                    for i in LinePoints[key]:
                        paygold = paygold + award_dic[(int(key), len(i))] * (betScore / 30) * hl_num
                print(key, paygold)
            if Points == [15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15]:
                paygold = MAXPAYGOLD * betScore/30
            if Points == [14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14]:
                paygold = MAXPAYGOLD * betScore/30
            if paygold > MAXPAYGOLD * betScore/30:
                paygold = MAXPAYGOLD * betScore/30
            current_gold = int(lastNgold + paygold)  # 计算出current——gold
        else:
            current_gold = int(lastNgold)
    elif response['et']['type'] == 0:
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
            if len(i) > len(list(set(i))) and i.count(14) <= 1:
                print("出现重复元素")
                # return False
        AdPoints = Rpoints['adPoints']
        LinePoints = Rpoints['linePoints']
        if len(Rpoints['awardLines']) > 0:  # 如果有中奖
            paygold = 0
            hl_num = 1
            awardLines = Rpoints['awardLines']
            Points = Rpoints['points']
            if not checkLinePoints(AdPoints, LinePoints,Points):
                return False
            for key, value in awardLines.items():  # 遍历中奖符号
                if key == '13':  # 出现散布图
                    paygold = paygold + (award_dic[(int(key), value)] * betScore) * hl_num  # 直接乘投注的倍数
                    # print(paygold)
                elif key not in WILD_STR:
                    for i in LinePoints[key]:
                        if [Points[X] for X in i].count(14) > 0:
                            paygold = paygold + award_dic[(int(key), len(i))] * (betScore / 30) * hl_num * 2
                        else:
                            paygold = paygold + award_dic[(int(key), len(i))] * (betScore / 30) * hl_num
                else:
                    for i in LinePoints[key]:
                        paygold = paygold + award_dic[(int(key), len(i))] * (betScore / 30) * hl_num
                print(key, paygold)
            if Points == [15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15]:
                paygold = MAXPAYGOLD * betScore/30
            if Points == [14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14]:
                paygold = MAXPAYGOLD * betScore/30
            if paygold > MAXPAYGOLD * betScore/30:
                paygold = MAXPAYGOLD * betScore/30
            current_gold = int(lastNgold + paygold - betScore) # 计算出current——gold
        else:
            current_gold = int(lastNgold - betScore)
    if current_gold != response['et']['nGold']:
        print('筹码错误',paygold,current_gold,response['et']['nGold'])
        return False
    return current_gold
def checkLotteryInitialize(tk,gametype,lastresponse):#核对断线重连初始化
    while True:
        url = "http://192.168.10.212:8001/callInitialize"
        data = {
            "gt": str(gametype),
            "timestamp": 45646545654,
            'actionType': '0'
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

    if response['et']['data']['lastData'] != lastresponse['et']['data']:
        print('断线重连有误',"response['et']['data']['lastData']",response['et']['data']['lastData'],"lastresponse['et']['data']",lastresponse['et']['data'])
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
            for col1_key,col1_value in col1.items():
                if col1_value in WILD:
                    adpoints[key].append(col1_key)
            for col2_key,col2_value in col2.items():
                if col2_value in WILD:
                    adpoints[key].append(col2_key)
            for col3_key,col3_value in col3.items():
                if col3_value in WILD:
                    adpoints[key].append(col3_key)
            for col4_key,col4_value in col4.items():
                if col4_value in WILD:
                    adpoints[key].append(col4_key)
            for col5_key,col5_value in col5.items():
                if col5_value in WILD:
                    adpoints[key].append(col5_key)
        elif len([x for x in adpoints[key] if x in col4.keys()]) > 0:
            for col1_key,col1_value in col1.items():
                if col1_value in WILD:
                    adpoints[key].append(col1_key)
            for col2_key,col2_value in col2.items():
                if col2_value in WILD:
                    adpoints[key].append(col2_key)
            for col3_key,col3_value in col3.items():
                if col3_value in WILD:
                    adpoints[key].append(col3_key)
            for col4_key,col4_value in col4.items():
                if col4_value in WILD:
                    adpoints[key].append(col4_key)
        elif len([x for x in adpoints[key] if x in col3.keys()]) > 0:
            for col1_key,col1_value in col1.items():
                if col1_value in WILD:
                    adpoints[key].append(col1_key)
            for col2_key,col2_value in col2.items():
                if col2_value in WILD:
                    adpoints[key].append(col2_key)
            for col3_key,col3_value in col3.items():
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
        adpoints[13] = symbol13_list
    my_adpoints = {}
    for key, value in adpoints.items():
        my_adpoints[str(key)] = value
    # print("my_adpoints",my_adpoints,"rpoints['adPoints']",rpoints['adPoints'])
    my_adpoints = filterAdpoints(my_adpoints,points)
    for key in my_adpoints.keys():
        if sorted(my_adpoints[key]) != sorted(rpoints['adPoints'].get(key,[])):
            print("adpoints有误",key)
            print('my_adpoints',sorted(my_adpoints[key]),'adpoints',sorted(rpoints['adPoints'].get(key,[])))
            return False
    for key in rpoints['adPoints'].keys():
        if sorted(my_adpoints[key]) != sorted(rpoints['adPoints'].get(key,[])):
            print("adpoints有误",key)
            print('my_adpoints', sorted(my_adpoints[key]), 'adpoints', sorted(rpoints['adPoints'].get(key, [])))
            return False
    return True
def checkAdpoints(response):#核对points
    for rpoints in response['et']['data']['lines']:
        # print(rpoints)
        if not checkAwardSymbol(rpoints):
            return False
        points = copy.deepcopy(rpoints['points'])
        if points.count(13) >= 3:
            print("免费场中免费场有误")
            exit(-4)
        adPoints = rpoints['adPoints']
        if 'myPoints' not in dir():  # myPoints变量未定义
            myPoints = []
            for Symbols in points:
                myPoints.append(Symbols)
            # print(myPoints,"=",points)
        if len(myPoints) != 15 or len(points) != 15:
            print(myPoints,rpoints['points'])
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
def normalPlay(tokenid,gametype,betScore):#正常玩模式
    url = "http://192.168.10.212:8001/getSlotData"
    millis = str(int(round(time.time() * 1000)))
    headers = {
        'token': tokenid,
        'Content-Type': 'application/json'
    }
    data = {
        "gt": str(gametype),
        "betScore": str(betScore),
        "actionType": "0",
        "timestamp": millis,
        'token': tokenid,
        'freeType': "0"
    }
    data = json.dumps(data)
    try:
        response = session.post(url, data=data,headers = headers)
        response = response.json()
        print(response)
        if response.get("code") == 20000:
            # print(response)
            return response
        elif response.get("code") == 20001:
            print(response)
            exit(-2)
        else:
            with open('error.txt','a')as f:
                f.write('\n'+ response)
            print("error",response)
    except:
        pass
    return None
def freeSpin4(tokenid,gametype,betScore,maxfreetype):#选择红利4
    print("选择红利")
    while True:
        url = "http://192.168.10.212:8001/getSlotData"
        millis = int(round(time.time() * 1000))
        game_type = str(random.randint(1,maxfreetype))
        headers = {
            'token': tokenid,
            'Content-Type': 'application/json'
        }
        data = {
            "tk":"null",
            "gt":gametype,
            "freeType":game_type,
            "betScore":betScore,
            "actionType":0,
            "timestamp":millis
            }
        data = json.dumps(data)
        try:
            response = session.post(url, data=data,headers = headers)
            response = response.json()
            print(response)
            if response.get("code") == 20000:
                break
        except:
            pass
def call(tk,gametype):
    url = "http://192.168.10.212:8001/callInitialize"
    data = {
            "gt":str(gametype),
            "timestamp": 45646545654,
            'actionType': '0'
            }
    headers = {
        'token': tk,
        'Content-Type': 'application/json'
        }
    data = json.dumps(data)
    print("初始化",data,headers)
    response = requests.post(url=url, data=data, headers=headers)
    response = response.json()
    print("初始化",response)
def register():
    url = "http://192.168.10.212:8001/registerUser"
    headers = {
        'Content-Type': 'application/json'
    }
    registerResponse = requests.get(url, headers=headers)
    print(registerResponse.json())
    username = registerResponse.json()['et'].get("username")
    password = "123456"
    if username:
        print(username,password)
        return username,password
    return None
def getToken(username,password):
    data = {
            "userName": username,
            "password": password
    }
    headers = {
        'Content-Type': 'application/json'
    }
    data = json.dumps(data)
    url = "http://192.168.10.212:8002/callToken"
    tokenResponse = requests.post(url = url, data = data, headers = headers)
    token = tokenResponse.json().get("ms")
    print(token)
    if token:
        return token
    return None
def java_login(username,password,style = 5):
    while True:
        url = f"http://192.168.10.212:8001/login?username={username}&password={password}&style={style}"
        headers = {
            'Content-Type': 'application/json;charset=UTF-8'
        }
        loginResponse = session.post(url,headers)
        loginResponse = loginResponse.json()
        print("登录",loginResponse)
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
            infoResponse = session.get(url = url,headers = headers)
            infoResponse = infoResponse.json()
            print("获取用户信息",infoResponse)
            return token
def main():#主函数 程序入口
    username, password = register()
    print("this",username,password)
    tk = java_login(username, password)
    tokenid = tk
    gameType = GT
    betScore = 30
    call(tokenid, gameType)
    # pay_response = requests.get(url=f"http://192.168.10.212:8002/pay/{username}/50000000")
    while True:
        response = normalPlay(tokenid=tokenid, gametype=gameType,betScore = betScore)
        if response:
            if not checkLotteryInitialize(tk=tokenid, gametype=gameType, lastresponse=response):  # 核对断线重连初始化
                return
            if 'lastNgold' not in dir():  # 如果是第一次运行脚本
                lastNgold = response['et']['nGold']
                lastachievement = response['et']['data']['achievement']
                if response['et']['data'].get('isFree', False) and response['et']['data']['type'] == 0:
                    if response['et']['data']['plan'] > 15:
                        maxfreetype = 4
                    elif response['et']['data']['plan'] > 10:
                        maxfreetype = 3
                    elif response['et']['data']['plan'] > 5:
                        maxfreetype = 2
                    else:
                        maxfreetype = 1
                    freeSpin4(tokenid, gametype=gameType,betScore=betScore,maxfreetype = maxfreetype)
                elif response['et']['type'] == 3:
                    if not checkAdpoints(response):
                        break
                elif response['et']['type'] == 2:
                    points = response['et']['data']['points']
                    specMuitNumber = response['et']['data']['specMuitNumber']
                    if specMuitNumber:
                        for specMuitNumber_key, specMuitNumber_value in specMuitNumber.items():
                            points[int(specMuitNumber_key)] = 15
                elif response['et']['type'] == 4:
                    points = response['et']['data']['points']
                    infectPoint = response['et']['data']['infectPoint']
                    if infectPoint:
                        for infectPoint_value in infectPoint:
                            points[infectPoint_value] = 15
                if response['et']['type'] != 3:
                    if not checkAwardSymbol(response['et']['data']):
                        exit(-3)
            else:
                # if not checkLotteryInitialize(tk=tokenid, gametype=gameType,lastresponse = response):#核对断线重连初始化
                #     break
                if response['et']['data'].get('isFree', False) and response['et']['data']['type'] == 0:
                    if response['et']['data']['plan'] > 15:
                        maxfreetype = 4
                    elif response['et']['data']['plan'] > 10:
                        maxfreetype = 3
                    elif response['et']['data']['plan'] > 5:
                        maxfreetype = 2
                    else:
                        maxfreetype = 1
                    freeSpin4(tokenid, gametype=gameType, betScore=betScore, maxfreetype=maxfreetype)
                elif response['et']['type'] == 3:
                    if not checkAdpoints(response):
                        break
                elif response['et']['type'] == 2:
                    points = response['et']['data']['points']
                    specMuitNumber = response['et']['data']['specMuitNumber']
                    if specMuitNumber:
                        for specMuitNumber_key, specMuitNumber_value in specMuitNumber.items():
                            points[int(specMuitNumber_key)] = 15
                elif response['et']['type'] == 4:
                    points = response['et']['data']['points']
                    infectPoint = response['et']['data']['infectPoint']
                    if infectPoint:
                        for infectPoint_value in infectPoint:
                            points[infectPoint_value] = 15
                if response['et']['type'] != 3:
                    if not checkAwardSymbol(response['et']['data']):
                        exit(-3)
                    lastachievement = checkachievement(response, lastachievement)
                    if lastachievement == False:
                        break
                lastNgold = checkNgold(response, betScore, lastNgold)
                if lastNgold == False:
                    break
if __name__ == '__main__':
    main()

