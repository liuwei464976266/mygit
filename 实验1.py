import requests, threading, logAnalysisUtil, json


def addGold(tk, money):
    url = 'http://18.167.1.28:8031/api/UserCore/AddPlayerGold'
    headers = {'Accept': '*/*',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Connection': 'keep-alive',
               'Content-Length': '94',
               'Content-Type': 'application/json',
               'Cookie': 'JSESSIONID=6F422CD9F2FF78E8DF14CA6DBE7438EE7239',
               'Host': "192.168.10.25:9002",
               'Origin': 'http://18.167.1.28:8031',
               }

    data = {"tk": tk, "type": 1, "money": money * 100, "timestamp": "1638779262282"}
    response = requests.post(url, headers=headers, json=data)
    print(response.text)


def cc():
    for i in range(100):
        addGold('857B21D5AF34B8806E5E', 1)


def get():
    a = 'liu9009'
    uid = 221
    ms = logAnalysisUtil.MSSQL(host='192.168.10.199', user='test', pwd='123456', db="OverseasGame", port=1433)
    ma = logAnalysisUtil.MSSQL(host='192.168.10.199', user='test', pwd='123456', db="ThirdPartyDB", port=1433)
    ms.GetConnect()
    ma.GetConnect()
    sql = [f"SELECT ISNULL(SUM(goldNum),0) from dbo.Game_GoldActionInfo WHERE userName='{a}' AND actionType='104'",
           f"SELECT ISNULL(SUM(gold),0) from dbo.Tran_Order_Info WHERE userName='{a}' AND status=1",
           f"SELECT SUM(goldNum) from dbo.Game_GoldActionInfo WHERE userName='{a}' AND actionType='103'"]

    sql1 = f"SELECT COUNT(operatingGold) from dbo.ThirdParty_OrderRecord WHERE  uid={uid} AND type=2"

    sql2 = [f"SELECT orderId from dbo.Tran_Order_Info WHERE userName='{a}' AND status=1",
            f"SELECT orderId from dbo.ThirdParty_OrderRecord WHERE  uid={uid} AND type=2"]
    print('转出金额，转入金额，超时冻结的金额')
    nus = []
    for i in sql:
        data = ms.ExecQuery(i)
        nu = data[0][0] / 100
        print(nu)
        nus.append(nu)
    nu = nus[0] - nus[1] + nus[2]
    print('大厅显示余额', nu)
    data1 = ma.ExecQuery(sql1)
    a1 = data1[0][0]
    print('三方成功的次数==平台余额', data1[0][0])
    dat, dac = ms.ExecQuery(sql2[0]), ma.ExecQuery(sql2[1])
    e = [i for i in dat if i not in dac]
    c = [i for i in dat if i in dac]
    print('冻结局数', len(dat))
    print('可解冻成功局', len(e))
    print(nu+a1+len(e))
    print(c)
    print(e)


def get1():
    a = 'liu9009'
    uid = 222
    ms = logAnalysisUtil.MSSQL(host='192.168.10.199', user='test', pwd='123456', db="OverseasGame", port=1433)
    ma = logAnalysisUtil.MSSQL(host='192.168.10.199', user='test', pwd='123456', db="ThirdPartyDB", port=1433)
    ms.GetConnect()
    ma.GetConnect()
    sql = [f"SELECT ISNULL(SUM(goldNum),0) from dbo.Game_GoldActionInfo WHERE userName='{a}' AND actionType='104'",
           f"SELECT ISNULL(SUM(gold),0) from dbo.Tran_Order_Info WHERE userName='{a}' AND status=1",
           f"SELECT SUM(goldNum) from dbo.Game_GoldActionInfo WHERE userName='{a}' AND actionType='103'"]

    sql1 = f"SELECT COUNT(operatingGold) from dbo.ThirdParty_OrderRecord WHERE  uid={uid} AND type=2"

    sql2 = [f"SELECT orderId from dbo.Tran_Order_Info WHERE userName='{a}' AND status=2",
            f"SELECT orderId from dbo.ThirdParty_OrderRecord WHERE  uid={uid} AND type=1"]
    print('转出金额，转入金额，超时冻结的金额')
    nus = []
    for i in sql:
        data = ms.ExecQuery(i)
        nu = data[0][0] / 100
        print(nu)
        nus.append(nu)
    nu = nus[0] - nus[1] + nus[2]
    print('大厅显示余额', nu)
    data1 = ma.ExecQuery(sql1)
    a1 = data1[0][0]
    print('三方成功的次数==平台余额', data1[0][0])
    dat, dac = ms.ExecQuery(sql2[0]), ma.ExecQuery(sql2[1])
    e = len([i for i in dat if i not in dac])
    c = len([i for i in dat if i in dac])
    print(e,c)
    print('冻结局数', len(dat), len(dac), len(dat)-len(dac), 50000-len(dac))


thread = []

for i in range(10):
    a = threading.Thread(target=cc,)
    thread.append(a)
    a.start()

# for i in thread:
#     i.join()
# get1()
