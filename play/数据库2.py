
import pymssql


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


def getSigleData(ms, sql):
    data = ms.ExecQuery(sql)
    ms.GetData(data)
    data = data[0][0]
    return data


def mywritelines(f, mylist):
    mylist = list(map(str, mylist))
    for title in mylist:
        f.write(title + ',')
    f.write('\n')


def SlotGame(game, name):
    ms = MSSQL(host='192.168.10.199', user='test', password='123456', db="OverseasGame", port=1433)
    ms.GetConnect()
    startTime = "'2021-12-06 00:00:00'"
    endTime = "'2021-12-06 16:59:00'"
    gameType = f"'{game}'"
    sql = """
        SELECT COUNT
        ( GoldNum ) AS '总局数',
        SUM ( AntesNum ) AS '投入底注',
        SUM ( Obtain ) AS '开奖金额',
        SUM ( GoldNum ) AS '总输赢' 
    FROM
        dbo.Game_GameGoldActionInfo 
    WHERE
        GameType = """ + gameType + """
        AND CreatDate > """ + startTime + """
        AND CreatDate < """ + endTime + """
        AND Style = 7;
            SELECT COUNT
        ( Obtain ) AS '1000+出现场次',
        ISNULL(SUM( Obtain ),0) AS '开奖金额' 
    FROM
        dbo.Game_GameGoldActionInfo 
    WHERE
        GameType = """ + gameType + """ 
        AND CreatDate > """ + startTime + """ 
        AND CreatDate < """ + endTime + """ 
        AND Obtain >= '1000'*100 
        AND AntesNum != 0;
            SELECT COUNT
        ( Obtain ) AS '500-999出现场次',
        ISNULL(SUM( Obtain ),0) AS '开奖金额'
    FROM
        dbo.Game_GameGoldActionInfo 
    WHERE
        GameType = """ + gameType + """ 
        AND CreatDate > """ + startTime + """ 
        AND CreatDate < """ + endTime + """ 
        AND Obtain >= '500'*100 
        AND Obtain < '1000'*100 
        AND AntesNum != 0 --查询1000+
        AND Style = 7;
            SELECT COUNT
        ( Obtain ) AS '400-499出现场次',
        ISNULL(SUM( Obtain ),0) AS '开奖金额' 
    FROM
        dbo.Game_GameGoldActionInfo 
    WHERE
        GameType = """ + gameType + """ 
        AND CreatDate > """ + startTime + """ 
        AND CreatDate < """ + endTime + """ 
        AND Obtain >= '400' *100 
        AND Obtain < '500' *100
        AND AntesNum != 0 --查询500-999
        AND Style = 7;
            SELECT COUNT
        ( Obtain ) AS '300-399出现场次',
        ISNULL(SUM( Obtain ),0) AS '开奖金额' 
    FROM
        dbo.Game_GameGoldActionInfo 
    WHERE
        GameType = """ + gameType + """ 
        AND CreatDate > """ + startTime + """ 
        AND CreatDate < """ + endTime + """ 
        AND Obtain >= '300'*100 
        AND Obtain < '400'*100 
        AND AntesNum != 0 --查询400-499
        AND Style = 7;
            SELECT COUNT
        ( Obtain ) AS '200-299出现场次',
        ISNULL(SUM( Obtain ),0) AS '开奖金额' 
    FROM
        dbo.Game_GameGoldActionInfo 
    WHERE
        GameType = """ + gameType + """ 
        AND CreatDate > """ + startTime + """ 
        AND CreatDate < """ + endTime + """ 
        AND Obtain >= '200'*100 
        AND Obtain < '300'*100 
        AND AntesNum != 0 --查询300-399
        AND Style = 7;
            SELECT COUNT
        ( Obtain ) AS '100-199出现场次',
        ISNULL(SUM( Obtain ),0) AS '开奖金额' 
    FROM
        dbo.Game_GameGoldActionInfo 
    WHERE
        GameType = """ + gameType + """ 
        AND CreatDate > """ + startTime + """ 
        AND CreatDate < """ + endTime + """ 
        AND Obtain >= '100'*100 
        AND Obtain < '200'*100 
        AND AntesNum != 0 --查询200-299
        AND Style = 7;
           SELECT COUNT
        ( Obtain ) AS '50-99出现场次',
        ISNULL(SUM( Obtain ),0) AS '开奖金额' 
    FROM
        dbo.Game_GameGoldActionInfo 
    WHERE
        GameType = """ + gameType + """ 
        AND CreatDate > """ + startTime + """ 
        AND CreatDate < """ + endTime + """ 
        AND Obtain >= '50'*100 
        AND Obtain < '100'*100 
        AND AntesNum != 0 --查询50-99
        AND Style = 7;
            SELECT COUNT
        ( Obtain ) AS '30-49出现场次',
        ISNULL(SUM( Obtain ),0) AS '开奖金额' 
    FROM
        dbo.Game_GameGoldActionInfo 
    WHERE
        GameType = """ + gameType + """ 
        AND CreatDate > """ + startTime + """ 
        AND CreatDate < """ + endTime + """ 
        AND Obtain >= '30'*100 
        AND Obtain < '50'*100 
        AND AntesNum != 0 --查询50-99
        AND Style = 7;
            SELECT COUNT
        ( Obtain ) AS '1-29出现场次',
        ISNULL(SUM( Obtain ),0) AS '开奖金额' 
    FROM
        dbo.Game_GameGoldActionInfo 
    WHERE
        GameType = """ + gameType + """ 
        AND CreatDate > """ + startTime + """ 
        AND CreatDate < """ + endTime + """ 
        AND Obtain > '0'*100 
        AND Obtain < '30'*100 
        AND AntesNum != 0 --查询30-49
        AND Style = 7;
            SELECT COUNT
        ( Obtain ) AS '0',
        ISNULL(SUM( Obtain ),0) AS '开奖金额' 
    FROM
        dbo.Game_GameGoldActionInfo 
    WHERE
        GameType = """ + gameType + """ 
        AND CreatDate > """ + startTime + """ 
        AND CreatDate < """ + endTime + """ 
        AND Obtain = '0' 
        AND AntesNum != 0 --查询0
        AND Style = 7;

    SELECT COUNT
        ( Obtain ) AS '红利赢场次' 
    FROM
        dbo.Game_GameGoldActionInfo 
    WHERE
        GameType = """ + gameType + """ 
        AND CreatDate > """ + startTime + """ 
        AND CreatDate < """ + endTime + """ 
        AND Obtain > 0
        AND AntesNum=0
    """
    sql_list = sql.split(";")
    tableNormalModelDic = []
    sumObtainNormalModel = 0
    countObtainNormalModel = 0
    sum200uptimes = 0
    for sqlIndex in range(len(sql_list)):
        print(sqlIndex)
        # print(sql_list[sqlIndex])
        data = ms.ExecQuery(sql_list[sqlIndex])
        ms.GetData(data)
        if sqlIndex == 0:
            GamesCount, sumAntesNum, sumObtain,sumGoldNum = data[0]
            print("sumObtain",sumObtain)
        elif 0 < sqlIndex < 11:
            countObtainNormal, sumObtainNormal = data[0]
            sumObtainNormalModel += int(sumObtainNormal)
            countObtainNormalModel += int(countObtainNormal)
            if 6 <= sqlIndex < 11:
                sum200uptimes += int(countObtainNormal)
            tableNormalModelDic.append([countObtainNormal, sumObtainNormal])
        elif sqlIndex == 11:
            fsWinTimes = data[0][0]
    with open("win_rata.csv", "a", encoding='UTF-8') as f:
        f.write('\n' * 2)
        f.write(name + gameType + '\n')
        f.write(startTime.replace("'","") + "-" + endTime.replace("'","") + '\n')
        titleList = ['游戏场次','总底注量','总获取奖项数额','总输赢金币','输赢投注比']
        mywritelines(f, titleList)
        print(GamesCount,sumAntesNum,sumObtain,sumGoldNum)
        row4 = [GamesCount,sumAntesNum,sumObtain,sumGoldNum, sumGoldNum/sumAntesNum]
        mywritelines(f, row4)
        titleList2 = ['普通场开奖倍数','出现场次','开奖额','总场次占比','玩家赢数据占比']
        mywritelines(f, titleList2)
        awardAreamList = ['1000+','999~500','499~400','399~300','299~200','199~100','99~50','49~30','1~29','=0']
        # awardAreamList.reverse()
        for i in range(len(tableNormalModelDic)):
            tableNormalModel = tableNormalModelDic[i]
            awardAream = awardAreamList[i]
            tableNormalModel =  [awardAream] + tableNormalModel
            tableNormalModel.append(int(tableNormalModel[1])/countObtainNormalModel)
            tableNormalModel.append(int(tableNormalModel[2])/sumObtainNormalModel)
            mywritelines(f, tableNormalModel)
        row5 = ['合计开奖',countObtainNormalModel,sumObtainNormalModel]
        mywritelines(f, row5)
        countfstimes = GamesCount - countObtainNormalModel
        sumfs = sumObtain - sumObtainNormalModel
        row6 = ['红利次数/奖项',countfstimes ,sumfs]
        mywritelines(f, row6)
        row7 = ['红利赢场次', fsWinTimes]
        mywritelines(f, row7)

        # row7 = ["》200",sum200uptimes]
        # mywritelines(f, row7)
        # row8 = ["比例",sum200uptimes]

     
def GamesApp(game, name):
    ms = MSSQL(host='192.168.10.199', user='test', pwd='123456', db="GamesApp", port=1433)
    ms.GetConnect()
    startTime = "'2021-09-15 18:00:00'"
    endTime = "'2021-09-15 15:40:00'"
    gameType = f"'{game}'"
    sql = """
        SELECT COUNT
        ( GoldNum ) AS '总局数',
        SUM ( AntesNum ) AS '投入底注',
        SUM ( Obtain ) AS '开奖金额',
        SUM ( GoldNum ) AS '总输赢' 
    FROM
        dbo.Game_GameGoldActionInfo 
    WHERE
        GameType = """ + gameType + """
        AND CreatDate > """ + startTime + """
        AND CreatDate < """ + endTime + """
        AND Style = 799;
            SELECT COUNT
        ( Obtain ) AS '1000+出现场次',
        ISNULL(SUM( Obtain ),0) AS '开奖金额' 
    FROM
        dbo.Game_GameGoldActionInfo 
    WHERE
        GameType = """ + gameType + """ 
        AND CreatDate > """ + startTime + """ 
        AND CreatDate < """ + endTime + """ 
        AND Obtain >= '1000'*100 
        AND AntesNum != 0;
            SELECT COUNT
        ( Obtain ) AS '500-999出现场次',
        SUM ( Obtain ) AS '开奖金额'
    FROM
        dbo.Game_GameGoldActionInfo 
    WHERE
        GameType = """ + gameType + """ 
        AND CreatDate > """ + startTime + """ 
        AND CreatDate < """ + endTime + """ 
        AND Obtain >= '500'*100 
        AND Obtain < '1000'*100 
        AND AntesNum != 0 --查询1000+
        AND Style = 799;
            SELECT COUNT
        ( Obtain ) AS '400-499出现场次',
        SUM ( Obtain ) AS '开奖金额' 
    FROM
        dbo.Game_GameGoldActionInfo 
    WHERE
        GameType = """ + gameType + """ 
        AND CreatDate > """ + startTime + """ 
        AND CreatDate < """ + endTime + """ 
        AND Obtain >= '400' *100 
        AND Obtain < '500' *100
        AND AntesNum != 0 --查询500-999
        AND Style = 799;
            SELECT COUNT
        ( Obtain ) AS '300-399出现场次',
        SUM ( Obtain ) AS '开奖金额' 
    FROM
        dbo.Game_GameGoldActionInfo 
    WHERE
        GameType = """ + gameType + """ 
        AND CreatDate > """ + startTime + """ 
        AND CreatDate < """ + endTime + """ 
        AND Obtain >= '300'*100 
        AND Obtain < '400'*100 
        AND AntesNum != 0 --查询400-499
        AND Style = 799;
            SELECT COUNT
        ( Obtain ) AS '200-299出现场次',
        SUM ( Obtain ) AS '开奖金额' 
    FROM
        dbo.Game_GameGoldActionInfo 
    WHERE
        GameType = """ + gameType + """ 
        AND CreatDate > """ + startTime + """ 
        AND CreatDate < """ + endTime + """ 
        AND Obtain >= '200'*100 
        AND Obtain < '300'*100 
        AND AntesNum != 0 --查询300-399
        AND Style = 799;
            SELECT COUNT
        ( Obtain ) AS '100-199出现场次',
        SUM ( Obtain ) AS '开奖金额' 
    FROM
        dbo.Game_GameGoldActionInfo 
    WHERE
        GameType = """ + gameType + """ 
        AND CreatDate > """ + startTime + """ 
        AND CreatDate < """ + endTime + """ 
        AND Obtain >= '100'*100 
        AND Obtain < '200'*100 
        AND AntesNum != 0 --查询200-299
        AND Style = 799;
           SELECT COUNT
        ( Obtain ) AS '50-99出现场次',
        SUM ( Obtain ) AS '开奖金额' 
    FROM
        dbo.Game_GameGoldActionInfo 
    WHERE
        GameType = """ + gameType + """ 
        AND CreatDate > """ + startTime + """ 
        AND CreatDate < """ + endTime + """ 
        AND Obtain >= '50'*100 
        AND Obtain < '100'*100 
        AND AntesNum != 0 --查询50-99
        AND Style = 799;
            SELECT COUNT
        ( Obtain ) AS '30-49出现场次',
        SUM ( Obtain ) AS '开奖金额' 
    FROM
        dbo.Game_GameGoldActionInfo 
    WHERE
        GameType = """ + gameType + """ 
        AND CreatDate > """ + startTime + """ 
        AND CreatDate < """ + endTime + """ 
        AND Obtain >= '30'*100 
        AND Obtain < '50'*100 
        AND AntesNum != 0 --查询50-99
        AND Style = 799;
            SELECT COUNT
        ( Obtain ) AS '1-29出现场次',
        SUM ( Obtain ) AS '开奖金额' 
    FROM
        dbo.Game_GameGoldActionInfo 
    WHERE
        GameType = """ + gameType + """ 
        AND CreatDate > """ + startTime + """ 
        AND CreatDate < """ + endTime + """ 
        AND Obtain > '0'*100 
        AND Obtain < '30'*100 
        AND AntesNum != 0 --查询30-49
        AND Style = 799;
            SELECT COUNT
        ( Obtain ) AS '0',
        SUM ( Obtain ) AS '开奖金额' 
    FROM
        dbo.Game_GameGoldActionInfo 
    WHERE
        GameType = """ + gameType + """ 
        AND CreatDate > """ + startTime + """ 
        AND CreatDate < """ + endTime + """ 
        AND Obtain = '0' 
        AND AntesNum != 0 --查询0
        AND Style = 799;

    SELECT COUNT
        ( Obtain ) AS '红利赢场次' 
    FROM
        dbo.Game_GameGoldActionInfo 
    WHERE
        GameType = """ + gameType + """ 
        AND CreatDate > """ + startTime + """ 
        AND CreatDate < """ + endTime + """ 
        AND Obtain > 0
        AND AntesNum=0
    """
    sql_list = sql.split(";")
    tableNormalModelDic = []
    sumObtainNormalModel = 0
    countObtainNormalModel = 0
    sum200uptimes = 0
    for sqlIndex in range(len(sql_list)):
        print(sqlIndex)
        # print(sql_list[sqlIndex])
        data = ms.ExecQuery(sql_list[sqlIndex])
        ms.GetData(data)
        if sqlIndex == 0:
            GamesCount,sumAntesNum,sumObtain,sumGoldNum = data[0]
            print("sumObtain",sumObtain)
        elif 0 < sqlIndex < 11:
            countObtainNormal, sumObtainNormal = data[0]
            sumObtainNormalModel += int(sumObtainNormal)
            countObtainNormalModel += int(countObtainNormal)
            if 6 <= sqlIndex < 11:
                sum200uptimes += int(countObtainNormal)
            tableNormalModelDic.append([countObtainNormal, sumObtainNormal])
        elif sqlIndex == 11:
            fsWinTimes = data[0][0]
    with open("win_rata.csv", "a") as f:
        f.write('\n' * 2)
        f.write(name + gameType + '\n')
        f.write(startTime.replace("'","") + " | " + endTime.replace("'","") + '\n')
        titleList = ['游戏场次','总底注量','总获取奖项数额','总输赢金币','输赢投注比']
        mywritelines(f, titleList)
        row4 = [GamesCount,sumAntesNum,sumObtain,sumGoldNum,sumGoldNum/sumAntesNum]
        mywritelines(f, row4)
        titleList2 = ['普通场开奖倍数','出现场次','开奖额','总场次占比','玩家赢数据占比']
        mywritelines(f, titleList2)
        awardAreamList = ['1000+','999~500','499~400','399~300','299~200','199~100','99~50','49~30','1~29','=0']
        # awardAreamList.reverse()
        for i in range(len(tableNormalModelDic)):
            tableNormalModel = tableNormalModelDic[i]
            awardAream = awardAreamList[i]
            tableNormalModel =  [awardAream] + tableNormalModel
            tableNormalModel.append(int(tableNormalModel[1])/countObtainNormalModel)
            tableNormalModel.append(int(tableNormalModel[2])/sumObtainNormalModel)
            mywritelines(f, tableNormalModel)
        row5 = ['合计开奖',countObtainNormalModel,sumObtainNormalModel]
        mywritelines(f, row5)
        countfstimes = GamesCount - countObtainNormalModel
        sumfs = sumObtain - sumObtainNormalModel
        row6 = ['红利次数/奖项',countfstimes ,sumfs]
        mywritelines(f, row6)
        row7 = ['红利赢场次', fsWinTimes]
        mywritelines(f, row7)

        # row7 = ["》200",sum200uptimes]
        # mywritelines(f, row7)
        # row8 = ["比例",sum200uptimes]


def SlotGame1(game, name):
    ms = MSSQL(host='192.168.10.199', user='test', pwd='123456', db="OverseasGame", port=1433)
    ms.GetConnect()
    startTime = "'2021-12-06 00:00:00'"
    endTime = "'2021-12-07 08:59:00'"
    gameType = f"'{game}'"
    sql = """
        SELECT COUNT
        ( GoldNum ) AS '总局数',
        SUM ( AntesNum ) AS '投入底注',
        SUM ( Obtain ) AS '开奖金额',
        SUM ( GoldNum ) AS '总输赢' 
    FROM
        dbo.Game_GameGoldActionInfo 
    WHERE
        GameType = """ + gameType + """
        AND CreatDate > """ + startTime + """
        AND CreatDate < """ + endTime + """

            SELECT COUNT
        ( Obtain ) AS '1000+出现场次',
        ISNULL(SUM( Obtain ),0) AS '开奖金额' 
    FROM
        dbo.Game_GameGoldActionInfo 
    WHERE
        GameType = """ + gameType + """ 
        AND CreatDate > """ + startTime + """ 
        AND CreatDate < """ + endTime + """ 
        AND Obtain >= '1000'*100 
        AND AntesNum != 0;
            SELECT COUNT
        ( Obtain ) AS '500-999出现场次',
        ISNULL(SUM( Obtain ),0) AS '开奖金额'
    FROM
        dbo.Game_GameGoldActionInfo 
    WHERE
        GameType = """ + gameType + """ 
        AND CreatDate > """ + startTime + """ 
        AND CreatDate < """ + endTime + """ 
        AND Obtain >= '500'*100 
        AND Obtain < '1000'*100 
        AND AntesNum != 0 --查询1000+

            SELECT COUNT
        ( Obtain ) AS '400-499出现场次',
        ISNULL(SUM( Obtain ),0) AS '开奖金额' 
    FROM
        dbo.Game_GameGoldActionInfo 
    WHERE
        GameType = """ + gameType + """ 
        AND CreatDate > """ + startTime + """ 
        AND CreatDate < """ + endTime + """ 
        AND Obtain >= '400' *100 
        AND Obtain < '500' *100
        AND AntesNum != 0 --查询500-999

            SELECT COUNT
        ( Obtain ) AS '300-399出现场次',
        ISNULL(SUM( Obtain ),0) AS '开奖金额' 
    FROM
        dbo.Game_GameGoldActionInfo 
    WHERE
        GameType = """ + gameType + """ 
        AND CreatDate > """ + startTime + """ 
        AND CreatDate < """ + endTime + """ 
        AND Obtain >= '300'*100 
        AND Obtain < '400'*100 
        AND AntesNum != 0 --查询400-499

            SELECT COUNT
        ( Obtain ) AS '200-299出现场次',
        ISNULL(SUM( Obtain ),0) AS '开奖金额' 
    FROM
        dbo.Game_GameGoldActionInfo 
    WHERE
        GameType = """ + gameType + """ 
        AND CreatDate > """ + startTime + """ 
        AND CreatDate < """ + endTime + """ 
        AND Obtain >= '200'*100 
        AND Obtain < '300'*100 
        AND AntesNum != 0 --查询300-399

            SELECT COUNT
        ( Obtain ) AS '100-199出现场次',
        ISNULL(SUM( Obtain ),0) AS '开奖金额' 
    FROM
        dbo.Game_GameGoldActionInfo 
    WHERE
        GameType = """ + gameType + """ 
        AND CreatDate > """ + startTime + """ 
        AND CreatDate < """ + endTime + """ 
        AND Obtain >= '100'*100 
        AND Obtain < '200'*100 
        AND AntesNum != 0 --查询200-299

           SELECT COUNT
        ( Obtain ) AS '50-99出现场次',
        ISNULL(SUM( Obtain ),0) AS '开奖金额' 
    FROM
        dbo.Game_GameGoldActionInfo 
    WHERE
        GameType = """ + gameType + """ 
        AND CreatDate > """ + startTime + """ 
        AND CreatDate < """ + endTime + """ 
        AND Obtain >= '50'*100 
        AND Obtain < '100'*100 
        AND AntesNum != 0 --查询50-99

            SELECT COUNT
        ( Obtain ) AS '30-49出现场次',
        ISNULL(SUM( Obtain ),0) AS '开奖金额' 
    FROM
        dbo.Game_GameGoldActionInfo 
    WHERE
        GameType = """ + gameType + """ 
        AND CreatDate > """ + startTime + """ 
        AND CreatDate < """ + endTime + """ 
        AND Obtain >= '30'*100 
        AND Obtain < '50'*100 
        AND AntesNum != 0 --查询50-99

            SELECT COUNT
        ( Obtain ) AS '1-29出现场次',
        ISNULL(SUM( Obtain ),0) AS '开奖金额' 
    FROM
        dbo.Game_GameGoldActionInfo 
    WHERE
        GameType = """ + gameType + """ 
        AND CreatDate > """ + startTime + """ 
        AND CreatDate < """ + endTime + """ 
        AND Obtain > '0'*100 
        AND Obtain < '30'*100 
        AND AntesNum != 0 --查询30-49

            SELECT COUNT
        ( Obtain ) AS '0',
        ISNULL(SUM( Obtain ),0) AS '开奖金额' 
    FROM
        dbo.Game_GameGoldActionInfo 
    WHERE
        GameType = """ + gameType + """ 
        AND CreatDate > """ + startTime + """ 
        AND CreatDate < """ + endTime + """ 
        AND Obtain = '0' 
        AND AntesNum != 0 --查询0


    SELECT COUNT
        ( Obtain ) AS '红利赢场次' 
    FROM
        dbo.Game_GameGoldActionInfo 
    WHERE
        GameType = """ + gameType + """ 
        AND CreatDate > """ + startTime + """ 
        AND CreatDate < """ + endTime + """ 
        AND Obtain > 0
        AND AntesNum=0
    """
    sql_list = sql.split(";")
    tableNormalModelDic = []
    sumObtainNormalModel = 0
    countObtainNormalModel = 0
    sum200uptimes = 0
    for sqlIndex in range(len(sql_list)):
        print(sqlIndex)
        # print(sql_list[sqlIndex])
        data = ms.ExecQuery(sql_list[sqlIndex])
        ms.GetData(data)
        if sqlIndex == 0:
            GamesCount, sumAntesNum, sumObtain,sumGoldNum = data[0]
            print("sumObtain",sumObtain)
        elif 0 < sqlIndex < 11:
            countObtainNormal, sumObtainNormal = data[0]
            sumObtainNormalModel += int(sumObtainNormal)
            countObtainNormalModel += int(countObtainNormal)
            if 6 <= sqlIndex < 11:
                sum200uptimes += int(countObtainNormal)
            tableNormalModelDic.append([countObtainNormal, sumObtainNormal])
        elif sqlIndex == 11:
            fsWinTimes = data[0][0]
    with open("win_rata.csv", "a", encoding='UTF-8') as f:
        f.write('\n' * 2)
        f.write(name + gameType + '\n')
        f.write(startTime.replace("'","") + "-" + endTime.replace("'","") + '\n')
        titleList = ['游戏场次','总底注量','总获取奖项数额','总输赢金币','输赢投注比']
        mywritelines(f, titleList)
        print(GamesCount,sumAntesNum,sumObtain,sumGoldNum)
        row4 = [GamesCount,sumAntesNum,sumObtain,sumGoldNum, sumGoldNum/sumAntesNum]
        mywritelines(f, row4)
        titleList2 = ['普通场开奖倍数','出现场次','开奖额','总场次占比','玩家赢数据占比']
        mywritelines(f, titleList2)
        awardAreamList = ['1000+','999~500','499~400','399~300','299~200','199~100','99~50','49~30','1~29','=0']
        # awardAreamList.reverse()
        for i in range(len(tableNormalModelDic)):
            tableNormalModel = tableNormalModelDic[i]
            awardAream = awardAreamList[i]
            tableNormalModel =  [awardAream] + tableNormalModel
            tableNormalModel.append(int(tableNormalModel[1])/countObtainNormalModel)
            tableNormalModel.append(int(tableNormalModel[2])/sumObtainNormalModel)
            mywritelines(f, tableNormalModel)
        row5 = ['合计开奖',countObtainNormalModel,sumObtainNormalModel]
        mywritelines(f, row5)
        countfstimes = GamesCount - countObtainNormalModel
        sumfs = sumObtain - sumObtainNormalModel
        row6 = ['红利次数/奖项',countfstimes ,sumfs]
        mywritelines(f, row6)
        row7 = ['红利赢场次', fsWinTimes]
        mywritelines(f, row7)

        # row7 = ["》200",sum200uptimes]
        # mywritelines(f, row7)
        # row8 = ["比例",sum200uptimes]


if __name__ == '__main__':
    dic = {125:'不朽情缘c#9000',126:'花花公子java8002__free3',127:'粉红女郎',128:'兰桂坊',130:'东方珍兽Java8001',131:'比基尼Java8001'
         ,132:'舞龙Java8001',133:'宝石转轴Java8001',134:'炙热欲望Java8001',135:'招财鞭炮Java8001',136:'幸运富豪Java8001',144:'迷失拉斯维加斯-僵尸',145:'迷失拉斯维加斯-僵尸'}
    li = [127,128,130,131,132,133,134,135,136,141]
    # lis = [131,132,133,134,135,136]
    # for i in lis:
    #     print(i)
    #     SlotGame(i, dic[i])
    SlotGame(131, dic[131])



