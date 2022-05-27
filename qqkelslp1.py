from logAnalysisUtil import *
import json, random
from enum import Enum, unique

goldPoint = {'4':60,'5':30,'6':17,'7':12,'8':8,'9':7,'10':6,'11':6,'12':7,'13':8,'14':12,'15':17,'16':30,'17':60,'19':2,'20':2,'21':2,'22':2,'18':30}

def getHs(point):
    pokerList = ['a', 'b', 'c', 'd', 'e', 'f']
    bigsmall = [[5,7,9,11,13,15,17],[4,6,8,10,12,14,16]]
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
                    c += str(a) + ','
                award3 = c[:-1]
                award2.sort()
                result = sum(award2)
                if 3 < result < 11:
                    result1 = 0
                elif 10 < result < 18:
                    result1 = 1
                else:
                    result1 = 2
                if result in bigsmall[0]:
                    result2 = 0
                elif result in bigsmall[1]:
                    result2 = 1
                else:
                    result2 =2
                if award2[0] == award2[1] and award2[1] == award2[2]:
                    result3 = 1
                    result = 0
                else:
                    result3 = 0
                # print(award,award2,award3)
                '''点数，大1小0，单0双1，豹子1result,result1,result2,result3'''
                awarlist = [result, result1, result2, result3]
                return awarlist

    if len(award) < 3:
        num = []
        for i in point[::-1]:
            if i in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9') and len(num) < 18:
                num.append(int(i))
        return


def random_hex(length):
    result = hex(random.randint(0, 16**length)).replace('0x','').upper()
    if(len(result)<length):
            result ='0'*(length-len(result))+result
    return result


def main():
    gold = 0
    for x, y in goldPoint.items():
        numdoc = {}
        initGold = 10000
        awardCount = 0
        for i in range(initGold):
            hashChain = str(random_hex(64)).lower()
            award = getHs(hashChain)
            # print(award)
            if int(x) < 18 and int(x) == award[0]:
                awardCount += 1
            elif int(x) == 19 and award[1] == 0:
                awardCount += 1
            elif int(x) == 20 and award[1] == 1:
                awardCount += 1
            elif int(x) == 21 and award[2] == 0:
                awardCount += 1
            elif int(x) == 22 and award[2] == 1:
                awardCount += 1
            elif int(x) == 18 and award[3] == 1:
                awardCount += 1
        numdoc[x] = awardCount
        gold1 = numdoc[x]*goldPoint[x]-initGold
        gold += numdoc[x]*goldPoint[x]-initGold
        print(numdoc, gold1)
    print(gold)







if __name__ == '__main__':
    main()