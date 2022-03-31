# coding:utf-8
import requests,pymssql,json,pymongo,time,datetime,calendar,os
from dateutil.parser import *
import jpype,configparser
base_dir = os.path.dirname(__file__)
config_path = os.path.join(base_dir, 'login.config')
login_configFile_path = config_path
# login_configFile_path = 'login.config'
def loadConfig():
    cf = configparser.ConfigParser()
    cf.read(login_configFile_path)
    loginConfig = cf.options('config')
    SQLSEVER_HOST = cf.get('config','SQLSEVER_HOST')
    SQLSEVER_PORT = cf.get('config', 'SQLSEVER_PORT')
    USER_NAME = cf.get('config', 'USER_NAME')
    PWD = cf.get('config', 'PWD')
    SQLSEVER_DB = cf.get('config', 'SQLSEVER_DB')
    MANGODB_INFO = cf.get('config', 'MANGODB_ADDRESS')
    MANGODB_VER = cf.get('config', 'MANGODB_DB')
    LOGIN_URL = cf.get('config', 'LOGIN_URL')
    STYLE = cf.get('config', 'STYLE')
    NICK_FIRST_NAME = cf.get('config', 'NICK_FIRST_NAME')
    URL_TYPE = cf.get('config', 'URL_TYPE')
    CURRENCY_TYPE = cf.get('config', 'CURRENCY_TYPE')
    BACK_STAGE_URL = cf.get('config', 'BACK_STAGE_URL')
    MONEY = cf.get('config', 'MONEY')
    GAMETYPE = cf.get('config', 'GAMETYPE')
    return LOGIN_URL,STYLE,NICK_FIRST_NAME,URL_TYPE,CURRENCY_TYPE,BACK_STAGE_URL,MONEY,GAMETYPE,SQLSEVER_HOST,SQLSEVER_PORT,USER_NAME,PWD,SQLSEVER_DB,MANGODB_INFO,MANGODB_VER
LOGIN_URL,STYLE,NICK_FIRST_NAME,URL_TYPE,CURRENCY_TYPE,BACK_STAGE_URL,MONEY,GAMETYPE,SQLSEVER_HOST,SQLSEVER_PORT,USER_NAME,PWD,SQLSEVER_DB,MANGODB_INFO,MANGODB_VER = loadConfig()
class MSSQL:
    def __init__(self, host, user, pwd, db, port):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.port = port


    def GetConnect(self):
        if not self.db:
            raise (NameError, '没有设置数据库信息')
        self.conn = pymssql.connect(host=self.host, user=self.user, password=self.pwd, database=self.db, port=self.port, charset='utf8')
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, '连接数据库失败')
        else:
            return cur

    def ExecQuery(self, sql):
        cur = self.GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()

        self.conn.close()
        return resList

    def ExecNonQuery(self, sql):
        cur = self.GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()

    def GetData(self, sql):
        count = 0
        for i in range(len(sql)):
            for j in range(len(sql[i])):
                count += 1
                if type(sql[i][j]) is str:
                    print(sql[i][j].encode('latin1').decode('gbk'), end=',')
                else:
                    print(sql[i][j], end=',')
                if count % len(sql[i]) == 0:
                    print('\n')
def init_sqlSever():
    ms = MSSQL(host=SQLSEVER_HOST, user=USER_NAME, pwd=PWD, db=SQLSEVER_DB, port=SQLSEVER_PORT)
    ms.GetConnect
    return ms
ms = init_sqlSever()
class Record():
    localUrl = BACK_STAGE_URL
    def __init__(self,username,password,gameType,startTime,endTime):
        self.gameType = gameType
        self.startTime = startTime
        self.endTime = endTime
        self.sessions = requests.session()
        self.username = username
        self.password = password

    def getRcords(self):
        doc = timeQueryMangodbLog(self.startTime,self.endTime,game_type = self.gameType)
        return doc
    def organizeRecords(self):
        responseData = self.getRcords()
        roomRecords = {}
        for records in responseData:  # 按房间分
            roomId = records['roomInfo'].get('roomId',records['roomInfo'].get('roomCfgId'))
            if roomId not in roomRecords.keys():
                roomRecords[roomId] = [records]
            else:
                temrecords = roomRecords[roomId]
                temrecords.append(records)
                roomRecords[roomId] = temrecords
        return roomRecords
    def getToken(self, url):
        username = self.username
        password = self.password
        data = {
            'username': username,
            'password': password
        }
        sessions = self.sessions
        loginUrl = url + "/login"
        response = sessions.post(loginUrl, data=data)
        response = response.json()
        token = response.get("token")
        return token
    def AddGold(self,data,url,style):
        token = self.getToken(url)
        url = url + "/goldAction/manualOperationGold"
        headers = {
            'Content-Type': 'application/json;charset=utf-8',
            'token': token
        }
        data = json.dumps(data)
        response = requests.post(url=url, headers=headers, data=data)
        print(response.text)
        return response.text
class Des_util():
    def __init__(self):
        """ getIdAndStyle(String tk)获取id style
            getStaticIdByDynamicUid(String tk)获取静态id
            decodeStaticUid(String staticUid) 根据静态id获取id style
        """
        jvmPath = jpype.getDefaultJVMPath()
        ext_classpath = r'.\JAVAt.jar'
        jvmArg = '-Djava.class.path=%s' % ext_classpath
        if not jpype.isJVMStarted():
            jpype.startJVM(jvmPath, '-ea', jvmArg)
        javaClass = jpype.JPackage('com.slot.basePlatform.utils').DESUtil
        self.jd = javaClass()
    def get_id_and_style(self,uid):
        id_style = self.jd.decodeStaticUid(uid)
        id = id_style.split(',')[0]
        style = id_style.split(',')[1]
        return id,style
    def get_static_uid(self,tk):
        static_uid = self.jd.staticUid(tk)
        return static_uid
def getExchangeRate():
    sql = "SELECT top 1 rates from dbo.Game_ExchangeRate order by createTime DESC"
    exchangeRate = json.loads(ms.ExecQuery(sql)[0][0])
    exchangeRate.insert(0, {"currencyType": 0, "rate": 1.0, "name": "CNY"})
    return exchangeRate
def getChangedGold(goldDic):
    exchangeRate = getExchangeRate()
    totalGold = 0
    for key,value in goldDic.items():
        totalGold += value / exchangeRate[key]['rate']
    return totalGold
def preciseRound(_float, _len = 0):
    if isinstance(_float, float):
        if str(_float)[::-1].find('.') <= _len:
            if _len == 0:
                return int(_float)
            return(_float)
        if str(_float)[-1] == '5':
            if _len == 0:
                return int(round(float(str(_float)[:-1]+'6'), _len))
            return(round(float(str(_float)[:-1]+'6'), _len))
        else:
            if _len == 0:
                return int(round(_float, _len))
            return(round(_float, _len))
    else:
        if _len == 0:
            return int(round(_float, _len))
        return(round(_float, _len))
def queryMangodb(startTime,endTime,black_List,noneStartTime = False,noneEndTime = False):
    myclient = pymongo.MongoClient(MANGODB_INFO)
    mydb = myclient[MANGODB_VER]
    monthDate = endTime[0:7]
    mycol = mydb["GameUserCount_" + monthDate]
    if noneStartTime and noneEndTime:
        myquery = {"uid": {"$nin": black_List}}
    elif noneStartTime:
        myquery = {"endTime": {'$lt': parse(endTime)}, "uid": {"$nin": black_List}}
    elif noneEndTime:
        myquery = {"endTime": {"$gt": parse(startTime)}, "uid": {"$nin": black_List}}
    else:
        myquery = {"endTime": {"$gt": parse(startTime),'$lt': parse(endTime)}, "uid": {"$nin": black_List}}
    mydoc = mycol.find(myquery)
    return mydoc
def getBlackUserList():
    sql = f"SELECT login.id FROM dbo.Game_UserLoginInfo as login RIGHT JOIN (select userInfo.id from dbo.Game_UserInfoBase as userInfo RIGHT JOIN  dbo.ReportBlacks as black on userInfo.userName = black.userName and userInfo.style =  black.style) as blackId on login.uid = blackId.id WHERE login.style <> 00000"
    black_List = [x[0] for x in ms.ExecQuery(sql)]
    return black_List
def timeQueryMangodb(_startTime,_endTime,black_List):
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
        doc = queryMangodb(startTime,endTime,black_List)
        for x in doc:
            docList.append(x)
    else:
        mon = startTimeArray.tm_mon
        for i in range(0,months + 1):
            if mon == startTimeArray.tm_mon:
                firstDayWeekDay,monthRange = calendar.monthrange(startTimeArray.tm_year,mon)
                monthLastTime = datetime.datetime(year=startTimeArray.tm_year,month=mon,day=monthRange,hour=23,minute=59,second=59)
                startTime = _startTime
                endTime = datetime.datetime.strftime(monthLastTime,"%Y-%m-%d %H:%M:%S")
                doc = queryMangodb(startTime, endTime, black_List,noneEndTime=True)
                for x in doc:
                    docList.append(x)
            elif mon == endTimeArray.tm_mon:
                monthFirstTime = datetime.datetime(year=endTimeArray.tm_year,month=mon,day=1,hour=0,minute=0,second=0)
                startTime = datetime.datetime.strftime(monthFirstTime,"%Y-%m-%d %H:%M:%S")
                endTime = _endTime
                doc = queryMangodb(startTime, endTime, black_List,noneStartTime=True)
                for x in doc:
                    docList.append(x)
            else:
                firstDayWeekDay, monthRange = calendar.monthrange(startTimeArray.tm_year, mon)
                monthFirstTime = datetime.datetime(year=endTimeArray.tm_year, month=mon, day=1, hour=0, minute=0,
                                                   second=0)
                monthLastTime = datetime.datetime(year=startTimeArray.tm_year, month=mon, day=monthRange, hour=23,
                                                  minute=59, second=59)
                startTime = datetime.datetime.strftime(monthFirstTime,"%Y-%m-%d %H:%M:%S")
                endTime = datetime.datetime.strftime(monthLastTime,"%Y-%m-%d %H:%M:%S")
                doc = queryMangodb(startTime, endTime, black_List)
                for x in doc:
                    docList.append(x)
            mon += 1
    return docList
def timeQueryMangodbLog(_startTime,_endTime,game_type = None):
    # _startTime = datetime.datetime.strptime(_startTime, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=-8)
    # _startTime = datetime.datetime.strftime(_startTime, "%Y-%m-%d %H:%M:%S")
    # _endTime = datetime.datetime.strptime(_endTime, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=-8)
    # _endTime = datetime.datetime.strftime(_endTime, "%Y-%m-%d %H:%M:%S")
    startTimeArray = time.strptime(_startTime, "%Y-%m-%d %H:%M:%S")
    endTimeArray = time.strptime(_endTime, "%Y-%m-%d %H:%M:%S")
    months = endTimeArray.tm_mon - startTimeArray.tm_mon
    docList = []
    if months == 0:
        startTime = _startTime
        endTime = _endTime
        doc = get_mangodb_data_by_gameType(startTime,endTime,game_type)
        for x in doc:
            docList.append(x)
    else:
        mon = startTimeArray.tm_mon
        for i in range(0,months + 1):
            if mon == startTimeArray.tm_mon:
                firstDayWeekDay,monthRange = calendar.monthrange(startTimeArray.tm_year,mon)
                monthLastTime = datetime.datetime(year=startTimeArray.tm_year,month=mon,day=monthRange,hour=23,minute=59,second=59)
                startTime = _startTime
                endTime = datetime.datetime.strftime(monthLastTime,"%Y-%m-%d %H:%M:%S")
                doc = get_mangodb_data_by_gameType(startTime, endTime,game_type)
                for x in doc:
                    docList.append(x)
            elif mon == endTimeArray.tm_mon:
                monthFirstTime = datetime.datetime(year=endTimeArray.tm_year,month=mon,day=1,hour=0,minute=0,second=0)
                startTime = datetime.datetime.strftime(monthFirstTime,"%Y-%m-%d %H:%M:%S")
                endTime = _endTime
                doc = get_mangodb_data(startTime, endTime,game_type)
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
                doc = get_mangodb_data_by_gameType(startTime, endTime,game_type)
                for x in doc:
                    docList.append(x)
            mon += 1
    return docList
def getGoldActionRecord(_startTime,_endTime,_actionType,_style):#获取金流记录，参数开始时间，结束时间，actionType元祖，style元祖
    if "'" not in _startTime:
        _startTime = f"'{_startTime}'"
        _endTime = f"'{_endTime}'"
    if isinstance(_style,tuple):
        _style = ",".join(_style)
        _style = f"({_style})"
    if isinstance(_actionType,tuple):
        _actionType = list(map(str,_actionType))
        _actionType = ",".join(_actionType)
        _actionType = f"({_actionType})"
    sql = f"select t.orderId,t.gameType,t.goldNum,t.userName from (select orderId,gameType,goldNum,userName,beforGoldNum,afterGoldNum,beforMoneyNum,afterMoneyNum,creatDate,extendedField1 from dbo.Game_GameGoldActionInfo where creatDate BETWEEN {_startTime} AND {_endTime} and style in {_style} and actionType in {_actionType} UNION all select orderId,gameType,goldNum,userName,beforeGoldNum,afterGoldNum,beforeMoneyNum,afterMoneyNum,creatDate,currencyType from dbo.Game_GoldActionInfo where creatDate BETWEEN {_startTime} AND {_endTime} and style in {_style} and actionType in {_actionType}) as t"
    goldLog = ms.ExecQuery(sql)
    return goldLog
def get_static_uid(tk):
    des_util = Des_util()
    static_uid = des_util.get_static_uid(tk)
    return static_uid
def get_user_gold(tk):
    static_uid = get_static_uid(tk)
    sql = f"SELECT gold,money FROM dbo.Platform_UserInfo where uid = '{static_uid}'"
    gold,money= ms.ExecQuery(sql)[0]
    return gold,money
def get_game_ENname(game_type = None):
    if game_type:
        sql = f'select enName,goldType from Game_Type where gameType = {game_type}'
    else:
        sql = f'select enName,goldType from Game_Type'
    en_name = ms.ExecQuery(sql)
    return en_name
def set_user_gold(tk,gold = 0,money = 0):
    static_uid = get_static_uid(tk)
    ms = MSSQL(host='192.168.10.199', user='test', pwd='123456', db=SQLSEVER_DB, port=1433)
    sql = f"update dbo.Platform_UserInfo set gold = {gold},money = {money} where uid = '{static_uid}'"
    ms.ExecNonQuery(sql)
def get_mangodb_data_by_gameType(startTime, endTime,game_type):
    data_list = []
    myclient = pymongo.MongoClient(MANGODB_INFO)
    mydb = myclient[MANGODB_VER]
    en_gold_type_name = get_game_ENname(game_type = game_type)
    en_name = en_gold_type_name[0][0]
    mycol = mydb[en_name + "Log"]
    startTimeArray = time.strptime(startTime, '%Y-%m-%d %H:%M:%S')
    endTimeArray = time.strptime(endTime, '%Y-%m-%d %H:%M:%S')
    startTime_strptime = int(time.mktime(startTimeArray)) * 1000
    endTime_strptime = int(time.mktime(endTimeArray)) * 1000
    myquery = {'roomInfo.endTime': {'$gt': startTime_strptime, '$lte': endTime_strptime}}
    # print(myquery)
    mydoc = mycol.find(myquery)
    for x in mydoc:
        data_list.append(x)
    return data_list
def get_mangodb_data(startTime,endTime):
    query_small_game_flag = False
    data_list = []
    myclient = pymongo.MongoClient(MANGODB_INFO)
    mydb = myclient[MANGODB_VER]
    en_gold_type_name = get_game_ENname()
    for name_gold_type in en_gold_type_name:
        en_name = name_gold_type[0]
        gold_type = name_gold_type[1]
        print('start:', en_name)
        if gold_type == 2:
            mycol = mydb["LotteryRecordModel"]
            startDateTime = datetime.datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=-8)
            endDateTime = datetime.datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=-8)
            myquery = {"createDate": {"$gt": startDateTime, '$lte': endDateTime}}
            if query_small_game_flag == False:
                mydoc = mycol.find(myquery)
                query_small_game_flag = True
        else:
            mycol = mydb[en_name + "Log"]
            startTimeArray = time.strptime(startTime,'%Y-%m-%d %H:%M:%S')
            endTimeArray = time.strptime(endTime, '%Y-%m-%d %H:%M:%S')
            startTime_strptime = int(time.mktime(startTimeArray)) * 1000
            endTime_strptime = int(time.mktime(endTimeArray)) * 1000
            myquery = {'roomInfo.endTime': {'$gt': startTime_strptime, '$lte': endTime_strptime}}
            mydoc = mycol.find(myquery)
        for x in mydoc:
            data_list.append((gold_type,x,en_name))
    return data_list
def get_userName_by_id(id):
    sql = f'select userName from Game_UserInfoBase where id = (select uid from Game_UserLoginInfo where id = {id})'
    userName = ms.ExecQuery(sql)[0][0]
    return userName
def get_id_by_userName(userName):
    sql = f"select id from Game_UserLoginInfo where uid = (select id from Game_UserInfoBase where userName = {userName}) and style != '00000'"
    id = ms.ExecQuery(sql)[0][0]
    return id
def timeQueryMangodbByGameType(_startTime,_endTime,black_List,gameType=None):
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
        doc = queryMangodbByGameType(startTime,endTime,black_List,gameType=gameType)
        for x in doc:
            docList.append(x)
    else:
        mon = startTimeArray.tm_mon
        for i in range(0,months + 1):
            if mon == startTimeArray.tm_mon:
                firstDayWeekDay,monthRange = calendar.monthrange(startTimeArray.tm_year,mon)
                monthLastTime = datetime.datetime(year=startTimeArray.tm_year,month=mon,day=monthRange,hour=23,minute=59,second=59)
                startTime = _startTime
                endTime = datetime.datetime.strftime(monthLastTime,"%Y-%m-%d %H:%M:%S")
                doc = queryMangodbByGameType(startTime, endTime, black_List,noneEndTime=True,gameType=gameType)
                for x in doc:
                    docList.append(x)
            elif mon == endTimeArray.tm_mon:
                monthFirstTime = datetime.datetime(year=endTimeArray.tm_year,month=mon,day=1,hour=0,minute=0,second=0)
                startTime = datetime.datetime.strftime(monthFirstTime,"%Y-%m-%d %H:%M:%S")
                endTime = _endTime
                doc = queryMangodbByGameType(startTime, endTime, black_List,noneStartTime=True,gameType=gameType)
                for x in doc:
                    docList.append(x)
            else:
                firstDayWeekDay, monthRange = calendar.monthrange(startTimeArray.tm_year, mon)
                monthFirstTime = datetime.datetime(year=endTimeArray.tm_year, month=mon, day=1, hour=0, minute=0,
                                                   second=0)
                monthLastTime = datetime.datetime(year=startTimeArray.tm_year, month=mon, day=monthRange, hour=23,
                                                  minute=59, second=59)
                startTime = datetime.datetime.strftime(monthFirstTime,"%Y-%m-%d %H:%M:%S")
                endTime = datetime.datetime.strftime(monthLastTime,"%Y-%m-%d %H:%M:%S")
                doc = queryMangodbByGameType(startTime, endTime, black_List,gameType=gameType)
                for x in doc:
                    docList.append(x)
            mon += 1
    return docList
def queryMangodbByGameType(startTime,endTime,black_List,noneStartTime = False,noneEndTime = False,gameType = None):
    myclient = pymongo.MongoClient(MANGODB_INFO)
    mydb = myclient[MANGODB_VER]
    monthDate = endTime[0:7]
    mycol = mydb["GameUserCount_" + monthDate]
    if noneStartTime and noneEndTime:
        myquery = {"uid": {"$nin": black_List},"gameType":{"$eq": gameType}}
    elif noneStartTime:
        myquery = {"endTime": {'$lt': parse(endTime)}, "uid": {"$nin": black_List},"gameType":{"$eq": gameType}}
    elif noneEndTime:
        myquery = {"endTime": {"$gt": parse(startTime)}, "uid": {"$nin": black_List},"gameType":{"$eq": gameType}}
    else:
        myquery = {"endTime": {"$gt": parse(startTime),'$lt': parse(endTime)}, "uid": {"$nin": black_List},"gameType":{"$eq": gameType}}
    mydoc = mycol.find(myquery)
    return mydoc
def getGameUserCountUsersCount(startTime,endTime,black_List,*conditions):
    startDateTime = datetime.datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=-8)
    endDateTime = datetime.datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=-8)
    myclient = pymongo.MongoClient(MANGODB_INFO)
    mydb = myclient[MANGODB_VER]
    monthDate = endTime[0:7]
    mycol = mydb["GameUserCount_" + monthDate]
    myquery = {"endTime": {"$gt": startDateTime, '$lt': endDateTime}, "uid": {"$nin": black_List}}
    for condition in conditions:
        myquery.update(condition)
    count = len(mycol.distinct('uid',myquery))
    return count
def getFrozenLog(_startTime,_endTime):
    startDay = _startTime[0:4] + _startTime[5:7] + _startTime[8:10]
    startDay = '20220120'
    sql = f"select roundId,userName,frozenGold from Game_UserFrozenInfo_{startDay} where frozenTime between '{_startTime}' and '{_endTime}' and actionUser = '系统结算'"
    logs = ms.ExecQuery(sql)
    return logs
def get_user_gold_by_userName(userName):
    if not userName.endswith("'"):
        userName = f"'{userName}'"
    sql = f"select money from Game_UserInfo where uid = (select id from Game_UserInfoBase where userName = {userName})"
    money = ms.ExecQuery(sql)[0][0] / 1000000
    return money
def get_userName_max_by_userName_like(userName_like):
    sql = f"select top 1 userName from Game_UserInfoBase where userName LIKE '{userName_like}' order by userName DESC "
    userName_max = ms.ExecQuery(sql)
    if len(userName_max) > 0:
        return userName_max[0][0]
    else:
        return userName_like.replace('%','1000')


