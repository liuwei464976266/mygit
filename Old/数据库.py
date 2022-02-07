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
        self.conn = pymssql.connect(host=self.host, user=self.user, password=self.pwd, database=self.db, port=self.port,
                                    charset='utf8')
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


def main():
    ma = MSSQL(host='192.168.10.129', user='test', pwd='123456', db="SlotGame", port=1433)
    ma.GetConnect()
    sql1 = ma.ExecQuery("SELECT Count(Obtain) FROM [dbo].[Game_GameGoldActionInfo] WHERE  CreatDate >'2020-10-10 09:06:00' AND CreatDate <'2020-10-29 10:18:00'AND AntesNum>0 AND Obtain>=100000")
    print(sql1)


if __name__ == '__main__':
    game = list(range(130, 136))
    numD = [1000,500,400,300,200,100,50,30,29]
    numX = [1000000000,1000,500,400,300,200,100,50,1]
    ms = MSSQL(host='192.168.10.129', user='test', pwd='123456', db="Gamesapp", port=1433)


    for game1 in game:
        print(game1, '游戏数据开始记录 大于---小于 ')

        for i in range(9):
            sql2 = f"SELECT COUNT( Obtain), SUM ( Obtain )  FROM dbo.SmallGameGoldActionInfo WHERE GameType = {game1} AND CreatDate > '2020-10-28 18:00:00' AND CreatDate < '2020-10-29 09:00:00' AND Obtain >= {numD[i] * 100} AND Obtain < {numX[i] * 100} AND AntesNum != 0"
            # print(sql2)
            d = ms.ExecQuery(sql2)
            x,y =d[0]
            print(x, y)

            #
            # x, y = d[0]
            # print(x, y)

