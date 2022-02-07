# encoding:utf-8
import copy
import json
import time

import requests


def checkLinePoints(adpoints, linepoints):  # 核对LinePoints
    myadpoints = copy.deepcopy(adpoints)  # 拷贝一个 myadpoints 避免后续直接修改adpoints对象
    for key, value in myadpoints.items():
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
                mylinepoints = [[a, b, c, d, e] for a in col1 for b in col2 for c in col3 for d in col4 for e in col5]
            elif len(col4) > 0:
                mylinepoints = [[a, b, c, d] for a in col1 for b in col2 for c in col3 for d in col4]
            elif len(col3) > 0:
                mylinepoints = [[a, b, c] for a in col1 for b in col2 for c in col3]
            elif len(col2) > 0:
                mylinepoints = [[a, b] for a in col1 for b in col2]
            else:
                mylinepoints = []
            if sorted(mylinepoints) != sorted(linepoints[key]):
                print("linepoints有误", sorted(mylinepoints), sorted(linepoints[key]))
                return False
        else:
            if key in linepoints:
                print("linepoints有误包含符号12")
                return False
    return True


def checkNgold(response, betScore, lastNgold):  # 核对Ngold
    award_dic = {
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
    awardlins = response['et']['Data']['AwardLins']
    Points = response['et']['Data']['Points']
    AdPoints = response['et']['Data']['AdPoints']
    LinePoints = response['et']['Data']['LinePoints']
    if response['et']['Type'] == 0:  # 判断是否是红利场
        paygold = -betScore  # 如果不是红利场，则底注为-底注
        hl_num = 1  # 红利倍数为1
    else:
        paygold = 0  # 如果是红利场，则底注为0
        hl_num = 3  # 红利倍数为3
    if not checkLinePoints(AdPoints, LinePoints):
        return False
    if len(awardlins) > 0:
        for key, value in awardlins.items():  # 遍历中奖符号
            if key == '12':  # 出现散布图
                paygold = paygold + (award_dic[(int(key), value)] * betScore) * hl_num  # 直接乘投注的倍数
            else:
                for i in LinePoints[key]:
                    paygold = paygold + award_dic[(int(key), len(i))] * (betScore / 25) * hl_num
    current_gold = int(lastNgold + paygold)  # 计算出current——gold
    if current_gold != response['et']['NGold']:
        print('筹码错误', paygold, current_gold, response['et']['NGold'])
        return False
    return current_gold


def checkLotteryInitialize(tk, gametype, lastresponse):  # 核对断线重连初始化
    while True:
        url = "http://192.168.10.25:8001//api/UserCore/CallLotteryInitialize"
        millis = int(round(time.time() * 1000))
        data = {"tk": tk,
                "gt": gametype,
                "timestamp": millis
                }
        data = json.dumps(data)
        response = requests.post(url=url, data=data)
        response = response.json()
        if response['code'] == 20000:
            break
    # print(response['et']['Data']['LastData'])
    # print(lastresponse['et']['Data'])
    if response['et']['Data']['LastData'] != lastresponse['et']['Data']:
        print("初始化错误", response)
        print("response['et']['Data']['LastData']", response['et']['Data']['LastData'], "lastresponse['et']['Data']",
              lastresponse['et']['Data'])
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
        if 2 in value or 7 in value or 12 in value:
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


def normalPlay(tokenid, gametype, betScore):  # 正常玩模式
    url = "http://192.168.10.25:8001//api/UserCore/CallLotteryModel"
    millis = int(round(time.time() * 1000))
    data = {
        "tk": tokenid,
        "gt": gametype,
        "timestamp": millis,
        "betScore": betScore
        }
    data = json.dumps(data)
    try:
        response = requests.post(url, data=data)
        response = response.json()
        if response.get("code") == 20000:
            # print(response)
            return response
        elif response.get("code") == 20017:
            url = "http://192.168.10.25:8001/api/UserCore/AddPlayerGold"
            millis = str(int(round(time.time() * 1000)))
            data = {"tk": tokenid, "type": 1, "gold": 99999900, "timestamp": millis}
            data = json.dumps(data)
            res = requests.post(url=url, data=data)
            print("充钱中", res.text)
        else:
            print("error", response)
    except:
        pass
    return None


def checkAchievement(response, lastAchievement):
    achievement = lastAchievement
    AddAchievement_flag = False
    awardlins = response['et']['Data']['AwardLins']
    AdPoints = response['et']['Data']['AdPoints']
    LinePoints = response['et']['Data']['LinePoints']
    points_list = response['et']['Data']['Points']
    if response['et']['Type'] == 0 and len(awardlins) != 0:
        for key, value in awardlins.items():
            award_symbol_index_list = []
            for i in AdPoints[key]:
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
                                AddAchievement_flag = True
                                if key not in response['et']['Data']['AddAchievement']:
                                    print("成就错误", key, response)
                                    return False
                        else:
                            if len(achievement[key]) == 4:
                                AddAchievement_flag = True
                                if key not in response['et']['Data']['AddAchievement']:
                                    print("成就错误", key, response)
                                    return False
                else:
                    achievement[key] = {str(value): 1}
    if achievement != response['et']['Data']['Achievement']:
        print("成就错误1", achievement, response, "\n")
        print(response['et']['Data']['Achievement'], "\n")
        return False
    if AddAchievement_flag == False:
        if len(response['et']['Data']['AddAchievement']) > 0:
            print("成就错误2", response['et']['Data']['AddAchievement'])
            return False
    else:
        if len(response['et']['Data']['AddAchievement']) <= 0:
            print("成就错误2", response['et']['Data']['AddAchievement'])
            return False
    return response['et']['Data']['Achievement']


def main():  # 主函数 程序入口
    while True:
        # tokenid = "A9FB9B30752B679D174F70E08941782F89D4"
        tokenid = "F080627258E08DDFD3DA6299C8B70C3F6BFE"
        gameType = 134
        betScore = 25
        response = normalPlay(tokenid=tokenid, gametype=gameType, betScore=betScore)
        print(response)
        if response:
            if not checkAwardSymbol(response):
                break
            if not checkLotteryInitialize(tk=tokenid, gametype=gameType, lastresponse=response):  # 核对断线重连初始化
                break

            if 'lastNgold' not in dir():  # 如果是第一次运行脚本
                lastNgold = response['et']['NGold']
                lastAchievement = response['et']['Data']['Achievement']
            else:
                lastNgold = checkNgold(response, betScore, lastNgold)
                lastAchievement = checkAchievement(response, lastAchievement)
                if lastNgold == False:
                    break
                if lastAchievement == False:
                    break
            checkAchievement(response, lastAchievement)
        time.sleep(5)


if __name__ == '__main__':
    main()

