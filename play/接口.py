#encoding:utf-8
import requests, json, threading, time, random,datetime
import operator
from functools import reduce
from queue import Queue
import copy
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
GT = 136
def checklinePoints(adPoints,linePoints):#核对linePoints
    myadPoints = copy.deepcopy(adPoints)#拷贝一个 myadPoints 避免后续直接修改adPoints对象
    for key,value in myadPoints.items():
        if key != '12':
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
                mylinePoints = [[a,b,c,d,e] for a in col1 for b in col2 for c in col3 for d in col4 for e in col5]
            elif len(col4) > 0:
                mylinePoints = [[a, b, c, d] for a in col1 for b in col2 for c in col3 for d in col4]
            elif len(col3) > 0:
                mylinePoints = [[a, b, c] for a in col1 for b in col2 for c in col3]
            elif len(col2) > 0:
                mylinePoints = [[a, b] for a in col1 for b in col2]
            else:
                mylinePoints = []
            if sorted(mylinePoints) != sorted(linePoints[key]):
                print("linePoints有误",sorted(mylinePoints),sorted(linePoints[key]))
                return False
        else:
            if key in linePoints:
                print("linePoints有误包含符号12")
                return False
    return True
def checkFsPoints(response,colNum,lastpoints):
    mypoints = copy.deepcopy(lastpoints)
    points = response['et']['data']['points']
    for i in range(len(mypoints)):
        if i % 5 == colNum - 1:
            mypoints[i] = "randomSymbol"
    if len(mypoints) == len(points):
        for i in range(len(mypoints)):
            if mypoints[i] != "randomSymbol" and mypoints[i] != points[i]:
                print("单轴旋转points错误",points,lastpoints)
                return False
    else:
        print("points长度错误",points,lastpoints)
        return False
    return points
def checknGold(response,betScore,lastnGold):#核对nGold
    if GT == 134:
        AWARD_DIC = ZR_AWARD_DIC
    elif GT == 130 or GT==131 or GT==136:
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
    if not checklinePoints(adPoints, linePoints):
        return False
    if len(awardlins) > 0:
        for key, value in awardlins.items():  # 遍历中奖符号
            if key == '12':  # 出现散布图
                paygold = paygold + (AWARD_DIC[(int(key), value)] * betScore) * hl_num  # 直接乘投注的倍数
            else:
                for i in linePoints[key]:
                    paygold = paygold + AWARD_DIC[(int(key), len(i))] * (betScore / 25) * hl_num
    current_gold = int(lastnGold + paygold)  # 计算出current——gold
    if response['et']['type'] == 0:  # 判断是否是红利场
        paygold = paygold + betScore  # 如果不是红利场，则+底注
    if paygold != response['et']['gold']:
        print('gold错误',paygold,current_gold,response['et']['nGold'])
        return False
    if current_gold != response['et']['nGold']:
        print('筹码错误',paygold,current_gold,response['et']['nGold'])
        return False
    return current_gold
def checkFsnGold(response,betScore,lastnGold,mybetScore):#核对nGold
    if GT == 134:
        AWARD_DIC = ZR_AWARD_DIC
    elif GT == 130 or GT==131 or GT==136:
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
    if not checklinePoints(adPoints, linePoints):
        return False
    if len(awardlins) > 0:
        for key, value in awardlins.items():  # 遍历中奖符号
            if key == '12':  # 出现散布图
                paygold = paygold + (AWARD_DIC[(int(key), value)] * mybetScore) * hl_num  # 直接乘投注的倍数
            else:
                for i in linePoints[key]:
                    paygold = paygold + AWARD_DIC[(int(key), len(i))] * (mybetScore / 25) * hl_num
    current_gold = int(lastnGold + paygold)  # 计算出current——gold
    if response['et']['type'] == 0:  # 判断是否是红利场
        paygold = paygold + betScore  # 如果不是红利场，则+底注
    if paygold != response['et']['gold']:
        print('gold错误',paygold,current_gold,response['et']['nGold'])
        return False
    if current_gold != response['et']['nGold']:
        print('筹码错误',paygold,current_gold,response['et']['nGold'])
        return False
    return current_gold
def checkLotteryInitialize(tk,gametype,lastresponse):#核对断线重连初始化
    while True:
        url = "http://192.168.10.212:8002/callInitialize"
        millis = int(round(time.time() * 1000))
        data = {
                "gt":gametype,
                "timestamp":millis,
                'actionType': '0'
                }
        headers = {
            'token':tk,
            'Content-Type': 'application/json'
        }
        data = json.dumps(data)
        response = requests.post(url = url, data = data,headers = headers)
        response = response.json()
        # print("init",response)
        if response['code'] == 20000:
            break
    # print(response['et']['data']['lastData'])
    # print(response)
    # print(lastresponse)
    # print(lastresponse['et']['data'])
    if response['et']['data']['lastData'] != lastresponse['et']['data']:
        print("初始化错误", response)
        print("response['et']['data']['lastData']",response['et']['data']['lastData'],"lastresponse['et']['data']",lastresponse['et']['data'])
        return False
    return True
def getColsSymbol(points):#取出各列中奖位置
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
    return col1,col2,col3,col4,col5,symbol12_list
def checkAwardSymbol(response):#核对adPoints
    points = response['et']['data']['points']
    col1,col2,col3,col4,col5,symbol12_list = getColsSymbol(points)
    list_col1 = [x for x in col1.values()]
    list_col2 = [x for x in col2.values()]
    list_col3 = [x for x in col3.values()]
    list_col4 = [x for x in col4.values()]
    list_col5 = [x for x in col5.values()]
    list_allcols = [list_col1,list_col2,list_col3,list_col4,list_col5]
    for i in list_allcols:
        if len(i) > len(list(set(i))):
            print("出现重复元素")
            return False
    adPoints = {}
    for col1_key, col1_value in col1.items():
        if col1_value not in adPoints.keys():  # 字典里没有该符号
            for col2_key, col2_value in col2.items():
                if col1_value == col2_value or col2_value == 13:
                    for col3_key, col3_value in col3.items():
                        if col1_value == col3_value:
                            try:
                                adPoints[col1_value].append(col1_key)
                            except:
                                adPoints[col1_value] = [col1_key]
                            adPoints[col1_value].append(col2_key)
                            adPoints[col1_value].append(col3_key)
                        elif col1_value in (10, 11):
                            try:
                                adPoints[col1_value].append(col1_key)
                            except:
                                adPoints[col1_value] = [col1_key]
                            adPoints[col1_value].append(col2_key)
        else:
            adPoints[col1_value].append(col1_key)
    for key, value in adPoints.items():
        if 2 in value or 7 in value or 12 in value:
            for col4_key, col4_value in col4.items():
                if key == col4_value or col4_value == 13:
                    # print("加入",col4_value)
                    adPoints[key].append(col4_key)
                    for col5_key, col5_value in col5.items():
                        if key == col5_value:
                            # print("加入", col5_value)
                            adPoints[key].append(col5_key)
    for key, value in adPoints.items():
        adPoints[key] = list(set(value))
    if len(symbol12_list) >= 2:
        adPoints[12] = symbol12_list
    my_adPoints = {}
    for key, value in adPoints.items():
        my_adPoints[str(key)] = value
    for key in my_adPoints.keys():
        if sorted(my_adPoints[key]) != sorted(response['et']['data']['adPoints'].get(key,[])):
            print("中奖点有误", my_adPoints, response)
            return False
    for key in response['et']['data']['adPoints'].keys():
        if sorted(my_adPoints[key]) != sorted(response['et']['data']['adPoints'].get(key,[])):
            print("中奖点有误", my_adPoints, response)
            return False
    return True
def checkFsAwardSymbol(response,colNum):#核对adPoints
    points = response['et']['data']['points']
    col1,col2,col3,col4,col5,symbol12_list = getColsSymbol(points)
    list_col1 = [x for x in col1.values()]
    list_col2 = [x for x in col2.values()]
    list_col3 = [x for x in col3.values()]
    list_col4 = [x for x in col4.values()]
    list_col5 = [x for x in col5.values()]
    list_allcols = [list_col1,list_col2,list_col3,list_col4,list_col5]
    for i in list_allcols:
        if len(i) > len(list(set(i))):
            print("出现重复元素")
            return False
    adPoints = {}
    for col1_key, col1_value in col1.items():
        if col1_value not in adPoints.keys():  # 字典里没有该符号
            for col2_key, col2_value in col2.items():
                if col1_value == col2_value or col2_value == 13:
                    for col3_key, col3_value in col3.items():
                        if col1_value == col3_value:
                            try:
                                adPoints[col1_value].append(col1_key)
                            except:
                                adPoints[col1_value] = [col1_key]
                            adPoints[col1_value].append(col2_key)
                            adPoints[col1_value].append(col3_key)
                        elif col1_value in (10, 11):
                            try:
                                adPoints[col1_value].append(col1_key)
                            except:
                                adPoints[col1_value] = [col1_key]
                            adPoints[col1_value].append(col2_key)
        else:
            adPoints[col1_value].append(col1_key)
    for key, value in adPoints.items():
        if 2 in value or 7 in value or 12 in value:
            for col4_key, col4_value in col4.items():
                if key == col4_value or col4_value == 13:
                    # print("加入",col4_value)
                    adPoints[key].append(col4_key)
                    for col5_key, col5_value in col5.items():
                        if key == col5_value:
                            # print("加入", col5_value)
                            adPoints[key].append(col5_key)
    for key, value in adPoints.items():
        adPoints[key] = list(set(value))
    if len(symbol12_list) >= 2:
        adPoints[12] = symbol12_list
    my_adPoints = {}
    for key, value in adPoints.items():
        my_adPoints[str(key)] = value
    for key in my_adPoints.keys():
        if sorted(my_adPoints[key]) != sorted(response['et']['data']['adPoints'].get(key,[])) and len([x for x in my_adPoints[key] if x % 5 == colNum -1]) > 0:
            print("中奖点有误", my_adPoints, response)
            return False
    for key in response['et']['data']['adPoints'].keys():
        if sorted(my_adPoints[key]) != sorted(response['et']['data']['adPoints'].get(key,[])) and len([x for x in my_adPoints[key] if x % 5 == colNum -1]) > 0:
            print("中奖点有误", my_adPoints, response)
            return False
    return True
def normalPlay(tokenid,gametype,betScore):#正常玩模式
    url = "http://192.168.10.212:8002/getSlotData"
    millis = str(int(round(time.time() * 1000)))
    headers = {
        'token': tokenid,
        'Content-Type': 'application/json'
    }
    data = {
        "gt": str(gametype),
        "betScore": str(betScore),
        "actionType": "0",
        "timestamp": millis
    }
    data = json.dumps(data)
    try:
        response = requests.post(url, data=data,headers = headers)
        # print('正常', response.text)
        # print(data)
        response = response.json()
        if response.get("code") == 20000:
            # print(response)
            return response
        elif response.get("code") == 20001:
            return False
            # url = "http://192.168.10.212:8001/api/UserCore/AddPlayerGold"
            # millis = str(int(round(time.time() * 1000)))
            # data = {"tk": tokenid, "type": 1, "gold": 5000000, "timestamp": millis}
            # data = json.dumps(data)
            # res = requests.post(url=url, data=data)
            # print("充钱中",res.text)
        else:
            with open('error.txt','a')as f:
                f.write('\n'+ response)
            print("error",response)
    except:
        pass
    return None
def checkachievement(response,lastachievement):
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
            for symbol_index in award_symbol_index_list:
                if points_list[symbol_index] == 13:
                    award_symbol_index_list.remove(symbol_index)
            if len(award_symbol_index_list) >= value:
                if key in achievement:
                    achievement_value = achievement[key]
                    award_dic_value = str(value)
                    if award_dic_value not in achievement_value:
                        achievement_value.update({award_dic_value: 1})
                        achievement[key] = achievement_value
                        if int(key) <= 9:
                            if len(achievement[key]) == 3:
                                addAchievement_flag = True
                                if key not in response['et']['data']['addAchievement']:
                                    print("成就错误", key, response)
                                    return False
                        else:
                            if len(achievement[key]) == 4:
                                addAchievement_flag = True
                                if key not in response['et']['data']['addAchievement']:
                                    print("成就错误", key, response)
                                    return False
                else:
                    achievement[key] = {str(value): 1}
    if achievement != response['et']['data']['achievement'] and lastachievement != {} and response['et']['data']['achievement'] != {}:
        print("成就错误1", achievement, response, "\n")
        print(response['et']['data']['achievement'], "\n")
        return False
    if addAchievement_flag == False:
        if len(response['et']['data']['addAchievement']) > 0:
            print("成就错误2", response['et']['data']['addAchievement'])
            return False
    else:
        if len(response['et']['data']['addAchievement']) <= 0:
            print("成就错误2", response['et']['data']['addAchievement'])
            return False
    return response['et']['data']['achievement']
def oneColSpin(response,tk,times,gameType,mybetScore):
    global tokenid
    oneColSpin_url = "http://192.168.10.212:8002/getSlotData"
    lastnGold = response['et']['nGold']
    lastachievement = response['et']['data']['achievement']
    lastpoints = response['et']['data']['points']
    lastachievement = response['et']['data']['achievement']
    for i in range(times):
        if response['code'] == 20000:
            roteKey = response['et']['data']['roteKey']
            rotaryBls = response['et']['data']['rotaryBls']
            colNum = random.randint(1,5)
            millis = int(round(time.time() * 1000))
            one_spin_data ={
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
                response = requests.post(url = oneColSpin_url,data = one_spin_data,headers = headers)
                response = response.json()
                tim = time.asctime()
                print(f"{tim}--单轴",colNum,response)
                if response['code'] == 20000:
                    break
                elif response.get("code") == 20001:
                    return False
                    # url = "http://192.168.10.212:8001/api/UserCore/AddPlayerGold"
                    # millis = str(int(round(time.time() * 1000)))
                    # data = {"tk": tokenid, "type": 1, "gold": 5000000, "timestamp": millis}
                    # data = json.dumps(data)
                    # res = requests.post(url=url, data=data)
                    # print("充钱中", res.text)
            if not checkFsAwardSymbol(response,colNum):
                return False
            if not checkLotteryInitialize(tk=tk, gametype=gameType, lastresponse=response):  # 核对断线重连初始化
                return False
            lastnGold = checkFsnGold(response, rotaryBls[colNum - 1], lastnGold,mybetScore = mybetScore)
            lastpoints = checkFsPoints(response,colNum,lastpoints)
            lastachievement = checkachievement(response,lastachievement)
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
            return False
            # url = "http://192.168.10.212:8001/api/UserCore/AddPlayerGold"
            # millis = str(int(round(time.time() * 1000)))
            # data = {"tk": tokenid, "type": 1, "gold": 99999900, "timestamp": millis}
            # data = json.dumps(data)
            # res = requests.post(url=url, data=data)
            # print("充钱中",res.text)
            # return False
        else:
            print('error',response)
    return response
def call(tk,gametype):
    url = "http://192.168.10.212:8002/callInitialize"
    data = {
            "gt":gametype,
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
    print("初始化",response)
def register():
    url = "http://192.168.10.82:8031/registerUser"
    headers = {
        'Content-Type': 'application/json'
    }
    registerResponse = requests.get(url, headers=headers)
    username = registerResponse.json().get("username")
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
def main():#主函数 程序入口
    username, password = register()
    tk = getToken(username,password)
    tokenid = tk
    requests.get(f'http://192.168.10.212:8002/pay/{tk}/10000000')
    gameType = GT
    print(gameType)
    betScore = 25
    call(tokenid, gameType)
    while True:
        response = normalPlay(tokenid = tokenid,gametype= gameType,betScore = betScore)
        print(response)
        if response:
            if response['et']['type'] == 0 and response['et']['data']['isFree'] == False:
                if not checkAwardSymbol(response):
                    return
                if not checkLotteryInitialize(tk=tokenid, gametype=gameType,lastresponse = response):#核对断线重连初始化
                    return
                if 'lastnGold' not in dir():  # 如果是第一次运行脚本
                    lastnGold = response['et']['nGold']
                    lastachievement = response['et']['data']['achievement']
                else:
                    lastnGold = checknGold(response,betScore,lastnGold)
                    lastachievement = checkachievement(response,lastachievement)
                    if lastnGold == False:
                        return
                    if lastachievement == False:
                        return
                    times = random.randint(51, 999)
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
                    print("bonusGold有误",response['et']['data']['bonusGold'])
                    return
                myfreegold = response['et']['data']['freeGold']
                if not checkAwardSymbol(response):
                    return
                if not checkLotteryInitialize(tk=tokenid, gametype=gameType,lastresponse = response):#核对断线重连初始化
                    return
                if 'lastnGold' not in dir():  # 如果是第一次运行脚本

                    lastnGold = response['et']['nGold']
                    lastachievement = response['et']['data']['achievement']
                else:
                    lastnGold = checknGold(response,betScore,lastnGold)
                    lastachievement = checkachievement(response,lastachievement)
                    if lastnGold == False:
                        return
                    if lastachievement == False:
                        return
                if response['et']['type'] == 1:
                    fsTimes = response['et']['data']['residue']
                elif response['et']['data']['isFree'] == True:
                    fsTimes = 15
                playedTimes = 1
                while playedTimes <= fsTimes:
                    response = normalPlay(tokenid=tokenid, gametype=gameType, betScore=betScore)
                    print(response)
                    if response:
                        myfreegold += response['et']['data']['gold']
                        if myfreegold != response['et']['data']['freeGold']:
                            print("freegold错误",myfreegold,response['et']['data']['freeGold'])
                            return
                        if not checkAwardSymbol(response):
                            return
                        if not checkLotteryInitialize(tk=tokenid, gametype=gameType, lastresponse=response):  # 核对断线重连初始化
                            return
                        if response['et']['type'] != 1:
                            print("红利错误",playedTimes,fsTimes)
                            return
                        fsTimes += response['et']['data']['plan']
                        print(response['et']['data']['plan'])
                        if 'lastnGold' not in dir():  # 如果是第一次运行脚本
                            lastnGold = response['et']['nGold']
                            lastachievement = response['et']['data']['achievement']
                        else:
                            lastnGold = checknGold(response, betScore, lastnGold)
                            lastachievement = checkachievement(response,lastachievement)
                            if lastnGold == False:
                                return
                            if lastachievement == False:
                                return
                        if response['et']['data']['residue'] + playedTimes != fsTimes:
                            print("红利错误",playedTimes,fsTimes)
                            return
                        playedTimes += 1




if __name__ == '__main__':
    main()