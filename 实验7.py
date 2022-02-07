import pymssql,time
"""配置"""

def start():
    server = '192.168.10.199'
    user = 'test'
    password = '123456'
    database = "OverseasGame"
    conn = pymssql.connect(server, user, password, database, port=1433)
    cursor = conn.cursor()
    aaa=f'''exec sp_Api_NewHundredsFrozen2v6 @uId={uId},@uFrozenGold={uFrozenGold},@uGenerateGUID2={uGenerateGUID2},
                   @uRoomConfigId={uRoomConfigId},@uRoundId={uRoundId},
                   @uStyle={uStyle},@uGameType={uGameType},@uSid={uSid},@uRoomId={uRoomId},@ufrozenTime={ufrozenTime},
                   @uActionType={uActionType},
                   @returnValue={returnValue},@uFrozenMoney={uFrozenMoney},@uActionTime={uActionTime}'''

    # cursor.execute(f'exec sp_Api_NewHundredsFrozen2v6 @uId={uId},@uFrozenGold={uFrozenGold},@uGenerateGUID2={uGenerateGUID2},@uRoomConfigId={uRoomConfigId},@uRoundId={uRoundId},@uStyle={uStyle},@uGameType={uGameType},@uSid={uSid},@uRoomId={uRoomId},@ufrozenTime={ufrozenTime},@uActionType={uActionType},@returnValue={returnValue},@uFrozenMoney={uFrozenMoney},@uActionTime={uActionTime}')

    cursor.execute(f'exec abc @type={uId}, @id={uRoundId},@style={uGameType}')

    # cursor.callproc('abc', (uId,uRoundId,uGameType))

    '''UID是userinfobase的ID   uFrozenGold是冻结金币 @uGenerateGUID2生成唯一键  @uRoomConfigId=房间ID
    @uRoundId=记录编号  @uStyle =玩家style    uGameType=游戏ID  @uSid=电脑IP   @uRoomId=房间编号 frozenTime=冻结时间
    @uActionType=1赢 12输  returnValue=返回值   @uFrozenMoney=冻结货币  @uActionTime
        
    '''

    result = cursor.fetchall()  #得到结果集
    for i in result:
        print(i)


uId= 1046
uFrozenGold= '100'
uGenerateGUID2= 3
uRoomConfigId= '5662'
uRoundId= '5625544591'
uStyle= '36'
uGameType= 32
uSid = '192.168.10.22'
uRoomId = 15454133
ufrozenTime = '2021-12-06 00:00:00'
uActionType = '1'
returnValue = 10
uFrozenMoney = uFrozenGold*0000
uActionTime = time.time()*1000

start()




