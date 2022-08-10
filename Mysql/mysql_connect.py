# -*- coding: UTF-8 -*-
import pymysql


class MySQL:
    def __init__(self, host, user, pwd, db, port):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.port = port

    def GetConnect(self):
        if not self.db:
            raise (NameError, '没有设置数据库信息')
        self.conn = pymysql.connect(host=self.host, user=self.user, password=self.pwd, database=self.db, port=self.port, charset='utf8')
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, '连接数据库失败')
        else:
            return cur

    def ExecQuery(self, sql):
        cur = self.GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()
        return resList

    def ExecNonQuery(self, sql):
        cur = self.GetConnect()
        cur.execute(sql)
        self.conn.commit()

