# encoding:utf-8
from logAnalysisUtil import *


def main(game, startime, endtime):
    oo = Record('Y002', '111', game, startime, endtime)
    b = oo.organizeRecords()
    a = oo.getRcords()
    game = oo.gameReport()
    print(game)
    key = b.keys()
    li = []
    for i in key:
        for x in b[i]:
            li.append(x['roomInfo']['roundId'])
            # print(x)
    print(len(li), len(set(li)))
    cc = [x for x in li if li.count(x) != 1]
    print(cc)


startime = '2021-11-25 00:00:00'
endtime = '2021-11-25 23:59:59'
GAMETYPELIST = {"41": "德州扑克", "202": "俄罗斯轮盘", "31": "推筒子"}

# main(31, startime, endtime)
for x, y in GAMETYPELIST.items():
    print(y, '记录重复局')
    main(x, startime, endtime)
