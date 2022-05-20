import requests,json,random,itertools,copy
from logAnalysisUtil import *
pokerList = ['a','b','c','d','e','f']


def getHs(point):
    award = []
    award2 = []
    for i in range(1, len(point)):
        if point[-i] in pokerList:
            award.append(point[-i])
            if len(award) > 2:
                c = ''
                for x in award:
                    a = pokerList.index(x) + 1
                    award2.append(a)
                    c += str(a)+','
                award3 = c[:-1]
                award2.sort()
                return award, award2, award3
    if len(award) < 3:
        num = []
        for i in point[::-1]:
            if i in ('0', '1', '2','3','4','5','6','7','8','9') and len(num) < 18:
                num.append(int(i))
        return


def parseThirtyWater():
    errorRounds = []
    gameType = 234
    userName = 'ada'
    pwd = 'ada'
    startTime = "2022-05-18 00:00:00"
    endTime = "2022-05-20 23:52:28"
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
            winPoint = roomInfo['winPoint']
            award = sorted([int(x) for x in winPoint[0][::2]])
            a, b, c = getHs(hashChain)
            if c != winPoint[0]:
                print('随机排序', c, winPoint[0])
                if b != award:
                    print("开奖错误", winPoint[0], c)
                    return


if __name__ == '__main__':
    parseThirtyWater()
    # getHs('a26b78fbb1ebb3464371352217219e255f4494ec6abb3cec323cf4ca6e191b64')
