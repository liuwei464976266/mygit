import requests,json,random,itertools,copy
from logAnalysisUtil import *
pokerList = [
        [1, '方块', '2', 1],
        [2, '梅花', '2', 1],
        [3, '红桃', '2', 1],
        [4, '黑桃', '2', 1],
        [1, '方块', '3', 2],
        [2, '梅花', '3', 2],
        [3, '红桃', '3', 2],
        [4, '黑桃', '3', 2],
        [1, '方块', '4', 3],
        [2, '梅花', '4', 3],
        [3, '红桃', '4', 3],
        [4, '黑桃', '4', 3],
        [1, '方块', '5', 4],
        [2, '梅花', '5', 4],
        [3, '红桃', '5', 4],
        [4, '黑桃', '5', 4],
        [1, '方块', '6', 5],
        [2, '梅花', '6', 5],
        [3, '红桃', '6', 5],
        [4, '黑桃', '6', 5],
        [1, '方块', '7', 6],
        [2, '梅花', '7', 6],
        [3, '红桃', '7', 6],
        [4, '黑桃', '7', 6],
        [1, '方块', '8', 7],
        [2, '梅花', '8', 7],
        [3, '红桃', '8', 7],
        [4, '黑桃', '8', 7],
        [1, '方块', '9', 8],
        [2, '梅花', '9', 8],
        [3, '红桃', '9', 8],
        [4, '黑桃', '9', 8],
        [1, '方块', '10', 9],
        [2, '梅花', '10', 9],
        [3, '红桃', '10', 9],
        [4, '黑桃', '10', 9],
        [1, '方块', 'J', 10],
        [2, '梅花', 'J', 10],
        [3, '红桃', 'J', 10],
        [4, '黑桃', 'J', 10],
        [1, '方块', 'Q', 11],
        [2, '梅花', 'Q', 11],
        [3, '红桃', 'Q', 11],
        [4, '黑桃', 'Q', 11],
        [1, '方块', 'K', 12],
        [2, '梅花', 'K', 12],
        [3, '红桃', 'K', 12],
        [4, '黑桃', 'K', 12],
        [1, '方块', 'A', 13],
        [2, '梅花', 'A', 13],
        [3, '红桃', 'A', 13],
        [4, '黑桃', 'A', 13]
    ]
new_pokerList = tuple(zip([x[0] for x in pokerList],[x[-1] for x in pokerList]))

def getHs(point):
    if point in ('0','1','2','3'):
        return 1
    elif point in ('4','5','6','7'):
        return 2
    elif point in ('8','9','a','b'):
        return 3
    elif point in ('c','d','e','f'):
        return 4
    return -1
def getCard(point):
    if point in ('0','1','2','3','4','5','6','7','8','9'):
        return int(point) + 1
    elif point == 'a':
        return 11
    elif point == 'b':
        return 11
    elif point == 'c':
        return 12
    elif point == 'd':
        return 12
    elif point == 'e':
        return 13
    elif point == 'f':
        return 13
    return -1
def parseThirtyWater():
    errorRounds = []
    gameType = 230
    userName = 'ada'
    pwd = 'ada'
    startTime = "2022-05-25 18:00:00"
    endTime = "2022-05-26 23:52:28"
    record = Record(userName,pwd,gameType,startTime,endTime)
    roomRecords = record.organizeRecords()
    count = 0
    for roomid, roomsetleRecords in roomRecords.items():  # 遍历每个房间
        roomsetleRecords.sort(key=lambda x:x['roomInfo']['endTime'])
        for records in roomsetleRecords:  # 遍历每一局

            print(records)
            settlements = records['settlements']
            roomInfo = records['roomInfo']
            roundId = roomInfo['roundId']
            if roundId in errorRounds:#过滤掉异常局号
                continue
            antes = roomInfo['roomScore']
            hashChain = roomInfo['hashChain']
            hashChain = 'f67f38ed31b1f651088a5bc6eda350f708f16e835831a78cea50b036bb61b2e4'
            cardsAndTyps = roomInfo['cardsAndTyps']
            print(cardsAndTyps)
            selerctHashChain = hashChain[-26:]
            print('hashChain:', selerctHashChain)
            bankerCards = []
            tianCards = []
            diCards = []
            xuanCards = []
            huangCards = []
            for i in range(len(selerctHashChain)):
                if i in range(0,5):
                    point = selerctHashChain[i]
                    nextPoint = selerctHashChain[i + 1]
                    hs = getHs(point)
                    card = getCard(nextPoint)
                    realCardNo = new_pokerList.index((hs,card))
                    bankerCards.append(str(realCardNo))
                if i in range(5,10):
                    point = selerctHashChain[i]
                    nextPoint = selerctHashChain[i + 1]
                    hs = getHs(point)
                    card = getCard(nextPoint)
                    realCardNo = new_pokerList.index((hs,card))
                    tianCards.append(str(realCardNo))
                if i in range(10,15):
                    point = selerctHashChain[i]
                    nextPoint = selerctHashChain[i + 1]
                    hs = getHs(point)
                    card = getCard(nextPoint)
                    realCardNo = new_pokerList.index((hs,card))
                    diCards.append(str(realCardNo))
                if i in range(15,20):
                    point = selerctHashChain[i]
                    nextPoint = selerctHashChain[i + 1]
                    hs = getHs(point)
                    card = getCard(nextPoint)
                    realCardNo = new_pokerList.index((hs,card))
                    xuanCards.append(str(realCardNo))
                if i in range(20,25):
                    point = selerctHashChain[i]
                    nextPoint = selerctHashChain[i + 1]
                    hs = getHs(point)
                    card = getCard(nextPoint)
                    realCardNo = new_pokerList.index((hs,card))
                    huangCards.append(str(realCardNo))
            if list(cardsAndTyps[0].keys())[0].split(',') != bankerCards:
                print('bankerCards',bankerCards)
                # exit(-1)
            if list(cardsAndTyps[1].keys())[0].split(',') != tianCards:
                print('tianCards', tianCards)
                # exit(-1)
            if list(cardsAndTyps[2].keys())[0].split(',') != diCards:
                print('diCards', diCards)
                # exit(-1)
            if list(cardsAndTyps[3].keys())[0].split(',') != xuanCards:
                print('xuanCards', xuanCards)
                # exit(-1)
            if list(cardsAndTyps[4].keys())[0].split(',') != huangCards:
                print('huangCards', huangCards)
                exit(-1)


if __name__ == '__main__':
    parseThirtyWater()

