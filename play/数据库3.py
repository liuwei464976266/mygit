
from logAnalysisUtil import *


def getSlotGameData(gameType,startTime,endTime):
    black_List = getBlackUserList()#黑名单
    mangoData = timeQueryMangodbByGameType(startTime,endTime,black_List, gameType=gameType)#mangodb数据 类似items
    print(111,mangoData)
    totalGameCount = 0#总游戏次数
    totalBetAmount = 0#总下注
    totalAwardGold = 0#总获取奖项
    totalGold = 0#总输赢
    normalSpin = 0#普通场次数
    normalSpinAward = 0#普通场次中奖额
    fsWinTimes = 0#红利场次数
    prize0,prize1,prize2,prize3,prize4,prize5,prize6,prize7,prize8,prize9 = [0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]#=0，1-29,30-49,50-99,100-199,200-299,300-399,400-499,500-999,1000+
    for colData in mangoData:
        print(colData)
        for k,v in colData.items():
            if k == 'gold':
                gold = v
                betAmount = colData['betAmount']
                totalGameCount += 1
                totalBetAmount += betAmount
                awardGold = gold + betAmount
                totalAwardGold += awardGold
                totalGold += gold
                totalWinRate = totalGold/totalBetAmount
                if betAmount != 0:
                    normalSpin += 1
                    normalSpinAward += awardGold
                    winRate = awardGold/betAmount
                    if winRate == 0:
                        prize0[0] += 1
                        prize0[1] += awardGold
                        prize0[2] = prize0[0]/totalGameCount
                    elif 0 < winRate <= 5:
                        prize1[0] += 1
                        prize1[1] += awardGold
                        prize1[2] = prize1[0] / totalGameCount
                    elif 5 < winRate <= 10:
                        prize2[0] += 1
                        prize2[1] += awardGold
                        prize2[2] = prize2[0] / totalGameCount
                    elif 10 < winRate <= 20:
                        prize3[0] += 1
                        prize3[1] += awardGold
                        prize3[2] = prize2[0] / totalGameCount
                    elif 20 < winRate <= 40:
                        prize4[0] += 1
                        prize4[1] += awardGold
                        prize4[2] = prize2[0] / totalGameCount
                    elif 40 < winRate <= 60:
                        prize5[0] += 1
                        prize5[1] += awardGold
                        prize5[2] = prize2[0] / totalGameCount
                    elif 60 < winRate <= 100:
                        prize6[0] += 1
                        prize6[1] += awardGold
                        prize6[2] = prize2[0] / totalGameCount
                    elif 100 < winRate <= 200:
                        prize7[0] += 1
                        prize7[1] += awardGold
                        prize7[2] = prize2[0] / totalGameCount
                    elif 200 < winRate <= 400:
                        prize8[0] += 1
                        prize8[1] += awardGold
                        prize8[2] = prize2[0] / totalGameCount
                    elif 400 < winRate:
                        prize9[0] += 1
                        prize9[1] += awardGold
                        prize9[2] = prize2[0] / totalGameCount
                elif gold + betAmount > 0:
                    fsWinTimes += 1
    fsTimes = totalGameCount - normalSpin
    fsAward = totalAwardGold - normalSpinAward
    prize = (prize0,prize1,prize2,prize3,prize4,prize5,prize6,prize7,prize8,prize9)
    with open("spinGamesWinRate.csv","a", encoding='UTF-8') as f:
        en_gameType = get_game_ENname(gameType)[0][0]
        print(en_gameType)
        f.write('\n')
        f.write(en_gameType + '\n')
        f.write(startTime.replace("'","") + "-" + endTime.replace("'","") + '\n')
        titleList = ['游戏场次','总底注量','总获取奖项数额','总输赢金币','输赢投注比']
        mywritelines(f,titleList)
        print(totalGameCount,totalBetAmount,totalAwardGold,totalGold)
        print(totalWinRate)
        row4 = [totalGameCount,totalBetAmount,totalAwardGold,totalGold, totalWinRate]
        mywritelines(f, row4)
        titleList2 = ['普通场开奖倍数','出现场次','开奖额','总场次占比','玩家赢数据占比']
        mywritelines(f, titleList2)
        awardAreamList = ['400+','200~400','100~200','60~100','40~60','20~40','10~20','5~10','0~5','为0']
        awardAreamList.reverse()
        for i in range(10):
            f.write(awardAreamList[i] + ',')
            mywritelines(f,prize[i])
        row5 = ['合计开奖',normalSpin,normalSpinAward]
        mywritelines(f, row5)
        row6 = ['红利次数/奖项',fsTimes ,fsAward]
        mywritelines(f, row6)
        row7 = ['红利赢场次', fsWinTimes]
        mywritelines(f, row7)


def mywritelines(f, mylist):
    mylist = list(map(str,mylist))
    for title in mylist:
        f.write(title + ',')
    f.write('\n')


if __name__ == '__main__':
    gameType = [130, 131, 132, 133, 134, 135, 136]
    startTime = "2021-12-15 18:00:00"
    endTime = "2021-12-16 08:59:59"
    for i in gameType:
        getSlotGameData(i, startTime,endTime)


