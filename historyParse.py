#encoding:utf-8
import requests,threading
import re,pymongo,json,copy,itertools
import os
import time
import datetime,json
import decimal
from decimal import Decimal
from dateutil.parser import *
import pymssql
from logAnalysisUtil import *
GAMETYPELIST =  {"34": "百人牛牛",
 "47": "红黑大战",
 "58": "百人骰宝",
 "125": "不朽情缘",
 "126": "花花公子",
 "130": "东方珍兽",
 "131": "比基尼派对",
 "132": "舞龙",
 "133": "宝石转轴",
 "134": "燃烧的欲望",
 "135": "招财鞭炮",
 "136": "幸运富豪",
 "141": "篮球巨星",
 "142": "幸运龙宝贝",
 "144": "迷失拉斯维加斯",
 "145": "爆破银行",
 "146": "野生大熊猫",
 "200": "鱼虾蟹",
 "201": "猜丁壳",
"39":"十三水",
"32":"三公",
"38":"二十一点",
"41":"德州扑克",
"143":"奇妙马戏团",
"202":"俄罗斯轮盘",
"31":"推筒子",
"33":'牌九',
"30":'扎金花',
"36":'通比牛牛',
"37":'极速扎金花',
"43":'新版斗牛',
"54":'血战骰宝',
"45":'欢乐炸金花',
"56":'抢庄牛牛',
"46":"港式梭哈",
"48":"炸金牛",
"59":"未知",
}
def player():
    print('\n')
    print('玩家报表')
    ms.GetConnect()
    sql = f"select count(*) from dbo.Game_UserInfoBase where regTime > '{startTime}'AND regTime < '{endTime}' and id not in {tuple_black_List}"
    print(sql)
    data = ms.ExecQuery(sql)
    regPersonCount = data[0][0]
    sql = f"select count(*) from dbo.Game_UserLoginInfo where updateTime > '{startTime}'AND updateTime < '{endTime}' and id not in {tuple_black_List} and style <> 00000"
    data = ms.ExecQuery(sql)
    plarLoginCount = data[0][0]
    sql = f"select COUNT(distinct (userName + '-' + style)) from (select userName,style from dbo.Game_GameGoldActionInfo where CreatDate > '{startTime}'AND CreatDate < '{endTime}' UNION all select userName,style from dbo.Game_GoldActionInfo where CreatDate > '{startTime}'AND CreatDate < '{endTime}') as s1 where (userName + '-' + style) not in {black_users_list}"
    data = ms.ExecQuery(sql)
    playerCount = data[0][0]
    sql = f"select count(*),COUNT(distinct (userName + '-' + style)) from (select userName,style from dbo.Game_GameGoldActionInfo where CreatDate > '{startTime}'AND CreatDate < '{endTime}' and actionType in (2,12) UNION all select userName,style from dbo.Game_GoldActionInfo where CreatDate > '{startTime}'AND CreatDate < '{endTime}'and actionType in (2,12)) as s1 where (userName + '-' + style) not in {black_users_list}"
    data = ms.ExecQuery(sql)
    betCount,tradePlayerCount = data[0]
    print('注册人数','登录人数','帐变玩家','游戏人数','投注次数')
    print(regPersonCount, plarLoginCount, playerCount, tradePlayerCount, betCount)
def comparePlayer(gameReportData):
    if gameReportData['regUserNum'] != regPersonCount or gameReportData['plarLoginCount'] != plarLoginCount or gameReportData['gamePeople'] != playerCount or gameReportData['gameBout'] != tradePlayerCount or gameReportData['goldChangeNum'] != betCount:
        print('玩家报表有误')

def playerData():
    print('\n')
    print('玩家数据')
    users = {}
    for x in mydoc:
        # if x.get("gameType") != 32:
        #     continue
        for key, value in x.items():
            if key == 'userName':
                value = value + str(x['currencyType']) + str(x['style'])
                if value not in users:
                    gameCount = 1
                    validBetSum = x['validAmount']
                    users[value] = {'style': x['style'],'gameCount':gameCount,'betAmount': x['betAmount'],'tax':x['tax'],'gold':x['gold'],'aveBet':x['betAmount']/gameCount,'currencyType':x['currencyType'],'validBetSum':validBetSum}
                else:
                    style = users[value]['style']
                    gameCount = users[value]['gameCount'] + 1
                    betAmount = users[value]['betAmount'] + x['betAmount']
                    tax = users[value]['tax'] + x['tax']
                    gold = users[value]['gold'] + x['gold']
                    validBetSum = users[value]['validBetSum'] + x['validAmount']
                    users[value] = {'style': style,'gameCount':gameCount,'betAmount': betAmount,'tax':tax,'gold':gold,'aveBet':betAmount/gameCount,'currencyType':x['currencyType'],'validBetSum':validBetSum}
    for key,value in users.items():
        print(key[0:-2],value)
    return users
def gameData():
    print('\n')
    print('游戏简报')
    games = {}
    totalBet = {0: 0, 1: 0, 2: 0, 3: 0}
    totalAward = {0: 0, 1: 0, 2: 0, 3: 0}
    totalTax = {0: 0, 1: 0, 2: 0, 3: 0}
    totalGameCount = 0
    totalBetAmount = 0
    totalProfit = 0
    for x in mydoc:
        for key,value in x.items():
            if key == 'gameType':
                totalBet[x['currencyType']] += x['validAmount']
                totalAward[x['currencyType']] += x['gold']
                totalTax[x['currencyType']] += x['tax']
                totalGameCount += 1
                if value not in games:
                    gameCount = 1
                    gold = x['gold']
                    profit = {x['currencyType']:gold}
                    betAmount = {x['currencyType']:x['validAmount']}
                    tax = {x['currencyType']:x['tax']}
                    totalBetAmount = x['validAmount'] / exchangeRate[int(x['currencyType'])]['rate']
                    totalProfit = x['gold'] / exchangeRate[int(x['currencyType'])]['rate']
                    games[value] = {'betAmount': betAmount,'profit':profit,'tax':tax,'gameCount':gameCount}
                else:
                    gameCount = games[value]['gameCount'] + 1
                    betAmount = games[value]['betAmount']
                    if x['currencyType'] in betAmount:
                        betAmount[x['currencyType']] += x['validAmount']
                    else:
                        betAmount[x['currencyType']] = x['validAmount']
                    tax = games[value]['tax']
                    if x['currencyType'] in tax:
                        tax[x['currencyType']] += x['tax']
                    else:
                        tax[x['currencyType']] = x['tax']
                    profit = games[value]['profit']
                    if x['currencyType'] in profit:
                        profit[x['currencyType']] += x['gold']
                    else:
                        profit[x['currencyType']] = x['gold']
                    games[value] = {'betAmount': betAmount,'profit':profit,'tax':tax,'gameCount':gameCount}
    for key,value in games.items():
        profit = value['profit']
        betAmount = value['betAmount']
        totalProfit = getChangedGold(profit)
        totalBetAmount = getChangedGold(betAmount)
        if totalBetAmount != 0:
            winRate = round(totalProfit/totalBetAmount * 100,2)
        else:
            winRate = 0
        print(GAMETYPELIST[str(key)],value,'胜率:',str(winRate) + "%")
    print(f'总计：投注额:{totalBet},玩家输赢:{totalAward},抽水:{totalTax},游戏次数:{totalGameCount},游戏胜率:{winRate}')
def roomData():
    print('\n')
    print('房间数据')
    rooms = {}
    for x in mydoc:
        for key, value in x.items():
            if key == 'roomId':
                roomName = str(x['gameType'])+'_'+str(value)
                if roomName not in rooms:
                    gold = x['gold']
                    profit = {x['currencyType']: gold}
                    tax = {x['currencyType']: x['tax']}
                    betAmount = {x['currencyType']: x['validAmount']}
                    rooms[roomName] = {'profit': profit, 'tax': tax,'roundIdList':[x['roundId']],'playerList':[x['userName']+x['style']],'validAmount':betAmount}
                else:
                    profit = rooms[roomName]['profit']
                    if x['currencyType'] in profit:
                        profit[x['currencyType']] += x['gold']
                    else:
                        profit[x['currencyType']] = x['gold']
                    tax = rooms[roomName]['tax']
                    if x['currencyType'] in tax:
                        tax[x['currencyType']] += x['tax']
                    else:
                        tax[x['currencyType']] = x['tax']
                    betAmount = rooms[roomName]['validAmount']
                    if x['currencyType'] in betAmount:
                        betAmount[x['currencyType']] += x['validAmount']
                    else:
                        betAmount[x['currencyType']] = x['validAmount']
                    roundIdList = rooms[roomName]['roundIdList']
                    roundIdList.append(x['roundId'])
                    playerList = rooms[roomName]['playerList']
                    if x.get('userName'):
                        playerList.append(x['userName']+x['style'])
                    else:
                        print(x)
                    rooms[roomName] = {'profit': profit, 'tax': tax,'roundIdList':roundIdList,'playerList':playerList,'validAmount':betAmount}
    roomDataList = []
    gameCountSum = 0
    for key,value in sorted(rooms.items()):
        gameName = GAMETYPELIST[key.split('_')[0]]
        roomName = key.split('_')[1]
        gameCount = len(value['roundIdList'])
        playerCount = len(set(value['playerList']))
        betAmount = value['validAmount']
        totalProfit = getChangedGold(value['profit'])
        totalBetAmount = getChangedGold(betAmount)
        if totalBetAmount != 0:
            winRate = round(totalProfit / totalBetAmount * 100, 2)
        else:
            winRate = 0
        print(gameName,roomName,value['profit'],value['tax'],gameCount,playerCount,'validAmount',betAmount, '胜率:', str(winRate) + "%")
def settlementsData():
    users = playerData()
    settlements = {}
    sql = f"select top 1 rates from dbo.Game_ExchangeRate ORDER by createTime DESC"
    exchangeRate = json.loads(ms.ExecQuery(sql)[0][0])
    for value in users.values():
        style = value['style']
        currencyType = value['currencyType']
        if style not in settlements.keys():
            playerCount = 1
            validBetSum = {currencyType:value['validBetSum']}
            gameCount = value['gameCount']
            gold = {currencyType:value['gold']}
            tax = {currencyType:value['tax']}
            settlements[style] = {'style':style,'gameCount':gameCount,'playerCount':playerCount,'validBetSum':validBetSum,'tax':tax,'gold':gold}
        else:
            settlements[style]['gameCount'] += value['gameCount']
            settlements[style]['playerCount'] += 1
            if currencyType in settlements[style]['validBetSum'].keys():
                settlements[style]['validBetSum'][currencyType] += value['validBetSum']
            else:
                settlements[style]['validBetSum'][currencyType] = value['validBetSum']
            if currencyType in settlements[style]['gold'].keys():
                settlements[style]['gold'][currencyType] += value['gold']
            else:
                settlements[style]['gold'][currencyType] = value['gold']
            if currencyType in settlements[style]['tax'].keys():
                settlements[style]['tax'][currencyType] += value['tax']
            else:
                settlements[style]['tax'][currencyType] = value['tax']
    print('\n')
    print('结算数据')
    for key, value in settlements.items():
        validBet = 0
        award = 0
        for currencyType,num in value['validBetSum'].items():
            if currencyType > 0:
                validBet += num/(exchangeRate[currencyType-1]['rate'])
            else:
                validBet += num
        for currencyType, num in value['gold'].items():
            if currencyType > 0:
                award += num / (exchangeRate[currencyType - 1]['rate'])
            else:
                award += num
        killRate = award/validBet
        value['killRate'] = killRate
        print(value)
def gameReport(startTime, endTime):
    print('\n')
    print('游戏报表')
    games = {}
    totalBet = {0:0,1:0,2:0,3:0}
    totalAward = {0:0,1:0,2:0,3:0}
    totalTax = {0: 0, 1: 0, 2: 0, 3: 0}
    gameRecord = {}
    totalGameCount = 0
    for x in mydoc:
        for key, value in x.items():
            if key == 'gameType':
                gameRecordList = gameRecord.get(value,[])
                if x.get('userName'):
                    gameRecordList.append((str(x['roundId']),x['userName'],x['gold']))
                else:
                    print(x)
                gameRecord[value] = gameRecordList
                totalBet[x['currencyType']] += x['betAmount']
                totalAward[x['currencyType']] += x['gold']
                totalTax[x['currencyType']] += x['tax']
                totalGameCount += 1
                if value not in games:
                    gameCount = 1
                    gold = x['gold']
                    profit = {x['currencyType']: gold}
                    betAmount = {x['currencyType']: x['betAmount']}
                    tax = {x['currencyType']: x['tax']}
                    sql = f"select t.extendedField1,sum(t.goldNum),count(*) from (select goldNum,extendedField1 from dbo.Game_GameGoldActionInfo where creatDate BETWEEN '{startTime}' AND '{endTime}' and gameType = {value} and actionType in (2,12) UNION all select goldNum,currencyType from dbo.Game_GoldActionInfo where creatDate BETWEEN '{startTime}' AND '{endTime}' and gameType = {value} and actionType in (2,12)) as t GROUP BY t.extendedField1"
                    goldNum = ms.ExecQuery(sql)
                    gameType = value
                    conditions = {"gameType":{"$eq": gameType}}
                    playerCount = getGameUserCountUsersCount(startTime,endTime,black_List,conditions)
                    games[value] = {'betAmount': betAmount, 'profit': profit, 'tax': tax, 'gameCount': gameCount,'playerCount':playerCount,'goldLogNum':goldNum}

                else:
                    playerCount = games[value]['playerCount']
                    gameCount = games[value]['gameCount'] + 1
                    betAmount = games[value]['betAmount']
                    if x['currencyType'] in betAmount:
                        betAmount[x['currencyType']] += x['betAmount']
                    else:
                        betAmount[x['currencyType']] = x['betAmount']
                    tax = games[value]['tax']
                    if x['currencyType'] in tax:
                        tax[x['currencyType']] += x['tax']
                    else:
                        tax[x['currencyType']] = x['tax']
                    profit = games[value]['profit']
                    if x['currencyType'] in profit:
                        profit[x['currencyType']] += x['gold']
                    else:
                        profit[x['currencyType']] = x['gold']
                    goldLogNum = games[value]['goldLogNum']
                    games[value] = {'betAmount': betAmount, 'profit': profit, 'tax': tax, 'playerCount':playerCount,'gameCount': gameCount,'goldLogNum':goldLogNum}
    # print(games)
    for key,value in games.items():
        goldLogNum = value['goldLogNum']
        profit = value['profit']
        print(GAMETYPELIST[str(key)], value)
        for currency_goldNum in goldLogNum:
            currency = currency_goldNum[0]
            if not currency:
                currency = 0
            goldNum = currency_goldNum[1]
            if goldNum != profit[currency]:
                sql = f"select t.orderId,t.userName,t.goldNum from (select orderId,userName,goldNum from dbo.Game_GameGoldActionInfo where creatDate BETWEEN '{startTime}' AND '{endTime}' and gameType = {key} and actionType in (2,12) UNION all select orderId,userName,goldNum from dbo.Game_GoldActionInfo where creatDate BETWEEN '{startTime}' AND '{endTime}' and gameType = {key} and actionType in (2,12)) as t"
                goldLog = ms.ExecQuery(sql)
                errorRound1 = [x for x in goldLog if x not in gameRecord[key]]
                errorRound2 = [x for x in gameRecord[key] if x not in goldLog]
                if len(errorRound1) > 0:
                    print('金流有',len(errorRound1))
                    for i in errorRound1:
                        print(i)
                if len(errorRound2) > 0:
                    print('日志有')
                    for i in errorRound2:
                        print(i)
    totalPlayerCount = getGameUserCountUsersCount(startTime, endTime, black_List)
    print(f'总计：投注额:{totalBet},玩家输赢:{totalAward},抽水:{totalTax},游戏人次:{totalPlayerCount},游戏次数:{totalGameCount}')
    return games
def getGlobalData():
    global black_users_list, exchangeRate,tuple_black_List,black_List
    sql = f"SELECT login.id FROM dbo.Game_UserLoginInfo as login RIGHT JOIN (select userInfo.id from dbo.Game_UserInfoBase as userInfo RIGHT JOIN  dbo.ReportBlacks as black on userInfo.userName = black.userName and userInfo.style =  black.style) as blackId on login.uid = blackId.id WHERE login.style <> 00000"
    black_List = [x[0] for x in ms.ExecQuery(sql)]
    tuple_black_List = str(black_List).replace('[', '(').replace(']', ')')
    sql = "SELECT (userName + '-' + style) from dbo.ReportBlacks"
    black_users_list = str([x[0] for x in ms.ExecQuery(sql)]).replace('[', '(').replace(']', ')')
    sql = "SELECT top 1 rates from dbo.Game_ExchangeRate order by createTime DESC"
    exchangeRate = json.loads(ms.ExecQuery(sql)[0][0])
    exchangeRate.insert(0, {"currencyType": 0, "rate": 1.0, "name": "CNY"})
def getBackStageGameReport(session,token,startTime, endTime,urlType):

    if urlType == 1:
        url = 'http://192.168.10.211:8082/report/findGameReport'
    elif urlType == 2:
        url = 'http://192.168.10.211:8082/report/findUserReport'
    startDay = startTime.split(' ')[0]
    endDay = startTime.split(' ')[0]
    headers = {'Content-Type': 'application/json;charset=UTF-8',
               'token':token}
    data = {"cid": "",
            "dateMax":endDay,
            "dateMin": startDay,
            "gameType": "",
            "gid": "",
            "limit": 10,
            "page": 1,
            "style": ""}
    data = json.dumps(data)
    response = session.post(url = url,data = data,headers = headers)
    response = response.json()
    if response.get('code','') == '0':
        return response.get('data','')
def loginBackStage(session):
    loginUrl = 'http://192.168.10.211:8082/login'
    data = {'username':'shu','password':'123456'}
    response = session.post(url = loginUrl,data = data)
    response = response.json()
    if response.get('status',0) == 200:
        return response.get('token','')
def init_requests():
    session = requests.session()
    return session
def compareGamesData(gameReportData,games):
    print('1111',gameReportData)
    print('2222', games)
    for game in gameReportData:
        gameType = game['gameName']
        betAmount = game['betAmount']
        goldNum = game['goldNum']
        tax = game['tax']
        userNum = game['userNum']
        gameNum = game['gameNum']
        my_gameType = int(gameType)
        my_betAmount = games[my_gameType]['betAmount']
        my_goldNum = games[my_gameType]['profit']
        my_tax = games[my_gameType]['tax']
        my_playerCount = games[my_gameType]['playerCount']
        my_gameCount = games[my_gameType]['gameCount']
        if not(compareDict(betAmount,my_betAmount) and compareDict(goldNum,my_goldNum) and compareDict(tax,my_tax) and userNum == my_playerCount and gameNum == my_gameCount):
            print(GAMETYPELIST[str(gameType)])
            exit(-1)
def compareDict(dict1,dict2):
    for i in range(0,4):
        if round(dict1.get(str(i),0) * 100) != dict2.get(int(i),0):
            print(round(dict1.get(str(i),0) * 100),dict2.get(int(i),0))
            return False
    return True
if __name__ == '__main__':
    ms = init_sqlSever()
    session = init_requests()
    checkBackstage = False
    startTime = "2022-04-20 18:00:00"
    endTime = "2022-04-21 09:00:00"
    getGlobalData()
    mydoc = timeQueryMangodb(startTime, endTime, black_List)
    token = loginBackStage(session)
    gameReportData = getBackStageGameReport(session,token,startTime, endTime,1)
    games = gameReport(startTime, endTime)
    player()
    gameData()
    roomData()
    settlementsData()
    if checkBackstage:
        compareGamesData(gameReportData,games)
        gameReportData = getBackStageGameReport(session, token, startTime, endTime, 2)[0]
        print(gameReportData)


