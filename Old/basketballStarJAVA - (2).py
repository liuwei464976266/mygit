#encoding:utf-8
import requests, json, threading, time, random,datetime
import operator
from functools import reduce
from queue import Queue
import copy
WILD = [11]
WILD_STR = ['11']
SCATTER = '10'
MAXPAYGOLD = 364500
session = requests.session()
GT = 141
LINESNUMBER = 50
BET = 50
INITURL = 'http://192.168.10.213:9008/callInitialize'
SLOTURL = 'http://192.168.10.25:9008/getSlotData'
REGISTERURL = 'http://192.168.10.213:9000/registerUser'
def filterAdpoints(adpoints,points):
    filtedAdpoints = {}
    myadpoints = copy.deepcopy(adpoints)  # 拷贝一个 myadpoints 避免后续直接修改adpoints对象
    myDicAdpoints = {}
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
            print(key, 'removeLines filter', removeLines)
            for i in removeLines:
                mylinepoints.remove(i)
            myListAdpoints = []
            for i in mylinepoints:
                myListAdpoints += i
            myListAdpoints = list(set(myListAdpoints))
            myDicAdpoints[key] = myListAdpoints
        else:
            myDicAdpoints[SCATTER] = value
    print("返回adpoints",myDicAdpoints)
    return myDicAdpoints
def checkachievement(response,lastachievement):
    print('lastachievement',lastachievement)
    if response['et']['data']['type'] == 0:
        achievement = copy.deepcopy(lastachievement)
        print('achievement',achievement)
        addAchievement_flag = False
        rpoints =  copy.deepcopy(response['et']['data']['lines'])
        for lines in rpoints:
            awardlins = lines['awardLines']
            adPoints = lines['adPoints']
            linePoints = lines['linePoints']
            points_list = lines['points']
            if response['et']['type'] == 0 and len(awardlins) != 0:
                copy_linePoints = {}
                for key, value in awardlins.items():
                    if key in linePoints:
                        copy_linePoints[key] = linePoints[key]
                    else:
                        copy_linePoints[key] = [adPoints[key]]
                    for award_symbol_index_list in copy_linePoints[key]:
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
                                    if int(key) != 11:
                                        if len(achievement[key]) == 3:
                                            addAchievement_flag = True
                                            if key not in rpoints[-1]['addAchievement']:
                                                print("成就错误", key)
                                                return False
                            else:
                                achievement[key] = {str(value): 1}
        if achievement != rpoints[-1]['achievement'] and ((achievement == {} and not rpoints[-1]['achievement'] is None) or (achievement != {} and rpoints[-1]['achievement'] is None)):
            print("成就错误1", "myachievement",achievement,"response",rpoints[-1]['achievement'])
            return False
        if addAchievement_flag == False:
            if rpoints[-1]['addAchievement']:
                if len(rpoints[-1]['addAchievement']) > 0:
                    print("成就错误2", rpoints[-1]['addAchievement'])
                    return False
        else:
            if rpoints[-1]['addAchievement']:
                if len(rpoints[-1]['addAchievement']) <= 0:
                    print("成就错误2", rpoints[-1]['addAchievement'])
                    return False
            if not rpoints[-1]['addAchievement']:
                print("成就错误2", rpoints[-1]['addAchievement'])
                return False
        print('返回achievement',achievement)
        return achievement
    else:
        print('返回lastachievement', lastachievement)
        return lastachievement
def checkLinePoints(adpoints,linepoints,points,type):#核对LinePoints
    myadpoints = copy.deepcopy(adpoints)#拷贝一个 myadpoints 避免后续直接修改adpoints对象
    for key,value in myadpoints.items():
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
                mylinepoints = [[a,b,c,d,e] for a in col1 for b in col2 for c in col3 for d in col4 for e in col5]
            elif len(col4) > 0:
                mylinepoints = [[a, b, c, d] for a in col1 for b in col2 for c in col3 for d in col4]
            elif len(col3) > 0:
                mylinepoints = [[a, b, c] for a in col1 for b in col2 for c in col3]
            else:
                mylinepoints = []
            removeLines = []
            for i in mylinepoints:
                if len([x for x in i if points[x] not in WILD]) <= 0 and key not in WILD_STR:#非百搭点位个数为0同时key不为百搭时删除该连线
                    removeLines.append(i)
            for i in removeLines:
                mylinepoints.remove(i)
            if sorted(mylinepoints) != sorted(linepoints[key]):
                print("linepoints有误",key,sorted(mylinepoints),sorted(linepoints[key]))
                return False
        else:
            if key in linepoints and type == 0:
                print("linepoints有误包含符号13")
                return False
    return True
def getCurrentGold(Rpoints,type):
    pass
def checkNgold(response,betScore,lastNgold):#核对Ngold和checkLinePoints
    award_dic = {
        (1, 3): 2,
        (2, 3): 5,
        (3, 3): 8,
        (4, 3): 8,
        (5, 3): 10,
        (6, 3): 12,
        (7, 3): 15,
        (8, 3): 20,
        (9, 3): 30,
        (10, 3): 5,
        (1, 4): 15,
        (2, 4): 20,
        (3, 4): 25,
        (4, 4): 30,
        (5, 4): 50,
        (6, 4): 60,
        (7, 4): 75,
        (8, 4): 80,
        (9, 4): 100,
        (10, 4): 50,
        (1, 5): 70,
        (2, 5): 80,
        (3, 5): 100,
        (4, 5): 120,
        (5, 5): 125,
        (6, 5): 150,
        (7, 5): 250,
        (8, 5): 300,
        (9, 5): 600,
        (10, 5): 250,
    }
    if response['et']['type'] == 0:  # 判断是否是红利场
        Rpoints = response['et']['data']['lines']
        if len(Rpoints[0]['awardLines']) > 0:#如果有中奖
            paygold = 0
            for rpointIndex in range(len(Rpoints)):
                hl_num = 1
                awardLines = Rpoints[rpointIndex]['awardLines']
                Points = Rpoints[rpointIndex]['points']
                AdPoints = Rpoints[rpointIndex]['adPoints']
                LinePoints = Rpoints[rpointIndex]['linePoints']
                copyGold = Rpoints[rpointIndex]['gold']
                if not checkLinePoints(AdPoints, LinePoints,Points,type = 0):
                    return False
                payLinesGold = 0
                for key, value in awardLines.items():  # 遍历中奖符号
                    if key == SCATTER:  # 出现散布图
                        payLinesGold = payLinesGold + (award_dic[(int(key), value)] * betScore) * hl_num  # 直接乘投注的倍数
                    elif key not in WILD_STR:
                        for i in LinePoints[key]:
                            payLinesGold = payLinesGold + award_dic[(int(key), len(i))] * (betScore / LINESNUMBER) * hl_num
                paygold = paygold + payLinesGold
                print(key, payLinesGold)
                if int(payLinesGold) != copyGold:
                    print('gold错误', 'payLinesGold', payLinesGold, 'copyGold', copyGold)
                    exit(-7)
            current_gold = int(lastNgold + paygold) - betScore# 计算出current——gold
        else:
            paygold = 0
            current_gold = lastNgold - betScore
    else:
        Rpoints = response['et']['data']['lines']
        if len(Rpoints[0]['awardLines']) > 0:  # 如果有中奖
            paygold = 0
            for rpointIndex in range(len(Rpoints)):
                if rpointIndex + 1 <= 5:  # 如果是1-4次掉落中奖
                    hl_num = rpointIndex + 1
                else:
                    hl_num = 10
                awardLines = Rpoints[rpointIndex]['awardLines']
                Points = Rpoints[rpointIndex]['points']
                AdPoints = Rpoints[rpointIndex]['adPoints']
                LinePoints = Rpoints[rpointIndex]['linePoints']
                copyGold = Rpoints[rpointIndex]['gold']
                if not checkLinePoints(AdPoints, LinePoints, Points,type = 1):
                    return False
                payLinesGold = 0
                for key, value in awardLines.items():  # 遍历中奖符号
                    if key == SCATTER:  # 出现散布图
                        payLinesGold = payLinesGold + (award_dic[(int(key), value)] * betScore) * hl_num  # 直接乘投注的倍数
                    elif key not in WILD_STR:
                        for i in LinePoints[key]:
                            payLinesGold = payLinesGold + award_dic[(int(key), len(i))] * (betScore / LINESNUMBER) * hl_num
                paygold = paygold + payLinesGold
                print(key, payLinesGold)
                if int(payLinesGold) != copyGold:
                    print('gold错误','payLinesGold',payLinesGold,'copyGold',copyGold)
                    exit(-7)
            current_gold = int(lastNgold + paygold)  # 计算出current——gold
        else:
            paygold = 0
            current_gold = lastNgold
    if paygold != response['et']['gold']:
        print('allgold错误','paygold',paygold,'gold',response['et']['gold'])
        return False
    if current_gold != response['et']['nGold']:
        print('筹码错误',paygold,current_gold,response['et']['nGold'])
        return False
    return current_gold
def checkLotteryInitialize(tk,gametype,lastresponse):#核对断线重连初始化
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
    print('核对断线重连',response)
    if response['et']['data']['lastData'] != lastresponse['et']['data']:
        print('断线重连有误',"response['et']['data']['lastData']",response['et']['data']['lastData'],"lastresponse['et']['data']",lastresponse['et']['data'])
        return False
    if response['et']['data']['lineNumber'] != LINESNUMBER:
        print('线数错误', "response['et']['data']['lineNumber']", response['et']['data']['lineNumber'])
        return False
    if response['et']['data']['parValue'] != [0.01, 0.02, 0.05, 0.1]:
        print('面额错误', "response['et']['data']['parValue']", response['et']['data']['parValue'])
        return False
    if response['et']['data']['quantityData'] != [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        print('数量错误', "response['et']['data']['quantityData']", response['et']['data']['quantityData'])
        return False
    if response['et']['data']['lastData']['residue'] != response['et']['data']['freeCount']:
        print('免费次数错误', "response['et']['data']['lastData']['residue']", response['et']['data']['lastData']['residue'])
        print("response['et']['data']['freeCount']",response['et']['data']['freeCount'])
        return False
    if response['et']['data']['lastData']['freeGold'] != response['et']['data']['freeGold']:
        print('freegold错误', "response['et']['data']['lastData']['freeGold']", response['et']['data']['lastData']['freeGold'])
        print("response['et']['data']['freeGold']",response['et']['data']['freeGold'])
        return False
    if response['et']['data']['initQuantity'] != BET:
        print('初始筹码错误',"response['et']['data']['initQuantity']",response['et']['data']['initQuantity'])
        return False
    if response['et']['data']['lastData']['bonusGold'] != response['et']['data']['bonusGold']:
        print('bonusGold错误', "response['et']['data']['lastData']['bonusGold']", response['et']['data']['lastData']['bonusGold'])
        print("response['et']['data']['bonusGold']",response['et']['data']['bonusGold'])
        return False
    if response['et']['data']['bonusGold'] > 0 and (response['et']['data']['lastData']['isFree'] == False and response['et']['data']['lastData']['type'] == 0):
        print('bonusGold错误1')
        return False
    if response['et']['data']['bonusGold'] == 0 and (response['et']['data']['lastData']['isFree'] == True or response['et']['data']['lastData']['type'] != 0):
        print('bonusGold错误2')
        return False
    if response['et']['data']['type'] != response['et']['data']['lastData']['type'] and (response['et']['data']['lastData']['isFree'] == False and ((response['et']['data']['lastData']['residue'] != 0 and response['et']['data']['lastData']['type'] == 1 ) or (response['et']['data']['lastData']['residue'] == 0 and response['et']['data']['lastData']['type'] == 0 ))):
        print('type错误')
        return False
    if response['et']['data']['lastData']['lines'][-1]['achievement'] != response['et']['data']['achievement']:
        print('断线重连成就错误')
        return False
    return True
def getColsSymbol(points):#取出各列中奖位置
    symbol13_list = []
    col1, col2, col3, col4, col5 = {}, {}, {}, {}, {}
    for i in range(len(points)):
        if points[i] == int(SCATTER):
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
def checkAwardSymbol(rpoints,targ,type):#核对adpoints
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
    if 11 in adpoints:
        adpoints.pop(11)
    if len(symbol13_list) >= 3:
        adpoints[SCATTER] = symbol13_list
    my_adpoints = {}
    for key, value in adpoints.items():
        my_adpoints[str(key)] = value
    # print("my_adpoints",my_adpoints,"rpoints['adPoints']",rpoints['adPoints'])
    my_adpoints = filterAdpoints(my_adpoints,points)
    if type == 0:
        for key in my_adpoints.keys():
            if key != SCATTER:
                if sorted(my_adpoints[key]) != sorted(rpoints['adPoints'].get(key,[])):
                    print(key,"adpoints有误")
                    print('my_adpoints',sorted(my_adpoints[key]),'adpoints',sorted(rpoints['adPoints'].get(key,[])))
                    return False
            else:
                if sorted(my_adpoints[key]) != sorted(rpoints['adPoints'].get(key,[])) and targ:
                    print(key,"adpoints有误",'targ',targ)
                    print('my_adpoints',sorted(my_adpoints[key]),'adpoints',sorted(rpoints['adPoints'].get(key,[])))
                    return False
                if sorted(my_adpoints[key]) == sorted(rpoints['adPoints'].get(key,[])) and not targ:
                    print(key,"adpoints有误",'targ',targ)
                    print('my_adpoints',sorted(my_adpoints[key]),'adpoints',sorted(rpoints['adPoints'].get(key,[])))
                    return False
        for key in rpoints['adPoints'].keys():
            if key != SCATTER:
                if sorted(my_adpoints[key]) != sorted(rpoints['adPoints'].get(key,[])):
                    print(key,"adpoints有误")
                    print('my_adpoints', sorted(my_adpoints[key]), 'adpoints', sorted(rpoints['adPoints'].get(key, [])))
                    return False
            else:
                if sorted(my_adpoints[key]) != sorted(rpoints['adPoints'].get(key,[])) and targ:
                    print(key,"adpoints有误",'targ',targ)
                    print('my_adpoints',sorted(my_adpoints[key]),'adpoints',sorted(rpoints['adPoints'].get(key,[])))
                    return False
                if sorted(my_adpoints[key]) == sorted(rpoints['adPoints'].get(key,[])) and not targ:
                    print(key,"adpoints有误",'targ',targ)
                    print('my_adpoints',sorted(my_adpoints[key]),'adpoints',sorted(rpoints['adPoints'].get(key,[])))
                    return False
    else:
        for key in my_adpoints.keys():
            if sorted(my_adpoints[key]) != sorted(rpoints['adPoints'].get(key,[])):
                print(key,"adpoints有误")
                print('my_adpoints',sorted(my_adpoints[key]),'adpoints',sorted(rpoints['adPoints'].get(key,[])))
                return False
        for key in rpoints['adPoints'].keys():
            if sorted(my_adpoints[key]) != sorted(rpoints['adPoints'].get(key,[])):
                print(key,"adpoints有误")
                print('my_adpoints', sorted(my_adpoints[key]), 'adpoints', sorted(rpoints['adPoints'].get(key, [])))
                return False
    return True
def checkAdpoints(response):#核对points和checkAwardSymbol
    indexLines = 0
    type = response['et']['data']['type']
    for rpoints in response['et']['data']['lines']:
        indexLines += 1
        # print(rpoints)
        if indexLines == len(response['et']['data']['lines']):
            targ = True
        else:
            targ = False
        if not checkAwardSymbol(rpoints,targ,type):
            return False
        points = copy.deepcopy(rpoints['points'])
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
        print("myPoints", myPoints)
        print("points", points)
        for i in range(len(myPoints)):
            if myPoints[i] != 'randomSymbol' and myPoints[i] != points[i]:
                print("结果错误","myPoints", myPoints,"points", points)
                return False
        # print(rpoints)
        myPoints = copy.deepcopy(points)
        award_index_list = []
        scatter_index_list = []
        if response['et']['data']['type'] != 1:
            for key,index_list in adPoints.items():
                if key != SCATTER:
                    award_index_list = award_index_list + index_list
                else:
                    scatter_index_list = scatter_index_list + index_list
        else:
            for key, index_list in adPoints.items():
                award_index_list = award_index_list + index_list
        # if len(scatter_index_list) > 0 and len(award_index_list) > 0:
        #     exit(-5)
        award_index_list = list(set(award_index_list))#中奖下标列表去重
        award_index_list = sorted(award_index_list)#中奖下标列表排序
        print('award_index_list', award_index_list)
        print(points)
        for award_index in award_index_list:
            if award_index < 5:
                myPoints[award_index] = "randomSymbol"#如果第一行有中奖，该位置为随机符号
            elif 5 <= award_index < 10 :
                myPoints[award_index] = myPoints[award_index - 5]#该位置为第一行符号
                myPoints[award_index - 5] = "randomSymbol"#第一行为随机符号
            elif 10 <= award_index <= 14 :
                myPoints[award_index] = myPoints[award_index - 5]#第三行为第二行符号
                myPoints[award_index - 5] = myPoints[award_index - 10]#第二行为第一行符号
                myPoints[award_index - 10] = "randomSymbol"#第一行为随机符号
    return True
def normalPlay(tokenid,gametype,betScore):#正常玩模式
    url = SLOTURL
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
def call(tk,gametype):
    url = INITURL
    data = {
            "gt":str(gametype),
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
    print("初始化",response)
def registerJava():
    url = REGISTERURL
    headers = {
        'Content-Type': 'application/json'
    }
    registerResponse = requests.get(url, headers=headers)
    print(registerResponse.json())
    username = registerResponse.json()['et'].get("username")
    password = "123456"
    if username:
        print(username,password)
        return username, password
    return None
def register():
    url = "http://192.168.10.25:9000/registerUser"
    headers = {
        'Content-Type': 'application/json'
    }
    registerResponse = requests.get(url, headers=headers)
    print(registerResponse.json())
    tokenId = registerResponse.json()['et'].get("uid")
    if tokenId:
        print(tokenId)
        return tokenId
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
    url = "http://192.168.10.213:8002/callToken"
    tokenResponse = requests.post(url = url, data = data, headers = headers)
    token = tokenResponse.json().get("ms")
    print(token)
    if token:
        return token
    return None
def java_login(username,password,style = 5):
    while True:
        url = f"http://192.168.10.213:8002/login?username={username}&password={password}&style={style}"
        headers = {
            'Content-Type': 'application/json;charset=UTF-8'
        }
        loginResponse = session.post(url,headers)
        loginResponse = loginResponse.json()
        print("登录",loginResponse)
        if loginResponse['code'] == 20000:
            url = 'http://192.168.10.213:8002/selectGame'
            token = loginResponse['et']['uid']
            headers = {
                'token': token,
                'Content-Type': 'application/json;charset=UTF-8'
            }
            selectResponse = session.post(url=url, headers=headers)
            url = 'http://192.168.10.213:8002/getUserInfo'
            headers = {
                'token': token,
            }
            infoResponse = session.get(url = url,headers = headers)
            infoResponse = infoResponse.json()
            print("获取用户信息",infoResponse)
            return token
# def checkNgold(response,betScore,lastNgold):#核对Ngold和checkLinePoints
#     award_dic = {
#         (1, 3): 2,
#         (2, 3): 5,
#         (3, 3): 8,
#         (4, 3): 8,
#         (5, 3): 10,
#         (6, 3): 12,
#         (7, 3): 15,
#         (8, 3): 20,
#         (9, 3): 30,
#         (10, 3): 5,
#         (1, 4): 15,
#         (2, 4): 20,
#         (3, 4): 25,
#         (4, 4): 30,
#         (5, 4): 50,
#         (6, 4): 60,
#         (7, 4): 75,
#         (8, 4): 80,
#         (9, 4): 100,
#         (10, 4): 50,
#         (1, 5): 70,
#         (2, 5): 80,
#         (3, 5): 100,
#         (4, 5): 120,
#         (5, 5): 125,
#         (6, 5): 150,
#         (7, 5): 250,
#         (8, 5): 300,
#         (9, 5): 600,
#         (10, 5): 250,
#     }
#     if response['et']['type'] == 0:  # 判断是否是红利场
#         Rpoints = response['et']['data']['lines']
#         if len(Rpoints[0]['awardLines']) > 0:#如果有中奖
#             paygold = 0
#             for rpointIndex in range(len(Rpoints)):
#                 hl_num = 1
#                 awardLines = Rpoints[rpointIndex]['awardLines']
#                 Points = Rpoints[rpointIndex]['points']
#                 AdPoints = Rpoints[rpointIndex]['adPoints']
#                 LinePoints = Rpoints[rpointIndex]['linePoints']
#                 if not checkLinePoints(AdPoints, LinePoints,Points):
#                     return False
#                 for key, value in awardLines.items():  # 遍历中奖符号
#                     if key == SCATTER:  # 出现散布图
#                         paygold = paygold + (award_dic[(int(key), value)] * betScore) * hl_num  # 直接乘投注的倍数
#                     elif key not in WILD_STR:
#                         for i in LinePoints[key]:
#                             paygold = paygold + award_dic[(int(key), len(i))] * (betScore / LINESNUMBER) * hl_num
#                     print(key,paygold)
#             current_gold = int(lastNgold + paygold) - betScore# 计算出current——gold
#         else:
#             paygold = 0
#             current_gold = lastNgold - betScore
#     else:
#         Rpoints = response['et']['data']['lines']
#         if len(Rpoints[0]['awardLines']) > 0:  # 如果有中奖
#             paygold = 0
#             for rpointIndex in range(len(Rpoints)):
#                 if rpointIndex + 1 <= 5:  # 如果是1-4次掉落中奖
#                     hl_num = rpointIndex + 1
#                 else:
#                     hl_num = 5
#                 awardLines = Rpoints[rpointIndex]['awardLines']
#                 Points = Rpoints[rpointIndex]['points']
#                 AdPoints = Rpoints[rpointIndex]['adPoints']
#                 LinePoints = Rpoints[rpointIndex]['linePoints']
#                 if not checkLinePoints(AdPoints, LinePoints, Points):
#                     return False
#                 for key, value in awardLines.items():  # 遍历中奖符号
#                     if key == SCATTER:  # 出现散布图
#                         paygold = paygold + (award_dic[(int(key), value)] * betScore) * hl_num  # 直接乘投注的倍数
#                     elif key not in WILD_STR:
#                         for i in LinePoints[key]:
#                             paygold = paygold + award_dic[(int(key), len(i))] * (betScore / LINESNUMBER) * hl_num
#                     print(key, paygold)
#             current_gold = int(lastNgold + paygold)  # 计算出current——gold
#         else:
#             paygold = 0
#             current_gold = lastNgold
#     if current_gold != response['et']['nGold']:
#         print('筹码错误',paygold,current_gold,response['et']['nGold'])
#         return False
#     return current_gold
def main():#主函数 程序入口
    # username,password = registerJava()
    # print("this", username, password)
    # tk = java_login(username, password)
    tk = '17ADD64C335AC0DA1E8498BE3DD248045CC9'
    tokenid = tk
    gameType = GT
    betScore = BET
    call(tokenid, gameType)
    while True:
        response = normalPlay(tokenid=tokenid, gametype=gameType,betScore = betScore)
        if response:
            if response['et']['type'] == 0 and response['et']['data']['isFree'] == False:
                if not checkLotteryInitialize(tk=tokenid, gametype=gameType, lastresponse=response):  # 核对断线重连初始化
                    return
                if not checkAdpoints(response):
                    exit(-4)
                if 'lastNgold' not in dir():  # 如果是第一次运行脚本
                    lastNgold = response['et']['nGold']
                    lastachievement = response['et']['data']['lines'][-1]['achievement']
                    if not lastachievement:
                        lastachievement = {}
                else:
                    lastachievement = checkachievement(response, lastachievement)
                    if lastachievement == False:
                        return
                    lastNgold = checkNgold(response, betScore, lastNgold)
                    if lastNgold == False:
                        return
            else:
                if response['et']['data']['bonusGold'] == 0:
                    print("bonusGold有误", response['et']['data']['bonusGold'])
                    return
                if not checkAdpoints(response):
                    exit(-4)
                if not checkLotteryInitialize(tk=tokenid, gametype=gameType, lastresponse=response):  # 核对断线重连初始化
                    return
                if 'lastnGold' not in dir():  # 如果是第一次运行脚本
                    bonusGold = response['et']['data']['bonusGold']
                    lastNgold = response['et']['nGold']
                    lastachievement = response['et']['data']['lines'][-1]['achievement']
                    if not lastachievement:
                        lastachievement = {}
                else:
                    lastachievement = checkachievement(response, lastachievement)
                    if lastachievement == False:
                        return
                    lastNgold = checkNgold(response, betScore, lastNgold)
                    if lastNgold == False:
                        return
                if response['et']['type'] == 1:
                    myfreegold = response['et']['data']['lines'][-1]['freeGold']
                    fsTimes = response['et']['data']['lines'][-1]['residue']
                elif response['et']['data']['isFree'] == True:
                    bonusGold = response['et']['data']['gold']
                    fsTimes = response['et']['data']['lines'][-1]['points'].count(10) * 5
                    myfreegold = 0
                playedTimes = 1
                while playedTimes <= fsTimes:
                    response = normalPlay(tokenid=tokenid, gametype=gameType, betScore=betScore)
                    if response:
                        if bonusGold != response['et']['data']['bonusGold']:
                            exit(-6)
                            print('bonusGold错误')
                        myfreegold += response['et']['data']['gold']
                        if myfreegold != response['et']['data']['lines'][-1]['freeGold']:
                            print("freegold错误", myfreegold, response['et']['data']['lines'][-1]['freeGold'])
                            return
                        if not checkAdpoints(response):
                            return
                        if not checkLotteryInitialize(tk=tokenid, gametype=gameType,
                                                      lastresponse=response):  # 核对断线重连初始化
                            return
                        if response['et']['type'] != 1:
                            print("红利错误", playedTimes, fsTimes)
                            return
                        # fsTimes += response['et']['data']['lines'][-1]['plan']
                        lastachievement = checkachievement(response, lastachievement)
                        if lastachievement == False:
                            return
                        lastNgold = checkNgold(response, betScore, lastNgold)
                        if lastNgold == False:
                            return
                    if response['et']['data']['lines'][-1]['residue'] + playedTimes != fsTimes:
                        print("红利错误", playedTimes, fsTimes)
                        return
                    playedTimes += 1


if __name__ == '__main__':
    main()

