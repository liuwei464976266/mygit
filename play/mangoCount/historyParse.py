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
STARTTIME = "2022-02-24 18:00:00"
ENDTIME = "2022-02-25 09:00:00"

GAMETYPELIST ={
     "56":"赌场扑克",
     "45": "欢乐扎金花",
     "54": "血战骰宝",
     "30": "扎金花",
     "43": "新版斗牛",
     "34": "百人牛牛",
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
    "33":"牌九",

}
class MSSQL:

    def __init__(self, host, user, pwd, db, port):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.port = port


    def GetConnect(self):
        if not self.db:
            raise (NameError, '没有设置数据库信息')
        self.conn = pymssql.connect(host=self.host, user=self.user, password=self.pwd, database=self.db, port=self.port, charset='utf8')
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, '连接数据库失败')
        else:
            return cur

    def ExecQuery(self, sql):
        cur = self.GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()
        self.conn.close()
        return resList

    def ExecNonQuery(self, sql):
        cur = self.GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()

    def GetData(self, sql):
        count = 0
        for i in range(len(sql)):
            for j in range(len(sql[i])):
                count += 1
                if type(sql[i][j]) is str:
                    print(sql[i][j].encode('latin1').decode('gbk'), end=',')
                else:
                    print(sql[i][j], end=',')
                if count % len(sql[i]) == 0:
                    print('\n')
def player():
    print('\n')
    print('玩家报表')
    ms = MSSQL(host='192.168.10.199', user='test', pwd='123456', db="OverseasGameV1", port=1433)
    ms.GetConnect()
    sql = f"select count(*) from dbo.Game_UserInfoBase where regTime > '{STARTTIME}'AND regTime < '{ENDTIME}' and id not in {tuple_black_List}"
    data = ms.ExecQuery(sql)
    regPersonCount = data[0][0]
    sql = f"select count(*) from dbo.Game_UserLoginInfo where updateTime > '{STARTTIME}'AND updateTime < '{ENDTIME}' and id not in {tuple_black_List} and style <> 00000"
    data = ms.ExecQuery(sql)
    plarLoginCount = data[0][0]
    sql = f"select COUNT(distinct (userName + '-' + style)) from (select userName,style from dbo.Game_GameGoldActionInfo where CreatDate > '{STARTTIME}'AND CreatDate < '{ENDTIME}' UNION all select userName,style from dbo.Game_GoldActionInfo where CreatDate > '{STARTTIME}'AND CreatDate < '{ENDTIME}') as s1 where (userName + '-' + style) not in {black_users_list}"
    data = ms.ExecQuery(sql)
    playerCount = data[0][0]
    sql = f"select count(*),COUNT(distinct (userName + '-' + style)) from (select userName,style from dbo.Game_GameGoldActionInfo where CreatDate > '{STARTTIME}'AND CreatDate < '{ENDTIME}' and actionType in (2,12) UNION all select userName,style from dbo.Game_GoldActionInfo where CreatDate > '{STARTTIME}'AND CreatDate < '{ENDTIME}'and actionType in (2,12)) as s1 where (userName + '-' + style) not in {black_users_list}"
    data = ms.ExecQuery(sql)
    betCount,tradePlayerCount = data[0]
    print('注册人数','登录人数','帐变玩家','游戏人数','投注次数')
    print(regPersonCount,plarLoginCount,playerCount,tradePlayerCount,betCount)
def playerData():
    print('\n')
    print('玩家数据')
    mydoc = timeQueryMangodb(STARTTIME,ENDTIME,black_List)
    users = {}
    for x in mydoc:
        for key,value in x.items():
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
    mydoc = timeQueryMangodb(STARTTIME,ENDTIME,black_List)
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
            winRate = round(totalProfit/totalBetAmount * 100, 2)
        else:
            winRate = 0
        print(GAMETYPELIST[str(key)],value,'胜率:', str(winRate) + "%")
    print(f'总计：投注额:{totalBet},玩家输赢:{totalAward},抽水:{totalTax},游戏次数:{totalGameCount},游戏胜率:{winRate}')
def roomData():
    print('\n')
    print('房间数据')
    mydoc = timeQueryMangodb(STARTTIME,ENDTIME,black_List)
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
                    playerList.append(x['userName']+x['style'])
                    rooms[roomName] = {'profit': profit, 'tax': tax,'roundIdList':roundIdList,'playerList':playerList,'validAmount':betAmount}
    roomDataList = []
    gameCountSum = 0
    for key,value in rooms.items():
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
    ms = MSSQL(host='192.168.10.199', user='test', pwd='123456', db="OverseasGameV1", port=1433)
    ms.GetConnect()
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
    for key,value in settlements.items():
        validBet = 0
        award = 0
        for currencyType,num in value['validBetSum'].items():
            if currencyType > 0:
                validBet += num/(exchangeRate[currencyType-1]['rate'])
            else:
                validBet += num
        for currencyType,num in value['gold'].items():
            if currencyType > 0:
                award += num / (exchangeRate[currencyType - 1]['rate'])
            else:
                award += num
        killRate = award/validBet
        value['killRate'] = killRate
        print(value)
def gameReport():
    print('\n')
    print('游戏报表')
    mydoc = timeQueryMangodb(STARTTIME,ENDTIME,black_List)
    games = {}
    totalBet = {0:0,1:0,2:0,3:0}
    totalAward = {0:0,1:0,2:0,3:0}
    totalTax = {0: 0, 1: 0, 2: 0, 3: 0}
    totalPlayerCount = 0
    totalGameCount = 0
    for x in mydoc:
        for key, value in x.items():
            if key == 'gameType':
                totalBet[x['currencyType']] += x['betAmount']
                totalAward[x['currencyType']] += x['gold']
                totalTax[x['currencyType']] += x['tax']
                totalGameCount += 1
                if value not in games:
                    gameCount = 1
                    gold = x['gold']
                    profit = {x['currencyType']: gold}
                    betAmount = {x['currencyType']: x['betAmount']}
                    tax = {x['currencyType']: x['profit']}
                    games[value] = {'betAmount': betAmount, 'profit': profit, 'tax': tax, 'gameCount': gameCount,'playerList':[x['uid']] }
                else:
                    gameCount = games[value]['gameCount'] + 1
                    betAmount = games[value]['betAmount']
                    if x['currencyType'] in betAmount:
                        betAmount[x['currencyType']] += x['betAmount']
                    else:
                        betAmount[x['currencyType']] = x['betAmount']
                    tax = games[value]['tax']
                    if x['currencyType'] in tax:
                        tax[x['currencyType']] += x['profit']
                    else:
                        tax[x['currencyType']] = x['profit']
                    profit = games[value]['profit']
                    if x['currencyType'] in profit:
                        profit[x['currencyType']] += x['gold']
                    else:
                        profit[x['currencyType']] = x['gold']
                    playerList = games[value]['playerList']
                    playerList.append(x['uid'])
                    games[value] = {'betAmount': betAmount, 'profit': profit, 'tax': tax, 'playerList':playerList,'gameCount': gameCount}
    for key,value in games.items():
        playerCount = len(set(value['playerList']))
        totalPlayerCount += playerCount
        value['playerList'] = playerCount
        print(GAMETYPELIST[str(key)], value)
    print(f'总计：投注额:{totalBet},玩家输赢:{totalAward},抽水:{totalTax},游戏人次:{totalPlayerCount},游戏次数:{totalGameCount}')

def getGlobalData():
    global black_users_list, exchangeRate,tuple_black_List,black_List
    ms = MSSQL(host='192.168.10.199', user='test', pwd='123456', db="OverseasGameV1", port=1433)
    ms.GetConnect()
    sql = f"SELECT login.id FROM dbo.Game_UserLoginInfo as login RIGHT JOIN (select userInfo.id from dbo.Game_UserInfoBase as userInfo RIGHT JOIN  dbo.ReportBlacks as black on userInfo.userName = black.userName and userInfo.style =  black.style) as blackId on login.uid = blackId.id WHERE login.style <> 00000"
    black_List = [x[0] for x in ms.ExecQuery(sql)]
    tuple_black_List = str(black_List).replace('[', '(').replace(']', ')')
    sql = "SELECT (userName + '-' + style) from dbo.ReportBlacks"
    black_users_list = str([x[0] for x in ms.ExecQuery(sql)]).replace('[', '(').replace(']', ')')
    sql = "SELECT top 1 rates from dbo.Game_ExchangeRate order by createTime DESC"
    exchangeRate = json.loads(ms.ExecQuery(sql)[0][0])
    exchangeRate.insert(0, {"currencyType": 0, "rate": 1.0, "name": "CNY"})


if __name__ == '__main__':
    getGlobalData()
    gameReport()
    player()
    gameData()
    roomData()
    settlementsData()
