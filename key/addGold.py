import logAnalysisUtil,configparser
login_configFile_path = r'D:\pytest\key\login.config'
def loadConfig():
    cf = configparser.ConfigParser()
    cf.read(login_configFile_path)
    # loginConfig = cf.options('config')
    LOGIN_URL = cf.get('config','LOGIN_URL')
    STYLE = cf.get('config', 'STYLE')
    NICK_FIRST_NAME = cf.get('config', 'NICK_FIRST_NAME')
    URL_TYPE = cf.get('config', 'URL_TYPE')
    CURRENCY_TYPE = cf.get('config', 'CURRENCY_TYPE')
    BACK_STAGE_URL = cf.get('config', 'BACK_STAGE_URL')
    MONEY = cf.get('config', 'MONEY')
    GAMETYPE = cf.get('config', 'GAMETYPE')
    return LOGIN_URL,STYLE,NICK_FIRST_NAME,URL_TYPE,CURRENCY_TYPE,BACK_STAGE_URL,MONEY,GAMETYPE
LOGIN_URL,STYLE,NICK_FIRST_NAME,URL_TYPE,CURRENCY_TYPE,BACK_STAGE_URL,MONEY,GAMETYPE = loadConfig()
def userGoldControl(target_gold,userName = None,style=STYLE):
    if userName:
        add_gold(userName, target_gold=target_gold,style = style)
    else:
        with open('usedNum.log', 'r') as f:
            usedNum = f.readline()
        realUserName = 's' + str(usedNum)
        userName = str(style) + '_' + realUserName
        add_gold(userName, target_gold=target_gold,style=style)

def add_gold(userName,target_gold,style = '1',actionType = '3'):
    try:
        currentGold = logAnalysisUtil.get_user_gold_by_userName(userName)
        target_gold = int(target_gold)
        money = round(target_gold - currentGold,2)
    except:
        money = target_gold
    data = dict(userName=userName, style=str(style), num=str(money), moneyType="1", actionType=actionType)
    print(data)
    url = "http://192.168.10.213:8082"
    record = logAnalysisUtil.Record('admin', '123456', '', '', '')
    record.AddGold(data, url=url,style = style)
def main():
    userNames = {1377700: '241_s12349', 1376940: '241_s12350', 1902536: '241_s12351', 2818724: '241_s12352'}
    for userName in userNames.values():
        userGoldControl(userName=userName, target_gold = 16,style=STYLE)
if __name__ == '__main__':
    main()