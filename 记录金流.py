# coding:utf-8
from logAnalysisUtil import *
import json
from bson import ObjectId


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


GAMETYPELIST = {"43": "新版斗牛",
                "202": "俄罗斯轮盘",
                "41": "德州扑克",
                "31": "推筒子",
                "33": "牌九",
                "34": "百人牛牛",
                "47": "红黑大战",
                "58": "百人骰宝",
                "200": "鱼虾蟹",
                "201": "猜丁壳",
                "39": "十三水",
                "32": "三公",
                "38": "二十一点",
                }


def queryMangodb(startTime, endTime, game=0):
    myclient = pymongo.MongoClient('mongodb://admin:admin@192.168.10.25:27017/OverseasGame?authSource=admin')
    mydb = myclient['OverseasGame']
    startTimeArray = time.strptime(startTime, "%Y-%m-%d %H:%M:%S")
    monthFirstTime = datetime.datetime(year=startTimeArray.tm_year, month=startTimeArray.tm_mon, day=1, hour=0,
                                       minute=0,
                                       second=0)
    monthFirstTime = datetime.datetime.strftime(monthFirstTime, "%Y-%m-%d %H:%M:%S")
    monthDate = startTime[0:7]
    mycol = mydb["GameUserCount_" + monthDate]
    slot_mycol = mydb["LotteryRecordModel"]  # 小游戏
    myquery = {"endTime": {"$gt": parse(startTime), '$lt': parse(endTime)}}
    slot_myquery = {"createDate": {"$gt": parse(startTime), '$lt': parse(endTime)}}
    if game == 0:
        mydoc = mycol.find(myquery)
        return mydoc
    else:
        mydoc = slot_mycol.find(slot_myquery)
        return mydoc


def Mangodb(STARTTIME):   #验证新版斗牛抢庄
    timeArray = time.strptime(STARTTIME, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray)) * 1000
    print(timeStamp)
    myclient = pymongo.MongoClient('mongodb://admin:admin@192.168.10.25:27017/OverseasGame?authSource=admin')
    mydb = myclient['OverseasGame']
    mycol = mydb["XBDNLog"]
    my = {"roomInfo.startTime": {"$gt": timeStamp}}
    mydoc = mycol.find(my)
    x= 0
    for i in mydoc:
        x+=1
        # i = JSONEncoder().encode(i)
        print(x,JSONEncoder().encode(i))
        settlements = i['settlements']
        playerOperator = i['playerOperator']
        Banker = []
        for i in settlements:
            if i.get('isBanker'):
                seatNo = i['seatNo']
        for i in playerOperator[:5]:
            if i['seatNo'] == seatNo:
                betGold = i['betGold']
            if i['betGold'] != 0:
                Banker.append(i['betGold'])
        if len(Banker) > 0:
            if betGold != max(Banker):
                print('错误了')
                return


def timeQueryMangodb(_startTime, _endTime):
    _startTime = datetime.datetime.strptime(_startTime, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=-8)
    _startTime = datetime.datetime.strftime(_startTime, "%Y-%m-%d %H:%M:%S")
    _endTime = datetime.datetime.strptime(_endTime, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=-8)
    _endTime = datetime.datetime.strftime(_endTime, "%Y-%m-%d %H:%M:%S")
    startTimeArray = time.strptime(_startTime, "%Y-%m-%d %H:%M:%S")
    endTimeArray = time.strptime(_endTime, "%Y-%m-%d %H:%M:%S")
    months = endTimeArray.tm_mon - startTimeArray.tm_mon
    docList = []
    if months == 0:
        startTime = _startTime
        endTime = _endTime
        doc = queryMangodb(startTime, endTime)
        for x in doc:
            docList.append(x)

    else:
        mon = startTimeArray.tm_mon
        for i in range(0, months + 1):
            if mon == startTimeArray.tm_mon:
                firstDayWeekDay, monthRange = calendar.monthrange(startTimeArray.tm_year, mon)
                monthLastTime = datetime.datetime(year=startTimeArray.tm_year, month=mon, day=monthRange, hour=23,
                                                  minute=59, second=59)
                startTime = _startTime
                endTime = datetime.datetime.strftime(monthLastTime, "%Y-%m-%d %H:%M:%S")
                doc = queryMangodb(startTime, endTime)
                for x in doc:
                    docList.append(x)
            elif mon == endTimeArray.tm_mon:
                monthFirstTime = datetime.datetime(year=endTimeArray.tm_year, month=mon, day=1, hour=0, minute=0,
                                                   second=0)
                startTime = datetime.datetime.strftime(monthFirstTime, "%Y-%m-%d %H:%M:%S")
                endTime = _endTime
                doc = queryMangodb(startTime, endTime)
                for x in doc:
                    docList.append(x)
            else:
                firstDayWeekDay, monthRange = calendar.monthrange(startTimeArray.tm_year, mon)
                monthFirstTime = datetime.datetime(year=endTimeArray.tm_year, month=mon, day=1, hour=0, minute=0,
                                                   second=0)
                monthLastTime = datetime.datetime(year=startTimeArray.tm_year, month=mon, day=monthRange, hour=23,
                                                  minute=59, second=59)
                startTime = datetime.datetime.strftime(monthFirstTime, "%Y-%m-%d %H:%M:%S")
                endTime = datetime.datetime.strftime(monthLastTime, "%Y-%m-%d %H:%M:%S")
                doc = queryMangodb(startTime, endTime)
                for x in doc:
                    docList.append(x)
            mon += 1
    return docList


def Gold_list(startTime, endTime, type):
    ms = MSSQL(host='192.168.10.199', user='test', pwd='123456', db="OverseasGame", port=1433)
    ms.GetConnect()
    sql = f"SELECT * FROM [dbo].[Game_GoldActionInfo] WHERE GameType = '{type}' AND CreatDate >'{startTime}' AND CreatDate <'{endTime}'"
    sql1 = f"SELECT SUM(goldNum),currencyType FROM [dbo].[Game_GoldActionInfo] WHERE GameType = '{type}' AND CreatDate > '{startTime}' AND CreatDate < '{endTime}' AND (actionType=2 OR actionType=12) GROUP BY currencyType"
    data = ms.ExecQuery(sql)
    data1 = ms.ExecQuery(sql1)
    return data, data1


def DATA(game):
    Type = game
    ALL = timeQueryMangodb(STARTTIME, ENDTIME)
    sex, sex1 = Gold_list(STARTTIME, ENDTIME, Type)
    game_list = []
    gold_list = []
    gold = []
    for i in ALL:
        if i['gameType'] == Type:
            game_list.append(i['roundId'])
    for i in sex:
        gold_list.append(int(i[1]))
        gold.append(int(i[4]))

    c = [x for x in gold_list if gold_list.count(x) != game_list.count(x) and game_list.count(x) == 0]
    d = [y for y in game_list if gold_list.count(y) < game_list.count(y)]
    e = [i for i in gold_list if gold_list.count(i) != 1]
    # a =[x for x in gold_list if x not in game_list]
    # b =[y for y in game_list if y not in gold_list]
    print('金流输赢', sex1)
    print(f'记录{len(game_list)}记录去重{len(set(game_list))}', '记录丢失局号', set(c))
    print(f'金流{len(gold_list)}金流去重{len(set(gold_list))}', '记录重复局号', set(d))
    return gold_list


def main(game, startime, endtime):
    global li
    oo = Record('Y002', '111', game, startime, endtime)
    # a = oo.getRcords()
    # print(a)
    # b = oo.organizeRecords()
    # print(b)
    # key = b.keys()

    # print(111, gamerecord)
    # print(game)
    # for i in key:
    #     for x in b[i]:
    #         li.append(x['roomInfo']['roundId'])
    li = []
    lis = []
    game = oo.gameReport()
    gamerecord = oo.gameRecord()
    if 'message' not in gamerecord :
        for x in gamerecord['data']:
            lis.append(int(x['roundId']))
    print('后台报表', game)
    print('后台记录局数', len(lis), len(set(lis)))
    cc = [x for x in li if li.count(x) != 1]
    print(cc)
    return li, lis


STARTTIME = "2022-01-20 00:00:00"
ENDTIME = "2022-01-20 23:59:59"


for x, y in GAMETYPELIST.items():
    print('\n', '------------------------')
    print('\n', y)
    gold = DATA(int(x))
    li, lis = main(x, STARTTIME, ENDTIME)
    d = [j for j in gold if j not in lis]
    c = [o for o in lis if o not in gold]
    print(f'纯后台核对有金流无记录{d},无金流有记录{c}')


