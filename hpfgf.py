import requests, json,random,itertools,copy
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
CARDA = [[1, '方块', 'A', 13],
        [2, '梅花', 'A', 13],
        [3, '红桃', 'A', 13],
        [4, '黑桃', 'A', 13]]

def check_straight_flush(hand):
    """检测是不是同花顺"""
    if check_flush(hand) and check_straight(hand):
        return True
    else:
        return False
def get_three_of_a_kind(hand):
    frequencies = {}
    frequencies_list = []
    ranks = [i[3] for i in hand]
    for rank in ranks:
        if rank not in frequencies:
            frequencies[rank] = 1
        else:
            frequencies[rank] += 1
    for key,value in frequencies.items():
        if value ==3:
            return key
    return 1
def checkSHI_ER_HUANG_ZU(hand):
    if len([x for x in hand if x[3] >= 10]) == len(hand):
        return True
    return False
def check_all_big(hand):
    if len([x for x in hand if x[3] >= 7]) == len(hand):
        return True
    return False
def check_all_small(hand):
    if len([x for x in hand if x[3] <= 7]) == len(hand):
        return True
    return False
def check_one_type_color(hand):
    colors = list(set([x[0] for x in hand]))
    if sorted(colors) == [1,3] or sorted(colors) == [2,4]:
        return True
    return False
def check_three_straight_flush(hand):
    colorsType = list(set([x[0] for x in hand]))
    if len(colorsType) == 1 or len(colorsType) == 4:
        return False
    elif len(colorsType) == 2:#两种颜色
        color1 = []
        color2 = []
        for card in hand:
            if len(color1) == 0:
                color1.append(card)
            else:
                if card[0] == color1[0][0]:
                    color1.append(card)
                else:
                    color2.append(card)
        if len(color1) not in [3,10,8,5]:
            return False
        if len(color1) > len(color2):#color1 3张 color2 10张
            tem = color2
            color2 = color1
            color1 = tem
        if check_straight_flush(color1) and check_two_flushAndStraight(color2):
            return True
    elif len(colorsType) == 3:
        color1 = []
        color2 = []
        color3 = []
        for card in hand:
            if card[0] == colorsType[0]:
                color1.append(card)
            elif card[0] == colorsType[1]:
                color2.append(card)
            elif card[0] == colorsType[2]:
                color3.append(card)
        if check_straight_flush(color1) and check_straight_flush(color2) and check_straight_flush(color3) and sorted([len(color1),len(color2),len(color3)]) == [3,5,5]:
            return True
        return False
    return False
def check_two_flushAndStraight(hand):
    copyHand = copy.deepcopy(hand)
    for i in range(0,5):
        if i != 0:
            copyHand = exchangeA(copyHand)
        handsCards = sorted(copyHand,key=lambda x:x[-1])#按牌的大小排序
        hand1 = handsCards[0:5]
        hand2 = handsCards[5:]
        if check_straight_flush(hand1) and check_straight_flush(hand2) and (len(hand2) == 3 or len(hand2) == 5):
            return True
        hand1 = handsCards[0:3]
        hand2 = handsCards[3:]
        if check_straight_flush(hand1) and check_straight_flush(hand2) and len(hand2) == 5:
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
def check_san_shun_zi(hand):
    handsCards = copy.deepcopy(hand)
    for i in range(0,5):
        if i != 0:
            exchageHand = exchangeA(exchageHand)
        else:
            exchageHand = handsCards
        exchageHand = sorted(exchageHand,key=lambda x:x[-1])#按牌的大小排序
        hand1,hand2,hand3,hand4 = [],[],[],[]
        flag = 0
        for i in range(0,len(exchageHand)):
            if i == 0:

                hand1.append(exchageHand[i])
            else:
                if len(hand1) == 3:
                    flag = 1
                if exchageHand[i][-1] - hand1[-1][-1] == 1 and flag == 0:
                    hand1.append(exchageHand[i])
                elif exchageHand[i][-1] - hand1[-1][-1] == 0 or exchageHand[i][-1] - hand1[-1][-1] > 1 or flag == 1:
                    hand2.append(exchageHand[i])
        flag = 0
        for i in range(0,len(hand2)):
            if i == 0:
                hand3.append(hand2[i])
            else:
                if len(hand3) == 5:
                    flag = 1
                if hand2[i][-1] - hand3[-1][-1] == 1 and flag == 0:
                    hand3.append(hand2[i])
                elif hand2[i][-1] - hand3[-1][-1] == 0 or hand2[i][-1] - hand3[-1][-1] > 1 or flag == 1:
                    hand4.append(hand2[i])
        if check_straight(hand1) and check_straight(hand3) and check_straight(hand4) and sorted([len(hand1),len(hand3),len(hand4)]) == [3,5,5]:
            return True
        hand1, hand2, hand3, hand4 = [], [], [], []
        flag = 0
        for i in range(0, len(exchageHand)):
            if i == 0:
                hand1.append(exchageHand[i])
            else:
                if len(hand1) == 5:
                    flag = 1
                if exchageHand[i][-1] - hand1[-1][-1] == 1 and flag == 0:
                    hand1.append(exchageHand[i])
                elif exchageHand[i][-1] - hand1[-1][-1] == 0 or exchageHand[i][-1] - hand1[-1][-1] > 1 or flag == 1:
                    hand2.append(exchageHand[i])
        flag = 0#前5
        for i in range(0, len(hand2)):
            if i == 0:
                hand3.append(hand2[i])
            else:
                if len(hand3) == 5:
                    flag = 1
                if hand2[i][-1] - hand3[-1][-1] == 1 and flag == 0:
                    hand3.append(hand2[i])
                elif hand2[i][-1] - hand3[-1][-1] == 0 or hand2[i][-1] - hand3[-1][-1] > 1 or flag == 1:
                    hand4.append(hand2[i])
        if check_straight(hand1) and check_straight(hand3) and check_straight(hand4) and sorted([len(hand1),len(hand3),len(hand4)]) == [3,5,5]:
            return True
        hand3,hand4 = [],[]
        flag = 0  # 前3
        for i in range(0, len(hand2)):
            if i == 0:
                hand3.append(hand2[i])
            else:
                if len(hand3) == 3:
                    flag = 1
                if hand2[i][-1] - hand3[-1][-1] == 1 and flag == 0:
                    hand3.append(hand2[i])
                elif hand2[i][-1] - hand3[-1][-1] == 0 or hand2[i][-1] - hand3[-1][-1] > 1 or flag == 1:
                    hand4.append(hand2[i])
        if check_straight(hand1) and check_straight(hand3) and check_straight(hand4) and sorted(
                [len(hand1), len(hand3), len(hand4)]) == [3, 5, 5]:
            return True
    return False
def checkFlush(list):
    list1 = []
    for i in list:
        if i[0] not in list1 :
            list1.append(i[0])
    if len(list1)==1:
        return True
    return False
def check_flush(list):
    list1 = []
    for i in list:
        if i[0] not in list1 :
            list1.append(i[0])
    if len(list1) == 1:
        return True
    return False
def check_san_tong_hua(hand):
    frequencies = {}
    frequencies_list = []
    ranks = [i[0] for i in hand]
    for rank in ranks:
        if rank not in frequencies:
            frequencies[rank] = 1
        else:
            frequencies[rank] += 1
    for value in frequencies.values():
        frequencies_list.append(value)
    frequencies_list.sort()
    if frequencies_list == [3,5,5] or frequencies_list == [13] or frequencies_list == [3,10] or frequencies_list == [5,8] or frequencies_list == [1]:
        return True
    return False
def check_straight(hand):
    preNum = 0
    handsCards = copy.deepcopy(hand)
    handsCards = [[4, '黑桃', 'A', 0] if i in CARDA else i for i in handsCards]
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
def check_special_type(hand):
    cardsNo = [x[2] for x in hand]
    colorList = [x[0] for x in hand]
    if sorted(cardsNo) == ['2','3','5'] and len(set(colorList)) >= 2:
        return True
    return False
def check_four_of_a_kind(hand):
    """检测是不是四张相同"""
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

    # 判断list中是否有值为4
    if frequencies_list[1] == 4:
        return True
    else:
        return False
def check_three_four_of_a_kind(hand):
    """检测是不是四张相同"""
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

    # 判断list中是否有值为4
    if frequencies_list[0] == 1 and frequencies_list[1] == 4 and frequencies_list[2] == 4 and frequencies_list[3] == 4:
        return True
    else:
        return False
def check_four_three_of_a_kind(hand):
    """检测是不是四张相同"""
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

    # 判断list中是否有值为4
    if frequencies_list == [1,3,3,3,3] or frequencies_list == [3,3,3,4]:
        return True
    else:
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
def check_wu_dui_san_tiao(hand):
    """ 检测是不是4ge对子"""
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

    if frequencies_list == [2,2,2,2,2,3] or frequencies_list == [2,2,2,3,4] or frequencies_list == [2,3,4,4]:
        return True
    else:
        return False
def check_liu_dui_ban(hand):
    """ 检测是不是6ge对子"""
    frequencies = {}
    frequencies_list = []
    ranks = [i[2] for i in hand]
    for rank in ranks:
        if rank not in frequencies:
            frequencies[rank] = 1
        else:
            frequencies[rank] += 1

    for frequency in frequencies.values():
        if frequency == 4:
            frequencies_list.append(2)
            frequencies_list.append(2)
        else:
            frequencies_list.append(int(frequency))
    frequencies_list.sort()

    if frequencies_list[0] == 1 and frequencies_list[1] == 2 and frequencies_list[2] == 2 and frequencies_list[3] == 2 and frequencies_list[4] == 2 and frequencies_list[5] == 2 and frequencies_list[6] == 2:
        return True
    else:
        return False
def check_three_of_a_kind(hand):
    """检测是不是三张相同"""
    ranks = [i[2] for i in hand]
    if len(set(ranks)) == 1:
        return True
    return False
def check_two_pairs(hand):
    """检测是不是两个对子"""
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

    if frequencies_list[1] == 2:
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
    if frequencies_list[0] == 1:
        if frequencies_list[1] == 2:
            return True
    return False
def normaljudge(hand):
    if check_three_of_a_kind(hand):
        return 6
    elif check_straight_flush(hand):
        return 5
    elif check_flush(hand):
        return 4
    elif check_straight(hand):
        return 3
    elif check_one_pairs(hand):
        return 2
    elif check_special_type(hand):
        return 0
    else:
        return 1
def checkThreeCards_three_of_a_kind(hand):
    if len(list(set([x[2] for x in hand]))) == 1:
        return True
    return False
def checkThreeCards_one_of_pairs(hand):
    if len(list(set([x[2] for x in hand]))) == 2:
        return True
    return False
def threeCardsJudge(hand):
    if checkThreeCards_three_of_a_kind(hand):
        return 3
    elif checkThreeCards_one_of_pairs(hand):
        return 1
    else:
        return 0
def specialCardsJudge(hand):
    if check_straight_flush(hand):
        return 21
    elif check_straight(hand):
        return 20
    elif checkSHI_ER_HUANG_ZU(hand):
        return 19
    elif check_three_straight_flush(hand):
        return 18
    elif check_three_four_of_a_kind(hand):
        return 17
    elif check_all_big(hand):
        return 16
    elif check_all_small(hand):
        return 15
    elif check_one_type_color(hand):
        return 14
    elif check_four_three_of_a_kind(hand):
        return 13
    elif check_wu_dui_san_tiao(hand):
        return 12
    elif check_liu_dui_ban(hand):
        return 11
    elif check_san_tong_hua(hand):
        return 10
    elif check_san_shun_zi(hand):
        return 9
    else:
        return -1
def checkDs(cards,types):
    if types[1] > types[0] and types[2] > types[1]:
        return True
    elif types[1] == types[0]:
        if sameTypeCompare(cards[0],cards[1],types[0]) <= 0:
            return True
    elif types[1] == types[2]:
        if sameTypeCompare(cards[1],cards[2],types[1]) <= 0:
            return True
    return False
def getCardType(cards):
    if len(cards) == 13:#特殊牌型
        type = specialCardsJudge(cards)
        return [type]
    else:#普通牌型
        headPiers = cards[0]
        midllePiers = cards[1]
        gourdPiers = cards[2]
        specialCardsJudgeCards = headPiers + midllePiers + gourdPiers
        type = specialCardsJudge(specialCardsJudgeCards)
        if type != -1:
            # exit(-5)
            return [type]
        else:
            type1 = threeCardsJudge(headPiers)
            type2 = normaljudge(midllePiers)
            type3 = normaljudge(gourdPiers)
        return [type1,type2,type3]
def getRepeatCardsMax(cards,num,cardType = 0):
    frequencies = {}
    frequencies_list = []
    temList = []
    ranks = [i[3] for i in cards]
    for rank in ranks:
        if rank not in frequencies:
            frequencies[rank] = 1
        else:
            frequencies[rank] += 1
    for key,frequency in frequencies.items():
        if frequency == num:
            for i in range(0,frequency):
                frequencies_list.append(key)
        elif frequency % num == 0 and num == 2:
            for i in range(0,frequency):
                frequencies_list.append(key)
        elif frequency == 4 and num == 3 and cardType == 13:
            for i in range(0, frequency):
                frequencies_list.append(key)
        else:
            for i in range(0, frequency):
                temList.append(key)
    if cardType in (12,13,17):
        maxCard = max(frequencies_list)
        frequencies_list = []
        frequencies_list.append(maxCard)
        temList = []
    frequencies_list.sort(reverse=True)
    temList.sort(reverse=True)
    frequencies_list += temList
    return frequencies_list
def pointsCompare(cards1,cards2):
    if isinstance(cards1[0],list):
        cards1 = [x[-1] for x in cards1]
        cards2 = [x[-1] for x in cards2]
        cards1.sort(reverse=True)
        cards2.sort(reverse=True)
    for i in range(0,len(cards1)):
        if cards1[i] > cards2[i]:
            return 1
        elif cards1[i] < cards2[i]:
            return -1
    return 0
def sameTypeCompare(cards1,cards2,type):
    cards1 = sorted(cards1,key=lambda x:x[-1],reverse=True)
    cards2 = sorted(cards2, key=lambda x: x[-1], reverse=True)
    if type in [12,13,17,11,7,5,6,3,1,2]:
        if type in [7] :
            repeatCards1 = getRepeatCardsMax(cards1,4)
            repeatCards2 = getRepeatCardsMax(cards2,4)
        elif type in [5,6,3]:
            repeatCards1 = getRepeatCardsMax(cards1, 3)
            repeatCards2 = getRepeatCardsMax(cards2, 3)
        elif type == 13:
            repeatCards1 = getRepeatCardsMax(cards1, 3,13)
            repeatCards2 = getRepeatCardsMax(cards2, 3,13)
        elif type == 12:
            repeatCards1 = getRepeatCardsMax(cards1, 3,12)
            repeatCards2 = getRepeatCardsMax(cards2, 3,12)
        elif type == 17:
            repeatCards1 = getRepeatCardsMax(cards1, 4,17)
            repeatCards2 = getRepeatCardsMax(cards2, 4,17)
        elif type in [1,2,11] :
            repeatCards1 = getRepeatCardsMax(cards1, 2)
            repeatCards2 = getRepeatCardsMax(cards2, 2)
        return pointsCompare(repeatCards1,repeatCards2)
    return pointsCompare(cards1,cards2)
def countMul(cards1,cards2,type1,type2):
    mul=[]
    if len(type1) == 1 :
        if len(type2) == 1:
            if type1[0] > type2[0]:
                mul = [0,0,0]
            elif type1[0] < type2[0]:
                mul = [0,0,0]
            else:
                if sameTypeCompare(cards1,cards2,type1[0]) == 1:
                    mul = [0,0,0]
                elif sameTypeCompare(cards1,cards2,type1[0]) == -1:
                    mul = [0,0,0]
                else:
                    mul = [0,0,0]
        else:
            mul = [0,0,0]
    else:
        mul=[]
        if len(type2) == 1:
            mul=[0,0,0]
        else:
            for i in range(0,3):
                if type1[i] > type2[i]:
                    mul.append(NORMALAWARDODDS[(type1[i],i)])
                elif type1[i] == type2[i]:
                    mul.append(sameTypeCompare(cards1[i],cards2[i],type1[i]) * NORMALAWARDODDS[(type1[i],i)])
                else:
                    mul.append(-NORMALAWARDODDS[(type2[i],i)])
    return mul
def countSpMul(cards1,cards2,type1,type2):
    if len(type1) == 1:
        type1 = type1[0]
    if len(type2) == 1:
        type2 = type2[0]
    else:
        type2 = 1
    if type1 == type2:
        if type1 >= 19:
            mul = 0
        else:
            mul = AWARDODDS[type1] * sameTypeCompare(cards1,cards2,type1)
    elif type1 > type2:
        mul = AWARDODDS[type1]
    else:
        mul = -AWARDODDS[type2]
    return mul
def toStrCards(card):
    if len(str(card)) == 1:
        return '0' + str(card)
    return str(card)
def mySorted(hand):
    sortedHand = sorted(hand,key=lambda x:pokerList.index(x))
    color = sortedHand[-1][0]
    bombPoint = [x[3] for x in hand]
    bombPoint = sorted(bombPoint, reverse=True)
    if bombPoint == [13,2,1]:
        return '020100' + str(color)
    bombPoint = list(map(toStrCards,bombPoint))
    weight = ''.join(bombPoint)
    return weight + str(color)
def mySortedPairs(hand):
    sortedHand = sorted(hand, key=lambda x: pokerList.index(x))
    if sortedHand[0][-1] == sortedHand[1][-1]:
        color = sortedHand[1][0]
    else:
        color = sortedHand[2][0]
    bombPoint = [x[3] for x in hand]
    bombPoint = sorted(bombPoint)
    if bombPoint[0] == bombPoint[1]:
        pass
    else:
        bombPoint.reverse()
    bombPoint = list(map(toStrCards,bombPoint))
    weight = ''.join(bombPoint)
    return weight + str(color)
def getWeight(hand):
    cardsType = normaljudge(hand)
    if cardsType == 6:
        baozi = mySorted(hand)
    else:
        baozi = "0000000"
    if cardsType == 5:
        tongHuaShun = mySorted(hand)
    else:
        tongHuaShun = "0000000"
    if cardsType == 4:
        jinHua = mySorted(hand)
    else:
        jinHua = "0000000"
    if cardsType == 3:
        shunZi = mySorted(hand)
    else:
        shunZi = "0000000"
    if cardsType == 2:
        duiZi = mySortedPairs(hand)
    else:
        duiZi = "0000000"
    if cardsType == 1 or cardsType == 0:
        gaoPai = mySorted(hand)
    else:
        gaoPai = "0000000"
    weight = int(baozi + tongHuaShun + jinHua + shunZi + duiZi + gaoPai)
    # print(hand,weight,'baozi',baozi,'tongHuaShun',tongHuaShun,'jinHua',jinHua,'shunZi',shunZi,'duiZi',duiZi,'gaoPai',gaoPai)
    return weight
def soloCompare(myCards,enemyCards):
    # if sorted([x[-1] for x in myCards]) == sorted([x[-1] for x in enemyCards]) and normaljudge(myCards) == 2:
    #     pass
    if normaljudge(myCards) == 6 and normaljudge(enemyCards) == 0:
        return False
    elif normaljudge(myCards) == 0 and normaljudge(enemyCards) == 6:
        return True
    else:
        if getWeight(myCards) > getWeight(enemyCards):
            return True
    return False
def get_changed_cards(cards):
    cards = cards.split(',')
    cards = list(map(int, cards))
    realCards = [pokerList[x] for x in cards]
    return realCards
def parseThirtyWater():
    errorRounds = [533880360443527680,536453922048131584,536543844046160384]
    gameType = 45
    userName = 'ada'
    pwd = 'ada'
    startTime = "2022-04-11 00:00:00"
    endTime = "2022-04-18 23:52:28"
    record = Record(userName,pwd,gameType,startTime,endTime)
    roomRecords = record.organizeRecords()
    for roomid, roomsetleRecords in roomRecords.items():  # 遍历每个房间
        roomsetleRecords.sort(key=lambda x:x['roomInfo']['endTime'])
        for records in roomsetleRecords:  # 遍历每一局
            print(records)
            userFrozenGold = {}#存放玩家操作 key:seatNo座位号 ，value：（type操作类型,gold投注筹码）
            enterRoonFrozen = {}#存放进入房间时冻结筹码
            settlements = records['settlements']
            userList = records['userlist']
            if len(userList) > 5 or len(userList) < 2:
                print('匹配人数异常')
                exit(-7)
            for i in userList:
                seatNo = i['seatNo']
                frozenGold = i['frozenGold']
                enterRoonFrozen[seatNo] = frozenGold#存放进入房间时冻结筹码
            playersList = []
            roomInfo = records['roomInfo']
            roundId = roomInfo['roundId']
            if roundId in errorRounds:#过滤掉异常局号
                continue
            antes = roomInfo['roomScore']
            for user in userList:#存放玩家列表
                seatNo = user['seatNo']
                playersList.append(seatNo)
            playerOperators = records['playerOperator']#玩家操作记录
            allin_stage = -1#孤注一掷标识
            shouldBet = antes#初始跟注值等于底注
            showRecourd = {}#存放看牌玩家座位号list
            byGzyz = []#存放被孤注一掷比输的玩家,即要退费的玩家
            for playerOperator in playerOperators:
                seatNo = playerOperator['seatNo']
                stage = playerOperator['raiseCount']
                type = playerOperator['type']
                betGold = playerOperator['betGold']
                isShow = playerOperator['isShow']
                compWin = playerOperator['compWin']
                destSeatNo = playerOperator['destSeatNo']
                userBet = userFrozenGold.get(seatNo, [])
                lastBet = antes
                if seatNo not in showRecourd.keys():
                    showRecourd[seatNo] = isShow
                elif isShow:
                    showRecourd[seatNo] = isShow
                if len(userBet) != 0:
                    for sinUserBet in userBet:
                        sinStage = sinUserBet[0]
                        sinbetGold = sinUserBet[1]
                        if sinStage == stage - 1:
                            lastBet = sinbetGold#倒数第二轮下注
                if type == 1:#加注
                    if showRecourd[seatNo]:
                        shouldBet = round((betGold - lastBet) / 2)#应该跟注值
                    else:
                        shouldBet = betGold - lastBet
                if type == 3 and betGold == enterRoonFrozen[seatNo]:
                    if compWin:
                        byGzyz.append(destSeatNo)
                    else:
                        byGzyz = []
                    allin_stage = stage
                    if showRecourd[seatNo]:
                        byPercent = (betGold - lastBet) / (shouldBet * 2)
                    else:
                        byPercent = (betGold - lastBet) / shouldBet
                if type != 5:#非看牌操作
                    userBet.append((stage, betGold))
                    userFrozenGold.update({seatNo: userBet})
            userCards = {}
            for settlement in settlements:
                seatNo = settlement['seatNo']
                cards = settlement['card']
                realCards = get_changed_cards(cards)
                userCards[seatNo] = realCards
            for playerOperator in playerOperators:
                seatNo =  playerOperator['seatNo']
                type = playerOperator['type']
                destSeatNo = playerOperator['destSeatNo']
                compWin = playerOperator['compWin']
                stage = playerOperator['raiseCount']
                betGold = playerOperator['betGold']

                if type == 4:
                    print("最终结算移除座位号",seatNo)
                    playersList.remove(seatNo)
                if destSeatNo != 0:#发生比牌操作
                    myCards = userCards[seatNo]
                    enemyCards = userCards[destSeatNo]
                    if soloCompare(myCards,enemyCards) != compWin:
                        print("比牌异常",seatNo,'比牌',destSeatNo)
                        exit(-7)
                    if compWin:
                        playersList.remove(destSeatNo)
                    else:
                        playersList.remove(seatNo)
            compareCards = []

            for settlement in settlements:
                seatNo = settlement['seatNo']
                uid = settlement['uid']
                cards = settlement['card']
                cardTypes = settlement['type']
                gold = settlement['gold']
                if allin_stage != -1:
                    aSeatNo = seatNo

                    operators = userFrozenGold[aSeatNo]
                    lastOperator = operators[-1]
                    stage,bet = lastOperator[0],lastOperator[1]
                    if gold < 0 and stage == allin_stage:
                        if len(operators) > 1:
                            nextLastOperator = operators[-2]
                            nextLastBet = nextLastOperator[-1]
                        else:
                            nextLastBet = antes
                        if seatNo in byGzyz:
                            realBet = preciseRound(bet - (bet - nextLastBet) * (1 - byPercent))
                            userFrozenGold[aSeatNo][-1] = (stage,realBet)
                            print("投注修正",aSeatNo,realBet,"原筹码",bet,'投注百分比',byPercent,"上次投注",nextLastBet)
            print(userFrozenGold)
            for settlement in settlements:
                seatNo = settlement['seatNo']
                uid = settlement['uid']
                cards = settlement['card']
                cardTypes = settlement['type']
                gold = settlement['gold']
                if gold < 0 and abs(-gold - (round(userFrozenGold.get(seatNo)[-1][-1]))) > 1:
                    print(seatNo,'gold',gold,'myGold',-round(userFrozenGold.get(seatNo)[-1][-1]))
                    exit(-3)
                if gold > 0:
                    losersGold = 0
                    for user_seatNo,frozenGold in userFrozenGold.items():
                        if user_seatNo != seatNo:
                            # print('user_seatNo',user_seatNo,'frozenGold[-1][-1]',frozenGold[-1][-1])
                            losersGold += frozenGold[-1][-1]
                    losersGold = round(losersGold * 0.95)
                    if abs(gold - losersGold) > 5:
                        print('seatNo',seatNo,'gold',gold,'losersGold',losersGold)
                        exit(-2)
                cards = cards.split(',')
                cards = list(map(int,cards))
                realCards = [pokerList[x] for x in cards]
                myCardsType = normaljudge(realCards)
                if myCardsType != int(cardTypes):
                    exit(-1)
                for playerSeatNo in playersList:
                    if playerSeatNo == seatNo:
                        compareCards.append(realCards)
            sortedCompareCards = sorted(compareCards,key=lambda x:getWeight(x))
            for settlement in settlements:
                cards = settlement['card']
                cards = cards.split(',')
                cards = list(map(int, cards))
                realCards = [pokerList[x] for x in cards]
                gold = settlement['gold']
                if realCards == sortedCompareCards[-1] and gold < 0:
                    print('真实牌输了',realCards,'理论最大牌',sortedCompareCards[-1])
                    exit(-2)
                if realCards != sortedCompareCards[-1] and gold > 0:
                    print('真实牌赢了', realCards, '理论最大牌', sortedCompareCards[-1])
                    exit(-2)
if __name__ == '__main__':
    parseThirtyWater()

