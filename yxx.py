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
STARTTIME = "2021-08-16 10:00:00"#这个时间早8个小时
ENDTIME = "2021-08-17 23:59:59"
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
"38":"二十一点"
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
def settlementsCheck(bet,recordPoints):
    symbolPoints = ['35', '36', '37', '38', '39', '40']
    recordList = [x for x in recordPoints.values()]
    myWinPoint = []
    awardDic = {
        "0": 1,
        "1": 1,
        "2": 7,
        "3": 180,
        "4": 180,
        "5": 180,
        "6": 180,
        "7": 180,
        "8": 180,
        "9": 30,
        "10": 20,
        "11": 20,
        "12": 20,
        "13": 1,
        "14": 1,
        "15": 60,
        "16": 30,
        "17": 17,
        "18": 12,
        "19": 8,
        "20": 6,
        "21": 6,
        "22": 6,
        "23": 6,
        "24": 8,
        "25": 12,
        "26": 17,
        "27": 30,
        "28": 60,
        "29": 3,
        "30": 3,
        "31": 3,
        "32": 1,
        "33": 1,
        "34": 1,
        "35": 1,
        "36": 1,
        "37": 1,
        "38": 1,
        "39": 1,
        "40": 1
    }
    myWinPoint.append(singleDouble(recordList))
    myWinPoint.append(bigSmall(recordList))
    myWinPoint = myWinPoint + singleColor(recordList)
    myWinPoint.append(doubleColor(recordList))
    myWinPoint.append(tripleColor(recordList))
    myWinPoint.append(anySingleColor(recordList))
    myWinPoint = myWinPoint + SingleDice(recordList)
    myWinPoint.append(doubleDice(recordList))
    myWinPoint.append(allDice(recordList))
    myWinPoint.append(roundDice(recordList))
    myWinPoint.append(allRoundDice(recordList))
    myWinPoint.append(pointsSum(recordList))
    myStrWinPoint = [str(x) for x in myWinPoint if x is not None]
    sum = 0
    for k, v in bet.items():
        if k in myStrWinPoint:
            if k not in symbolPoints:
                award = v * awardDic.get(k, -2)
                award1 = v * (awardDic.get(k, -2) + 1)
            else:
                if recordList.count(41 - int(k)) == 3:
                    award = v * 3
                    award1 = v * 4
                elif recordList.count(41 - int(k)) == 2:
                    award = v * 2
                    award1 = v * 3
                elif recordList.count(41 - int(k)) == 1:
                    award = v
                    award1 = v * 2
                else:
                    print('error')
        else:
            award = -v
            award1 = -v
        sum += award
    return sum
def singleDouble(diceNum):
    if allRoundDice(diceNum) != 9:
        if sum(diceNum) % 2 == 0:
            return 14
        elif sum(diceNum) % 2 == 1:
            return 1
def bigSmall(diceNum):
    if allRoundDice(diceNum) != 9:
        if 4 <= sum(diceNum) <= 10:
            return 13
        elif 10 <= sum(diceNum) <= 17:
            return 0
def singleColor(diceNum):
    colors = []
    if len([x for x in diceNum if x in REDICE]) == 1:
        colors.append(34)
    if len([x for x in diceNum if x in GREENDICE]) == 1:
        colors.append(33)
    if len([x for x in diceNum if x in BLUEDICE]) == 1:
        colors.append(32)
    return colors
def doubleColor(diceNum):
    if len([x for x in diceNum if x in REDICE]) == 2:
        return 31
    elif len([x for x in diceNum if x in GREENDICE]) == 2:
        return 30
    elif len([x for x in diceNum if x in BLUEDICE]) == 2:
        return 29
def tripleColor(diceNum):
    if len([x for x in diceNum if x in REDICE]) == 3:
        return 10
    elif len([x for x in diceNum if x in GREENDICE]) == 3:
        return 11
    elif len([x for x in diceNum if x in BLUEDICE]) == 3:
        return 12
def anySingleColor(diceNum):
    if len([x for x in diceNum if x in REDICE]) == 3 or len([x for x in diceNum if x in GREENDICE]) == 3 or len([x for x in diceNum if x in BLUEDICE]) == 3:
        return 2
def SingleDice(diceNum):
    awardPointsSum = []
    for i in range(1, 7):
        if diceNum.count(i) == 1:
            awardPointsSum.append(41-i)
    return awardPointsSum
def doubleDice(diceNum):
    for i in range(1, 7):
        if diceNum.count(i) == 2:
            return 41-i
def allDice(diceNum):
    for i in range(1, 7):
        if diceNum.count(i) == 3:
            return 41-i
def roundDice(diceNum):
    for i in range(1, 7):
        if diceNum.count(i) == 3:
            return 9-i
def allRoundDice(diceNum):
    for i in range(1,7):
        if diceNum.count(i) == 3:
            return 9
def pointsSum(diceNum):
    if sum(diceNum) != 3 and sum(diceNum) != 18:
        return 32-sum(diceNum)
    elif sum(diceNum) == 18:
        return 42
    elif sum(diceNum) == 3:
        return 41
def checkWinPoint(record,winPoint):
    recordList = [x for x in record.values()]
    myWinPoint = []
    myWinPoint.append(singleDouble(recordList))
    myWinPoint.append(bigSmall(recordList))
    myWinPoint = myWinPoint + singleColor(recordList)
    myWinPoint.append(doubleColor(recordList))
    myWinPoint.append(tripleColor(recordList))
    myWinPoint.append(anySingleColor(recordList))
    myWinPoint = myWinPoint + SingleDice(recordList)
    myWinPoint.append(doubleDice(recordList))
    myWinPoint.append(allDice(recordList))
    myWinPoint.append(roundDice(recordList))
    myWinPoint.append(allRoundDice(recordList))
    myWinPoint.append(pointsSum(recordList))
    if sorted(winPoint) != sorted([str(x) for x in set(myWinPoint) if x is not None]):
        print('sorted(winPoint)',sorted(winPoint),'sorted([str(x) for x in set(myWinPoint) if x is not None])',sorted([str(x) for x in set(myWinPoint) if x is not None]))
        return False
    return True
def getMul(cardsType):
    cardsType = int(cardsType)
    if -1 <= cardsType <= 6:
        return 1
    elif 7 <= cardsType <= 9:
        return 2
    else:
        return 3
def getMax(handcard,bookmakerCards):
    handcard = sorted(list(map(int,handcard.split(','))))
    bookmakerCards = sorted(list(map(int,bookmakerCards.split(','))))
    for nowIndex in range(0,len(handcard)):
        i = 4 - nowIndex
        if int(handcard[i]/4) > int(bookmakerCards[i]/4):
            return True
        if int(handcard[i]/4) < int(bookmakerCards[i]/4):
            return False
    if handcard[-1] > bookmakerCards[-1]:
        return True
    else:
        return False
    # for nowIndex in range(0,len(handcard)):
    #     i = 4 - nowIndex
    #     if handcard[i] > bookmakerCards[i]:
    #         return True
    #     if handcard[i] < bookmakerCards[i]:
    #         return False
def toPoker(i):
    if 0 <= i <= 39:
        return int(i/4) + 1
    else:
        return 10
def checkCardType(cards,cardsType):
    pointsCards = sorted(list(map(int,cards.split(','))))
    cards = list(map(toPoker,pointsCards))
    for j in itertools.combinations(cards, 3):
        if sum(j) % 10 == 0:
            if sum(cards) % 10 == 0:
                if len([x for x in pointsCards if x > 39]) == 4:
                    cardType = 11
                    break
                elif len([x for x in pointsCards if x > 39]) == 5:
                    cardType = 12
                    break
                cardType = 10
                break
            cardType = sum(cards) % 10
            break
        else:
            cardType = -1
    if list(map(lambda x:int(x/4),pointsCards)).count(list(map(lambda x:int(x/4),pointsCards))[0]) == 4 or list(map(lambda x:int(x/4),pointsCards)).count(list(map(lambda x:int(x/4),pointsCards))[-1]) == 4:
        cardType = 13
    if len([x for x in pointsCards if x <= 15]) == 5 and sum(cards) <= 10:
        cardType = 14
    if cardsType != cardType:
        print('cardsType',cardsType,'cardType',cardType)
        exit(-12)
    return True
def checkBrnnWinPoint(record,bet,gold):
    record = copy.deepcopy(record)
    bet = json.loads(bet)
    bookmaker = record.pop(0)
    for key,value in bookmaker.items():
        bookmakerCards = key
        bookmakerCardsType = int(value)
    checkCardType(bookmakerCards,bookmakerCardsType)
    settlmentMulList = []
    for cards in record:
        for handcard,cardType in cards.items():
            cardType = int(cardType)
            checkCardType(handcard, cardType)
            if cardType > bookmakerCardsType:
                settlmentMul = getMul(cardType)
            elif cardType == bookmakerCardsType:
                if getMax(handcard,bookmakerCards):
                    settlmentMul = getMul(cardType)
                else:
                    settlmentMul = -getMul(bookmakerCardsType)
            else:
                settlmentMul = -getMul(bookmakerCardsType)
            settlmentMulList.append(settlmentMul)
    print(settlmentMulList)
    awardGold = 0
    for betPoint,betGold in bet.items():
        awardGold += betGold * settlmentMulList[int(betPoint)-1]
    if awardGold != gold:
        print('awardGold',awardGold,'gold',gold)
        return False
    return True
def parseYXX(gameType):
    rmbBet = 0
    usdBet = 0
    vnBet = 0
    coinsBet = 0
    rmbSum = 0
    usdSum = 0
    vnSum = 0
    coinsSum  = 0
    personCount = []
    if os.path.exists('yxx.csv'):
        os.remove('yxx.csv')
    loginUrl = 'http://192.168.10.211:8080/login'
    data = {
        'username': 'shu',
        'password': '123456'
    }
    sessions = requests.session()
    response = sessions.post(loginUrl, data=data)
    response = response.json()
    token = response.get("token")
    headers = {
        'Content-Type':'application/json;charset=utf-8',
        'token':token
    }
    data = {
        "gameType":gameType,
        "dateMin":STARTTIME,
        "dateMax":ENDTIME
    }
    data = json.dumps(data)
    url = "http://192.168.10.211:8080/gameRecord/getList"
    response = sessions.post(url = url, headers= headers,data = data)
    response = response.json()
    betPoints = {}
    awardPoints = {}
    roomRecords = {}
    responseData = response['data']
    for records in responseData:#按房间分
        roomCfgId = records['roomInfo']['roomCfgId']
        if roomCfgId not in roomRecords.keys():
            roomRecords[roomCfgId] = [records]
        else:
            temrecords = roomRecords[roomCfgId]
            temrecords.append(records)
            roomRecords[roomCfgId] = temrecords
    lastGoldPool = False
    count = 0
    for roomid,roomsetleRecords in roomRecords.items():#遍历每个房间
        validAmountSum = 0
        awardSum = 0
        recordsnum = len(roomsetleRecords)
        roomsetleRecords.reverse()
        for records in roomsetleRecords:#遍历每一局
            print(roomid, records)
            winPoint = records['roomInfo']['winPoint']
            record = records['roomInfo']['record']
            if checkWinPoint(record,winPoint) == False:
                exit(-7)

            if '9' in records['roomInfo']['winPoint']:
                flag_bz = True
            else:
                flag_bz = False
            roundBetSum = 0
            roundPaySum = 0
            personBetSum = {0:0,1:0,2:0,3:0}
            personAwardSum = {0:0,1:0,2:0,3:0}
            for record in records['settlements']:#遍历每个人
                count += 1
                key = record['key']
                if key not in personCount:
                    personCount.append(key)
                response = sessions.get(url="http://192.168.10.211:8080/gameRecord/getCurrencyType" + "?key=" + key,
                                        headers=headers)
                if response.text == '1':
                    exchangeRate = 1
                    currencyType = 1
                    rmbBet += record['betAmount']
                    rmbSum += record[ 'gold']
                elif response.text == '2':
                    exchangeRate = 0.155
                    currencyType = 2
                    usdBet += record['betAmount']
                    usdSum += record['gold']
                elif response.text == '3':
                    exchangeRate = 3567.48
                    currencyType = 3
                    vnBet += record['betAmount']
                    vnSum += record['gold']
                elif response.text == '0':
                    exchangeRate = 1
                    currencyType = 0
                    coinsBet += record['betAmount']
                    coinsSum += record['gold']
                validAmount = 0
                bets = json.loads(record['bets'])
                if settlementsCheck(bets, records['roomInfo']['record']) != record['gold']:
                    print('结算出错')
                    exit(-8)
                if flag_bz == True:
                    for points, bet in bets.items():
                        validAmount += bet / exchangeRate
                else:
                    for points, bet in bets.items():
                        if points not in ['0', '13', '1', '14']:
                            validAmount += bet / exchangeRate
                    validAmount += abs(bets['0'] - bets['13']) / exchangeRate
                    validAmount += abs(bets['1'] - bets['14']) / exchangeRate
                for value in json.loads(record['bets']).values():
                    personBetSum[currencyType] += value
                for key, value in json.loads(record['WinGolds']).items():
                    if value > 0:
                        personAwardSum[currencyType] += value + json.loads(record['bets'])[key]
                awardSum += record['gold'] / exchangeRate
                validAmountSum += validAmount
            print('personBetSum', personBetSum, 'personAwardSum', personAwardSum)
            for key, value in personAwardSum.items():
                roundBetSum += int(personBetSum[key] / exchangeRate)
                roundPaySum += int(value / exchangeRate)
            roundAwardSum = roundPaySum - roundBetSum
            nowindex = roomsetleRecords.index(records)
            betMap = records['roomInfo']['betMap']
            if roomid not in betPoints.keys():
                tembetMap = {}
                for i in range(0,41):
                    tembetMap[str(i)] = 0
                betPoints[roomid] = tembetMap
            for key, value in betMap.items():
                if value > 0:
                    betPoints[roomid][key] += 1
            winPoint = records['roomInfo']['winPoint']
            if roomid not in awardPoints.keys():
                temwinPoint = {}
                for i in range(0,43):
                    temwinPoint[str(i)] = 0
                awardPoints[roomid] = temwinPoint
            for points in winPoint:
                awardPoints[roomid][points] += 1
            reduceGoldpool = 0
            if records['roomInfo']['goldPool'] < 0:
                exit(-3)
            if not lastGoldPool:
                lastGoldPool = records['roomInfo']['goldPool']
            else:
                print('roundAwardSum',roundAwardSum,'roundBetSum',roundBetSum)
                reduceGoldpool = int(roundAwardSum)
                if reduceGoldpool < 0 :
                    context = decimal.getcontext()  # 获取decimal现在的上下文
                    context.rounding = decimal.ROUND_05UP
                    reduceGoldpool = reduceGoldpool * 0.95
                    reduceGoldpool = str(reduceGoldpool)
                    reduceGoldpoolList = reduceGoldpool.split('.')
                    reduceGoldpoolList[-1] = reduceGoldpoolList[-1].replace('5','6')
                    reduceGoldpool = float(reduceGoldpoolList[0] + '.' + reduceGoldpoolList[-1])
                    reduceGoldpool = round(reduceGoldpool)
                try:
                    if lastGoldPool - reduceGoldpool != records['roomInfo']['goldPool'] and roomsetleRecords[nowindex + 1]['roomInfo']['roundId'] != roomsetleRecords[nowindex]['roomInfo']['roundId'] and roomsetleRecords[nowindex - 1]['roomInfo']['roundId'] != roomsetleRecords[nowindex]['roomInfo']['roundId']:
                        print('reduceGoldpool',reduceGoldpool,'lastGoldPool',lastGoldPool,'nowgoldPool',records['roomInfo']['goldPool'])
                        exit(-2)
                except:
                    pass
                lastGoldPool = records['roomInfo']['goldPool']
        lastGoldPool = False
        print(f'{roomid}房间总有效投注'.format(roomid = roomid),validAmountSum)
        print('{roomid}房间总局数'.format(roomid=roomid),recordsnum)
        with open('yxx.csv','a') as f:
            f.write(f'{roomid}房间总有效投注,{validAmountSum}\n'.format(roomid = roomid,validAmountSum = validAmountSum))
            f.write(f'{roomid}房间总局数,{recordsnum}\n'.format(roomid=roomid,recordsnum = recordsnum))
        betRate = {}
        for key,value in betPoints.items():
            if key == roomid:
                for points,times in value.items():
                    if points not in betRate.keys():
                        betRate[points] = times/recordsnum
                    else:
                        betRate[points] += times/recordsnum
        print(f'{roomid}下注概率'.format(roomid=roomid),betRate)
        with open('yxx.csv','a') as f:
            f.write('{roomid}房间下注概率:\n'.format(roomid=roomid))
            for key,value in betRate.items():
                f.write('{key},{value}%\n'.format(key=key,value=round(value*100,2)))
        awardRate= {}
        for key,value in awardPoints.items():
            if key == roomid:
                for points,times in value.items():
                    if points not in awardRate.keys():
                        awardRate[points] = times/recordsnum
                    else:
                        awardRate[points] += times/recordsnum
        print(f'{roomid}房间开奖概率'.format(roomid = roomid),awardRate)
        print(f'{roomid}房间总输赢'.format(roomid = roomid),awardSum)
        print(f'{roomid}房间总胜率'.format(roomid = roomid),awardSum/validAmountSum)
        with open('yxx.csv','a') as f:
            f.write(f'{roomid}房间开奖概率:\n'.format(roomid = roomid))
            for key, value in awardRate.items():
                f.write('{key},{value}%\n'.format(key=key, value=round(value * 100, 2)))
            f.write('{roomid}房间总输赢:,{awardSum}\n'.format(roomid = roomid,awardSum = awardSum))
            f.write('{roomid}房间总胜率:,{rateSum}%\n'.format(roomid = roomid,rateSum=round(awardSum/validAmountSum * 100, 2)))
    myPrint(coinsBet, coinsSum, rmbBet, rmbSum, usdBet, usdSum, vnBet, vnSum, len(personCount), count)
def parseBRNN(gameType):
    rmbBet = 0
    usdBet = 0
    vnBet = 0
    coinsBet = 0
    rmbSum = 0
    usdSum = 0
    vnSum = 0
    coinsSum = 0
    personCount = []
    loginUrl = 'http://192.168.10.211:8080/login'
    data = {
        'username': 'shu',
        'password': '123456'
    }
    sessions = requests.session()
    response = sessions.post(loginUrl, data=data)
    response = response.json()
    token = response.get("token")
    headers = {
        'Content-Type': 'application/json;charset=utf-8',
        'token': token
    }
    data = {
        "gameType": gameType,
        "dateMin": STARTTIME,
        "dateMax": ENDTIME
    }
    data = json.dumps(data)
    url = "http://192.168.10.211:8080/gameRecord/getList"
    response = sessions.post(url=url, headers=headers, data=data)
    response = response.json()
    betPoints = {}
    awardPoints = {}
    roomRecords = {}
    responseData = response['data']
    for records in responseData:#按房间分
        roomCfgId = records['roomInfo']['roomCfgId']
        if roomCfgId not in roomRecords.keys():
            roomRecords[roomCfgId] = [records]
        else:
            temrecords = roomRecords[roomCfgId]
            temrecords.append(records)
            roomRecords[roomCfgId] = temrecords
    count = 0
    for roomid, roomsetleRecords in roomRecords.items():  # 遍历每个房间
        for records in roomsetleRecords:  # 遍历每一局
            print(records)
            cardsAndTyps = records['roomInfo']['cardsAndTyps']
            for record in records['settlements']:#遍历每个人
                bet = record['bets']
                gold = record['gold']
                if not checkBrnnWinPoint(cardsAndTyps,bet,gold):
                    exit(-11)
                count += 1
                key = record['key']
                if key not in personCount:
                    personCount.append(key)
                response = sessions.get(url="http://192.168.10.211:8080/gameRecord/getCurrencyType" + "?key=" + key,
                                        headers=headers)
                if response.text == '1':
                    exchangeRate = 1
                    currencyType = 1
                    rmbBet += record['betAmount']
                    rmbSum += record['gold']
                elif response.text == '2':
                    exchangeRate = 0.155
                    currencyType = 2
                    usdBet += record['betAmount']
                    usdSum += record['gold']
                elif response.text == '3':
                    exchangeRate = 3567.48
                    currencyType = 3
                    vnBet += record['betAmount']
                    vnSum += record['gold']
                elif response.text == '0':
                    exchangeRate = 1
                    currencyType = 0
                    coinsBet += record['betAmount']
                    coinsSum += record['gold']

    myPrint(coinsBet, coinsSum, rmbBet, rmbSum, usdBet, usdSum, vnBet, vnSum, len(personCount), count)
def parseLB(gameType):
    ms = MSSQL(host='192.168.10.199', user='test', pwd='123456', db="OverseasGame",port=1433)
    ms.GetConnect()
    coinsBet, coinsSum, rmbBet, rmbSum, usdBet, usdSum, vnBet, vnSum = 0, 0, 0, 0, 0, 0, 0, 0
    sql = f"select count(DISTINCT(userName)) from dbo.Game_GameGoldActionInfo where gameType={gameType} AND CreatDate > '{STARTTIME}'AND CreatDate < '{ENDTIME}' and actionType in (2,12)"
    data = ms.ExecQuery(sql)
    personCount = data[0][0]
    sql = f"select count(*),sum(antesNum),sum(goldNum) from dbo.Game_GameGoldActionInfo where gameType={gameType} AND CreatDate > '{STARTTIME}'AND CreatDate < '{ENDTIME}' and actionType in (2,12)"
    data = ms.ExecQuery(sql)
    gameCount,betSum,awardSum = data[0]
    coinsBet = betSum
    coinsSum = awardSum
    myPrint(coinsBet, coinsSum, rmbBet, rmbSum, usdBet, usdSum, vnBet, vnSum, personCount, gameCount)
def myPrint(coinsBet, coinsSum, rmbBet, rmbSum, usdBet, usdSum, vnBet, vnSum,personCount,gameCount):
    if gameCount is None or gameCount == 0:
        return
    if coinsBet is None:
        coinsBet = 0
        coinsSum = 0
    if rmbBet is None:
        rmbBet = 0
        rmbSum = 0
    if usdBet is None:
        usdBet = 0
        usdSum = 0
    if vnBet is None:
        vnBet = 0
        vnSum = 0
    print(f'rmbBet:{rmbBet} , usdBet:{usdBet} , vnBet:{vnBet} , coinsBet:{coinsBet}'.format(rmbBet=rmbBet/100, usdBet=usdBet/100,
                                                                                      vnBet=vnBet/100, coinsBet=coinsBet/100))
    print(f'rmbSum:{rmbSum} , usdSum:{usdSum} , vnSum:{vnSum} , coinsSum:{coinsSum}'.format(rmbSum=rmbSum/100, usdSum=usdSum/100,
                                                                                      vnSum=vnSum/100, coinsSum=coinsSum/100))
    print('personCount', personCount)
    print('count', gameCount,'\n')
def player():
    print('\n')
    print('玩家报表')
    ms = MSSQL(host='192.168.10.199', user='test', pwd='123456', db="OverseasGame", port=1433)
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
    mydoc = queryMangodb()
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
    mydoc = queryMangodb()
    games = {}
    totalBet = {0: 0, 1: 0, 2: 0, 3: 0}
    totalAward = {0: 0, 1: 0, 2: 0, 3: 0}
    totalTax = {0: 0, 1: 0, 2: 0, 3: 0}
    totalGameCount = 0
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
                    games[value] = {'betAmount': betAmount,'profit':profit,'tax':tax,'gameCount':gameCount,}
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
                    games[value] = {'betAmount': betAmount,'profit':profit,'tax':tax,'gameCount':gameCount,}
    for key,value in games.items():
        print(GAMETYPELIST[str(key)],value)
    print(f'总计：投注额:{totalBet},玩家输赢:{totalAward},抽水:{totalTax},游戏次数:{totalGameCount}')
def queryMangodb():
    myclient = pymongo.MongoClient('mongodb://admin:admin@192.168.10.25:27017/OverseasGame?authSource=admin')
    mydb = myclient['OverseasGame']
    monthDate = STARTTIME[0:7]
    mycol = mydb["GameUserCount_" + monthDate]
    myquery = {"startTime": {"$gt": parse(STARTTIME), '$lt': parse(ENDTIME)},"uid":{"$nin":black_List}}
    mydoc = mycol.find(myquery)
    return mydoc
def roomData():
    print('\n')
    print('房间数据')
    mydoc = queryMangodb()
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
        print(gameName,roomName,value['profit'],value['tax'],gameCount,playerCount,'validAmount',betAmount)
def settlementsData():
    users = playerData()
    settlements = {}
    ms = MSSQL(host='192.168.10.199', user='test', pwd='123456', db="OverseasGame", port=1433)
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
    mydoc = queryMangodb()
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
        print(GAMETYPELIST[str(key)],value)
    print(f'总计：投注额:{totalBet},玩家输赢:{totalAward},抽水:{totalTax},游戏人次:{totalPlayerCount},游戏次数:{totalGameCount}')
if __name__ == '__main__':
    global black_List,black_users_list
    ms = MSSQL(host='192.168.10.199', user='test', pwd='123456', db="OverseasGame", port=1433)
    ms.GetConnect()
    sql = f"SELECT login.id FROM dbo.Game_UserLoginInfo as login RIGHT JOIN (select userInfo.id from dbo.Game_UserInfoBase as userInfo RIGHT JOIN  dbo.ReportBlacks as black on userInfo.userName = black.userName and userInfo.style =  black.style) as blackId on login.uid = blackId.id WHERE login.style <> 00000"
    black_List = [x[0] for x in ms.ExecQuery(sql)]
    tuple_black_List = str(black_List).replace('[','(').replace(']',')')
    sql = "SELECT (userName + '-' + style) from dbo.ReportBlacks"
    black_users_list = str([x[0] for x in ms.ExecQuery(sql)]).replace('[', '(').replace(']', ')')
    # for gameType,gameName in GAMETYPELIST.items():
    #     if gameType == "200":
    #         print('gametype'+gameName)
    #         parseYXX(gameType)
    #     elif gameType == "34":
    #         print(gameName)
    #         parseBRNN(gameType)
    #     else:
    #         print('gametype' + gameName)
    #         parseLB(gameType)
    gameReport()
    player()
    gameData()
    roomData()
    settlementsData()
