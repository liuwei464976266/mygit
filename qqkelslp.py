from logAnalysisUtil import *
import json, random
from enum import Enum, unique
numberBet = (tuple(range(1,13)),tuple(range(13,25)),tuple(range(25,37)))
smallBet = tuple(range(1,19))
bigBet = tuple(range(9,37))
singleBet = tuple(range(1,37,2))
doubleBet = tuple(range(2,37,2))
redBet = (1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36)
blackBet = (2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35)
bet0 = (0,)
rowBet = (tuple(range(3,37,3)),tuple(range(2,36,3)),tuple(range(1,35,3)))
twoPointBet = ((1, 2),(4, 5),(7, 8),(10, 11),(13, 14),(16, 17),(19, 20),(22, 23),(25, 26),(28, 29),(31, 32),(34, 35),(2, 3),(5, 6),(8, 9),(11, 12),(14, 15),(17, 18),(20, 21),(23, 24),(26, 27),(29, 30),(32, 33),(35, 36),(1, 4),(2, 5),(3, 6),(4, 7),(5, 8),(6, 9),(7, 10),(8, 11),(9, 12),(10, 13),(11, 14),(12, 15),(13, 16),(14, 17),(15, 18),(16, 19),(17, 20),(18, 21),(19, 22),(20, 23),(21, 24),(22, 25),(23, 26),(24, 27),(25, 28),(26, 29),(27, 30),(28, 31),(29, 32),(30, 33),(31, 34),(32, 35),(33, 36))
two0PointBet =((0,1),(0,2),(0,3))
threePointBet = ((1, 2, 3),(4, 5, 6),(7, 8, 9),(10, 11, 12),(13, 14, 15),(16, 17, 18),(19, 20, 21),(22, 23, 24),(25, 26, 27),(28, 29, 30),(31, 32, 33),(34, 35, 36))
three0PointBet = ((0,1,2),(0,2,3))
sixPointBet = ((1, 2, 3, 4, 5, 6),(4, 5, 6, 7, 8, 9),(7, 8, 9, 10, 11, 12),(10, 11, 12, 13, 14, 15),(13, 14, 15, 16, 17, 18),(16, 17, 18, 19, 20, 21),(19, 20, 21, 22, 23, 24),(22, 23, 24, 25, 26, 27),(25, 26, 27, 28, 29, 30),(28, 29, 30, 31, 32, 33),(31, 32, 33, 34, 35, 36))
fourPointBet = ((1, 2, 4, 5),(4, 5, 7, 8),(7, 8, 10, 11),(10, 11, 13, 14),(13, 14, 16, 17),(16, 17, 19, 20),(19, 20, 22, 23),(22, 23, 25, 26),(25, 26, 28, 29),(28, 29, 31, 32),(31, 32, 34, 35),(2, 3, 5, 6),(5, 6, 8, 9),(8, 9, 11, 12),(11, 12, 14, 15),(14, 15, 17, 18),(17, 18, 20, 21),(20, 21, 23, 24),(23, 24, 26, 27),(26, 27, 29, 30),(29, 30, 32, 33),(32, 33, 35, 36))

odds = {
    (0,):35,
    tuple(range(1,37)):35,
    tuple(range(37,40)):2,
    tuple(range(40,46)):1,
    tuple(range(46,49)):2,
    tuple(range(49,61)):11,
    tuple(range(61,118)):17,
    tuple(range(118,129)):5,
    tuple(range(129,151)):8,
    tuple(range(151,154)):17,
    tuple(range(154,156)):11

}
def getPoint(num):
    return num
def getPointRange(num):
    for i in range(len(numberBet)):
        if num in numberBet[i]:
            return 37 + i
def getBigSmall(num):
    if num in smallBet:
        return 40
    elif num in bigBet:
        return 45
def getSingleDouble(num):
    if num in singleBet:
        return 44
    elif num in doubleBet:
        return 41
def getRedBlack(num):
    if num in redBet:
        return 42
    elif num in blackBet:
        return 43
def getRowNum(num):
    for i in range(len(rowBet)):
        if num in rowBet[i]:
            return 46 + i
def getTwoPoint(num):
    points = []
    for i in range(len(twoPointBet)):
        if num in twoPointBet[i]:
            points.append(61 + i)
    for i in range(len(two0PointBet)):
        if num in two0PointBet[i]:
            points.append(151 + i)
    return points
def getThreePoint(num):
    points = []
    for i in range(len(threePointBet)):
        if num in threePointBet[i]:
            points.append(49 + i)
    for i in range(len(three0PointBet)):
        if num in three0PointBet[i]:
            points.append(154 + i)
    return points
def getFourPoint(num):
    points = []
    for i in range(len(fourPointBet)):
        if num in fourPointBet[i]:
            points.append(129 + i)
    return points
def getSixPoint(num):
    points = []
    for i in range(len(sixPointBet)):
        if num in sixPointBet[i]:
            points.append(118 + i)
    return points
def strList(lists):
    if lists is None:
        return ""
    elif isinstance(lists,list):
        if lists == []:
            return ""
        else:
            return "|".join(map(str,lists))
    return str(lists)
def deepAppend(list1,list2):
    if isinstance(list2,list):
        for i in list2:
            list1.append(i)
    else:
        list1.append(list2)
    return list1
def getawardBetPointsDic():
    awardBetPointsDic = {}
    writeableBetPointsDic = {}
    for num in range(0,37):
        awardBetPoints = []
        writeableBetPoints = []
        awardBetPoint = getPoint(num)
        writeableBetPoints.append(awardBetPoint)
        if awardBetPoint or awardBetPoint == 0:
            awardBetPoints.append(awardBetPoint)
        awardBetPoint = getPointRange(num)
        writeableBetPoints.append(awardBetPoint)
        if awardBetPoint:
            awardBetPoints.append(awardBetPoint)
        awardBetPoint = getBigSmall(num)
        writeableBetPoints.append(awardBetPoint)
        if awardBetPoint:
            awardBetPoints.append(awardBetPoint)
        awardBetPoint = getSingleDouble(num)
        writeableBetPoints.append(awardBetPoint)
        if awardBetPoint:
            awardBetPoints.append(awardBetPoint)
        awardBetPoint = getRedBlack(num)
        writeableBetPoints.append(awardBetPoint)
        if awardBetPoint:
            awardBetPoints.append(awardBetPoint)
        awardBetPoint = getRowNum(num)
        writeableBetPoints.append(awardBetPoint)
        if awardBetPoint:
            awardBetPoints.append(awardBetPoint)
        awardBetPoint = getTwoPoint(num)
        writeableBetPoints.append(awardBetPoint)
        if awardBetPoint:
            awardBetPoints = deepAppend(awardBetPoints, awardBetPoint)
        awardBetPoint = getThreePoint(num)
        writeableBetPoints.append(awardBetPoint)
        if awardBetPoint:
            awardBetPoints = deepAppend(awardBetPoints, awardBetPoint)
        awardBetPoint = getFourPoint(num)
        writeableBetPoints.append(awardBetPoint)
        if awardBetPoint:
            awardBetPoints = deepAppend(awardBetPoints, awardBetPoint)
        awardBetPoint = getSixPoint(num)
        writeableBetPoints.append(awardBetPoint)
        if awardBetPoint:
            awardBetPoints = deepAppend(awardBetPoints, awardBetPoint)
        awardBetPointsDic[num] = awardBetPoints
        writeableBetPointsDic[num] = writeableBetPoints

    return awardBetPointsDic,writeableBetPointsDic
def getPointGold(point):
    for key,value in odds.items():
        if point in key:
            return value
def getHs(point):
    if point in ('0','1','2','3'):
        return 0
    elif point in ('4','5','6','7'):
        return 1
    elif point in ('8','9','a','b'):
        return 2
    elif point in ('c','d','e','f'):
        return 3
    return -1
def getCard(hashChain):
    print(hashChain)
    for i in range(len(hashChain)):
        print("i",i)
        if i == 0:
            index_flag = 0
        reverseIndex = len(hashChain) - i -1
        sw = getHs(hashChain[reverseIndex])
        for n in range(index_flag,len(hashChain)):
            print("n",n)
            index_flag = n + 1
            if hashChain[n] not in ('a', 'b', 'c', 'e', 'f', 'd'):
                gw = int(hashChain[n])
                break
            else:
                continue
        result = sw * 10 + gw
        print(result)
        if result >= 37:
            continue
        else:
            break
    return result
def settments(bets,point,awardBetPointsDic):
    gold = 0
    awardBets = awardBetPointsDic[point]
    for point,bet in bets.items():
        if bet > 0:
            point = int(point)
            if point in awardBets:
                gold += getPointGold(point) * bet
            else:
                gold -= bet
    return gold

def random_hex(length):
    result =hex(random.randint(0,16**length)).replace('0x','').upper()
    if(len(result)<length):
            result ='0'*(length-len(result))+result
    return result

def main():

    bet = 100
    awardBetPointsDic, writeableBetPointsDic = getawardBetPointsDic()
    rusult = {}
    bet_result = {}
    for bet_point in range(0,156):
        initGold = 10000
        for i in range(10000):
            # url = "http://192.168.10.212:11111/getTronId?gametype=qkldb&rid=0.000001"
            # try:
            #     response = requests.get(url)
            # except:
            #     time.sleep(10)
            #     response = requests.get(url)
            # response = response.json()
            # hashChain = response['txId']
            hashChain = str(random_hex(64)).lower()
            numResult = getCard(hashChain)
            if not numResult:
                continue
            point = numResult
            times = rusult.get(point,0)
            times += 1
            rusult.update({point:times})
            my_win_point = sorted(awardBetPointsDic.get(point))
            if bet_point in my_win_point:
                initGold += bet * getPointGold(bet_point)
            else:
                initGold -= bet
        print("initGOLD",initGold)
        for i in sorted(rusult.keys()):
            print(i,rusult[i])
        bet_result[bet_point] = initGold
    for i in sorted(bet_result.keys()):
        print(i,bet_result[i])


if __name__ == '__main__':
    main()
    # re_odds = {}
    # for key,value in odds.items():
    #     re_odds[value] = re_odds.get(value,[]) + list(key)
    # for key,value in re_odds.items():
    #     print(key,value)

