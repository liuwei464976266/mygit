from logAnalysisUtil import MSSQL


def updateGold(userName,money):
    ms = MSSQL(host='192.168.10.199', user='test', pwd='123456', db="OverseasGameV1", port=1433)
    ms.GetConnect()
    sql = f"UPDATE [dbo].[Game_UserInfo] SET [money] = {money} WHERE [uid] = (SELECT id FROM dbo.Game_UserInfoBase WHERE userName = '{userName}')"
    ms.ExecNonQuery(sql)

updateGold('L878787', 300)


