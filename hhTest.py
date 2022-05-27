import requests,json,random,itertools,copy,math,time
from logAnalysisUtil import *
STARTTIME = "2022-05-19 18:00:00"
ENDTIME = "2022-05-20 23:52:28"
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
CARDGONGZAI = ([1, '方块', 'J', 11],
        [2, '梅花', 'J', 11],
        [3, '红桃', 'J', 11],
        [4, '黑桃', 'J', 11],
        [1, '方块', 'Q', 12],
        [2, '梅花', 'Q', 12],
        [3, '红桃', 'Q', 12],
        [4, '黑桃', 'Q', 12],
        [1, '方块', 'K', 13],
        [2, '梅花', 'K', 13],
        [3, '红桃', 'K', 13],
        [4, '黑桃', 'K', 13])
ERRORROUND = [552059025634231808]
CARDA = [[1, '方块', 'A', 13],
        [2, '梅花', 'A', 13],
        [3, '红桃', 'A', 13],
        [4, '黑桃', 'A', 13]]
AWARDDIC = {
    6:9,
    5:5,
    4:2,
    3:1.5,
    2:1
}
new_pokerList = tuple(zip([x[0] for x in pokerList],[x[-1] for x in pokerList]))
def check_straight_flush(hand):
    """检测是不是同花顺"""
    if check_flush(hand) and check_straight(hand):
        return True
    else:
        return False
def checkBaoZi(hand):
    if len(set([x[-1] for x in hand])) == 1:
        return True
    return False
def check_flush(list):
    list1 = []
    for i in list:
        if i[0] not in list1 :
            list1.append(i[0])
    if len(list1)==1:
        return True
    return False
def exchangeA(hand):
    hands = copy.deepcopy(hand)
    for card in hand:
        if card in CARDA:
            hands.remove(card)
            hands.append([card[0], card[1], card[2], 0])
            return hands
    return hands
def check_straight(hand):
    preNum = 0
    handsCards = copy.deepcopy(hand)
    handsCards = exchangeA(handsCards)
    handsCards = sorted(handsCards, key=lambda x: x[-1])  # 按牌的大小排序
    for i in range(1,len(handsCards)):
        if handsCards[i][3] - handsCards[i-1][3] == 1:
            preNum += 1
    if preNum == len(hand)-1:
        return True
    #下面为为替换
    preNum = 0
    handsCards = copy.deepcopy(hand)
    handsCards = sorted(handsCards, key=lambda x: x[-1])  # 按牌的大小排序
    for i in range(1, len(handsCards)):
        if handsCards[i][3] - handsCards[i - 1][3] == 1:
            preNum += 1
    if preNum == len(hand) - 1:
        return True
    return False
def check_full_house(hand):
    """ 检测是不是三张相同加一个对子"""
    frequencies = {}
    frequencies_list = []
    ranks = [i[2] for i in hand]
    for rank in ranks:
        if rank not in frequencies:
            frequencies[rank] = 1
        else:
            frequencies[rank] += 1

    for frequency in frequencies.values():
        frequencies_list.append(int(frequency))

    frequencies_list.sort()

    if frequencies_list[0] == 2:
        return True
    else:
        return False
def check_one_pairs(hand):
    """检测是不是一个对子"""
    frequencies = {}
    frequencies_list = []
    ranks = [i[2] for i in hand]
    for rank in ranks:
        if rank not in frequencies:
            frequencies[rank] = 1
        else:
            frequencies[rank] += 1

    for frequency in frequencies.values():
        frequencies_list.append(int(frequency))
    frequencies_list.sort()
    if frequencies_list[0] == 1 and frequencies_list[1] == 2:
        return True
    else:
        return False
def check_one_type_color(hand):
    if len(set([x[0] for x in hand])) == 1:
        return True
    return False
def checkDiLong(hand):
    if sorted([x[-1] for x in hand]) == [1,2,4]:
        return True
    return False
def getCardsType(hand):
    if checkBaoZi(hand):
        return 6
    elif check_straight_flush(hand):
        return 5
    elif check_one_type_color(hand):
        return 4
    elif check_straight(hand):
        return 3
    elif check_one_pairs(hand):
        return 2
    elif checkDiLong(hand):
        return 0
    else:
        return 1
def cardToPoint(card):
    return pokerList.index(card)
def getPoints(card):
    if card in CARDGONGZAI:
        return 0
    else:
        return card[-1]
def cardToStrPoint(card):
    point = card[-1]
    return point
def cardToStrPoint(point):
    point = str(point)
    if len(point) == 1:
        point = "0" + point
    return point
def getWeight(hand):
    cardsType = getCardsType(hand)
    baozi = "00"
    shunJin = "000000"
    jinHua = "000000"
    shunZi = "000000"
    duiZi = "000000"
    danZhang = "000000"
    if cardsType == 6:
        baozi = str(hand[0][-1])
        if len(baozi) == 1:
            baozi = "0" + baozi
    if cardsType == 5:
        shunJin = [x[-1] for x in hand]
        shunJin.sort(reverse=True)
        if shunJin == [13,2,1]:
            shunJin = [2,1,0]
        shunJin = "".join(list(map(cardToStrPoint,shunJin)))
    if cardsType == 4:
        jinHua = [x[-1] for x in hand]
        jinHua.sort(reverse=True)
        jinHua = "".join(list(map(cardToStrPoint,jinHua)))
    if cardsType == 3:
        shunZi = [x[-1] for x in hand]
        shunZi.sort(reverse=True)
        if shunZi == [13,2,1]:
            shunZi = [2,1,0]
        shunZi = "".join(list(map(cardToStrPoint,shunZi)))
    if cardsType == 2:
        duiZiList = [x[-1] for x in hand]
        duiZi = []
        for i in duiZiList:
            if duiZiList.count(i) == 2:
                duiZi.append(i)
        for i in duiZiList:
            if duiZiList.count(i) == 1:
                duiZi.append(i)
        duiZi = "".join(list(map(cardToStrPoint,duiZi)))
    if cardsType == 1:
        danZhang = [x[-1] for x in hand]
        danZhang.sort(reverse=True)
        danZhang = "".join(list(map(cardToStrPoint,danZhang)))
    weight = int(baozi + shunJin + jinHua + shunZi + duiZi + danZhang)
    return weight
def getMaxPoint(hand,type):
    card = []
    if type == 2:
        card1 = [x[-1] for x in hand]
        for i in range(len(card1)):
            if card1.count(card1[i]) == 2:
                card.append(pokerList.index(hand[i]))
        sortedCard = sorted(card,reverse=True)
        for i in range(len(card1)):
            if card1.count(card1[i]) == 1:
                card.append(pokerList.index(hand[i]))
    else:
        card = [pokerList.index(x) for x in hand]
        sortedCard = sorted(card,reverse=True)
    sortedCard = list(map(lambda x:"%02d" % x,sortedCard))
    point = int("".join(sortedCard))
    return point
def getMaxPoint1(hand,type):
    card = []
    if type == 2:
        card1 = [x[-1] for x in hand]
        for i in range(len(card1)):
            if card1.count(card1[i]) == 2:
                card.append(pokerList.index(hand[i]))
    else:
        card = [pokerList.index(x) for x in hand]
    point = max(card)
    return point
def compareCards(hand1,hand2,type1,type2):
    weight1 = getWeight(hand1)
    weight2 = getWeight(hand2)
    if sorted((type1,type2)) != [0,6]:
        if weight1 == weight2:
            weight1 = getMaxPoint(hand1,type1)
            weight2 = getMaxPoint(hand2,type2)
    else:
        if type1 == 0:
            weight1 = 999999999999999999999999999999999999999999
        else:
            weight2 = 999999999999999999999999999999999999999999
    if weight1 > weight2:
        return True
    elif weight1 < weight2:
        return False
    else:
        return True
def checkMul(hand,mul):
    cardsTyoe = getCardsType(hand)
    if cardsTyoe == 4:
        myMul = 5
    elif cardsTyoe == 3:
        myMul = 4
    elif cardsTyoe == 2:
        myMul = 3
    elif cardsTyoe == 1:
        point = sum(list(map(getPoints, hand))) % 10
        if point >= 7:
            myMul = 2
        else:
            myMul = 1
    if myMul == mul:
        return True
    return False
def getHs(point):
    if point in ('0','4','8','c'):
        return 1
    elif point in ('1','5','9','d'):
        return 2
    elif point in ('2','6','a','e'):
        return 3
    elif point in ('3','7','b','f'):
        return 4
    return -1
def getCard(point):
    if point in ('0','1','2','3','4','5','6','7','8','9'):
        return int(point) + 1
    elif point == 'a':
        return 11
    elif point == 'b':
        return 12
    elif point == 'c':
        return 13
    return -1
def parseRedBlack():
    # global usersNgold
    # usersNgold = {}
    # gameType = 232
    # userName = 'ada'
    # pwd = 'ada'
    # startTime = "2022-05-1 18:00:00"
    # endTime = "2022-05-20 09:00:28"
    # record = Record(userName, pwd, gameType, startTime, endTime)
    # roomRecords = record.organizeRecords()
    # lastGoldPool = False

    count = 0
    initGold = 10000
    duizi = 0
    shunzi = 0
    tonghua = 0
    tonghuashun = 0
    baozi = 0
    # for roomid, roomsetleRecords in roomRecords.items():  # 遍历每个房间
    #     roomsetleRecords.sort(key=lambda x:x['roomInfo']['endTime'])
        # if 77 <= roomid <= 82:
        #     reduceGold = 5
        # if roomid == 81:
        #     reduceGold = 10
        # for records in roomsetleRecords:  # 遍历每一局
        # print(records)
        # roomInfo = records['roomInfo']
        # if roomInfo['roundId'] in ERRORROUND:
        #     continue
        # roomMul = int(roomInfo['roomScore'])
        # cardsAndTyps = roomInfo['cardsAndTyps']
        # redCard = [int(list(cardsAndTyps[0].keys())[0]),int(list(cardsAndTyps[1].keys())[0]),int(list(cardsAndTyps[2].keys())[0])]
        # blackCard = [int(list(cardsAndTyps[3].keys())[0]), int(list(cardsAndTyps[4].keys())[0]),
        #            int(list(cardsAndTyps[5].keys())[0])]
    sqTimes = 0
    jqTimes = 0
    # tast_list = list(range(52))

    # x = [[a, b, c] for a in tast_list for b in tast_list for c in tast_list]

    for i in range(10000):
        url = "http://192.168.10.212:11111/getTronId?gametype=qkldb&rid=0.000001"
        try:
            response = requests.get(url)
        except:
            time.sleep(10)
            response = requests.get(url)
        response = response.json()
        hashChain = response['txId']
        count += 1
        selerctHashChain = hashChain[-6:]
        hsList = list(map(getHs, selerctHashChain))
        resultCards = []
        for i in range(len(hashChain)):
            point = hashChain[i]
            card = getCard(point)
            if card == -1:
                continue
            resultCards.append(card)
            if len(resultCards) >= 6:
                break
        realCardNo = []
        for i in range(6):
            realCardNo.append(new_pokerList.index((hsList[i], resultCards[i])))
        redCard = realCardNo[0:3]
        blackCard = realCardNo[3:6]
        blackCard = [pokerList[int(x)] for x in blackCard]
        redCard = [pokerList[int(x)] for x in redCard]
        redType = getCardsType(redCard)
        blackType= getCardsType(blackCard)
        bets = {"3":500,"1":0,"2":0}
        for betPoint,betAmout in bets.items():
            if betAmout == 0:
                continue
            # if betPoint == "1":
            #     if compareCards(redCard,blackCard,redType,blackType):
            #         currentGold = betAmout
            #     else:
            #         currentGold = -betAmout
            # if betPoint == "2":
            #     if compareCards(redCard,blackCard,redType,blackType):
            #         currentGold = -betAmout
            #     else:
            #         currentGold = betAmout
            if betPoint == "3":
                currentGold = -betAmout
                if compareCards(redCard,blackCard,redType,blackType):
                    if redType > 1:


                        if redType == 2 and getMaxPoint1(redCard,redType) < 28:
                            currentGold = -betAmout
                        elif redType == 2 and getMaxPoint1(redCard,redType) >= 28:
                            duizi += 1
                            currentGold = AWARDDIC[redType] * betAmout * 0.95
                        elif redType == 3:
                            shunzi += 1
                            currentGold = AWARDDIC[redType] * betAmout * 0.95
                        elif redType == 4:
                            tonghua += 1
                            currentGold = AWARDDIC[redType] * betAmout * 0.95
                        elif redType == 5:
                            tonghuashun += 1
                            currentGold = AWARDDIC[redType] * betAmout * 0.95
                        elif redType == 6:
                            baozi += 1
                            currentGold = AWARDDIC[redType] * betAmout * 0.95
                    else:
                        currentGold = -betAmout
                else:
                    if blackType > 1:
                        if blackType == 2 and getMaxPoint1(blackCard,blackType) < 28:
                            currentGold = -betAmout
                        elif blackType == 2 and getMaxPoint1(blackCard, blackType) >= 28:
                            currentGold = AWARDDIC[blackType] * betAmout * 0.95
                            duizi += 1
                        elif blackType == 3:
                            shunzi += 1
                            currentGold = AWARDDIC[blackType] * betAmout * 0.95
                        elif blackType == 4:
                            tonghua += 1
                            currentGold = AWARDDIC[blackType] * betAmout * 0.95
                        elif blackType == 5:
                            tonghuashun += 1
                            currentGold = AWARDDIC[blackType] * betAmout * 0.95
                        elif blackType == 6:
                            baozi += 1
                            currentGold = AWARDDIC[blackType] * betAmout * 0.95
                    else:
                        currentGold = -betAmout
        print("对子次数", duizi, "顺子次数", shunzi, "同花次数", tonghua, "同花顺次数", tonghuashun, "豹子次数", baozi, '游戏次数', count)
        if currentGold < 0:
            sqTimes += 1
        else:
            jqTimes += 1
        initGold += currentGold
    # print('currentGold',currentGold)
    print('initGold',initGold)
    print("对子次数",duizi,"顺子次数",shunzi,"同花次数",tonghua,"同花顺次数",tonghuashun,"豹子次数",baozi,'游戏次数',count)
    print(initGold,sqTimes,jqTimes)
def settlementXianJia(xianjia,banker,roomMul):
    if xianjia['weight'] > banker['weight']:
        gold = xianjia['betScore'] * xianjia['mul'] * roomMul
    else:
        gold = -xianjia['betScore'] * banker['mul'] * roomMul
    gold = gold/(abs(gold)) * min([abs(gold),banker['frozenGold'],xianjia['frozenGold']])
    return gold
if __name__ == '__main__':
    parseRedBlack()
