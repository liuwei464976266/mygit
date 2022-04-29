import os,requests,json,re,time,logAnalysisUtil
goldPoolRuduce = 5
goldPoolLog = {}
sql = "SELECT orderId,userName,goldNum FROM Game_GoldActionInfo WHERE userName = 'liu501uIi'"
ms = logAnalysisUtil.ms
datas = ms.ExecQuery(sql)
for data in datas:
    roundId = str(data[0])

    gold = data[-1]
    if gold > 0:
        goldPoolLog[roundId] = -gold
    else:
        goldPoolLog[roundId] = -gold * 0.95
print(goldPoolLog)
for root, dirs, files in os.walk(r"\\DESKTOP-ER67CM9\GoldPool\48"):
    for file in files:
        if file.endswith('txt'):
            goldPoolFilePath = os.path.join(root,file)
            with open(goldPoolFilePath,'r',encoding='utf-8') as f:
                goldPoolData = f.read()
                goldPoolData = json.loads(goldPoolData)
                preUserGoldPool = goldPoolData.get('结算前库存', {}).get('0B1CF62FD93DF49E5CAD14D14A0302BD_231', '0')
                userGoldPool = goldPoolData.get('结算后库存',{}).get('0B1CF62FD93DF49E5CAD14D14A0302BD_231','0')
                if preUserGoldPool != '0':
                    roundId = file.split(r'.')[0]
                    print(roundId)
                    if abs((userGoldPool - preUserGoldPool) - goldPoolLog.get(roundId,0)) > 2:
                        print(roundId,'实际库存',userGoldPool - preUserGoldPool,'应有库存',goldPoolLog.get(roundId,0))
