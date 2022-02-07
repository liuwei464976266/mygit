import pymssql


def call_sp_test():

    # 打开数据库连接
    db = pymssql.connect(host='192.168.10.199', user='test', pwd='123456', db="OverseasGame", port=1433)
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    try:
        cursor.execute(f"exec 存储过程名称 @参数1='xxx',@参数2='xxx',@参数3='xxx',@参数4='xxx'")
        db.commit()
    except Exception as e:
        print(e)
    db.close()