import requests, json, random, itertools, copy
from logAnalysisUtil import *

pokerList = ['a', 'b', 'c', 'd', 'e', 'f']
poker = ['01','02','03','11','12','13','21','22','23']
def getHs(point):
    award = []
    award2 = []
    for i in range(1, len(point)):
        if point[-i] in pokerList:
            award.append(point[-i])
            if len(award) > 1:
                c = ''
                for x in award:
                    a = pokerList.index(x)
                    award2.append(a % 3+1)
                    c += str(a % 3+1) + ','
                award3 = c[:-1]
                print(award, award2, award3)
                return award, award2, award3
    if len(award) < 2:
        num = []
        for i in point[::-1]:
            if i in ('1', '2', '3', '4', '5', '6', '7', '8', '9') and len(num) < 2:
                num.append(int(i))
                num = [i % 3 for i in num]
                num1 = [(i % 3)+1 for i in num]
                print(num)
        return num, num, 3


def parseThirtyWater():
    errorRounds = [554482681668878848,554483075883123200]
    gameType = 235
    userName = 'ada'
    pwd = 'ada'
    startTime = "2022-05-26 16:59:00"
    endTime = "2022-05-27 17:00:28"
    record = Record(userName, pwd, gameType, startTime, endTime)
    roomRecords = record.organizeRecords()
    count = 0
    for roomid, roomsetleRecords in roomRecords.items():  # 遍历每个房间
        roomsetleRecords.sort(key=lambda x: x['roomInfo']['endTime'])
        for records in roomsetleRecords:  # 遍历每一局
            print(records)
            settlements = records['settlements']
            roomInfo = records['roomInfo']
            roundId = roomInfo['roundId']
            if roundId in errorRounds:  # 过滤掉异常局号
                continue
            antes = roomInfo['roomScore']
            hashChain = roomInfo['hashChain']
            cardsAndTyps = roomInfo['cardsAndTyps']
            # print(cardsAndTyps)
            a, b, c = getHs(hashChain)
            card = [i for i in cardsAndTyps.items()]
            print(222, card)
            ca, car = card[0]
            ca = eval(ca)
            if ca != b:
                print('石头剪刀布开奖错误')
                return
            group = ['', '']
            '''moban'''
            # if abs(ca[0]-ca[1]) == 2:
            #     group[0] = ca.index(3)
            #     group[1] = (ca.index(3)+1)*5
            # elif abs(ca[0]-ca[1]) == 1:
            #     group[0] = ca.index(min(ca))
            #     group[1] = ca.index(min(ca))

            if ca == [1, 2] or ca == [2, 3] or ca == [3, 1]:
                group[0] = 0
                ss = str(group[0]) + str(ca[0])
            elif ca == [2, 1] or ca == [3, 2] or ca == [1, 3]:
                group[0] = 2
                ss = str(group[0]) + str(ca[1])
            else:
                group[0] = 1
                ss = str(group[0]) + str(min(ca))
            group[1] = poker.index(ss)+3
            print('开奖数据---', cardsAndTyps)
            print('me解析的开奖数据---', a, '-', b, '-', group)
            if group != car:
                print("二级开奖点位错误")
                return


if __name__ == '__main__':
    parseThirtyWater()
    # getHs('8618af59929b5c0beca782047980d292b0a12a7e30f00e63f29359659b1f7e62')
