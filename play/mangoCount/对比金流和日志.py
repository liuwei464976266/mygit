#encoding:utf-8
import datetime
from logAnalysisUtil import *
def main():
    startTime = "2021-10-19 00:00:00"
    endTime = "2021-10-19 23:59:59"
    styleTuple = ('1', '7')
    actionType = (2, 12)
    logRoundId = []
    black_List = getBlackUserList()
    record = {}
    mydoc = timeQueryMangodbLog(startTime,endTime)
    for x in mydoc:
        gold_type = x[0]
        if gold_type == 2:
            roundId = str(x[1]['orderId'])
        else:
            roundId = str(x[1]['roomInfo']['roundId'])
        logRoundId.append(roundId)
    roundIdList = getGoldActionRecord(startTime,endTime,actionType,styleTuple)
    errorRound = [x for x in logRoundId if x not in roundIdList] + [x for x in roundIdList if x not in logRoundId]
    for i in logRoundId:
        if logRoundId.count(i) > 1:
            print('重复记录局号',i)
    print('roundIdList长度',len(set(roundIdList)),'logRoundId长度',len(logRoundId),'logRoundId去重长度',len(set(logRoundId)))
    print('无法对应局数',len(errorRound),'局号如下:')
    if len(errorRound) > 0:
        for i in errorRound:
            print(i)


if __name__ == '__main__':
    main()
