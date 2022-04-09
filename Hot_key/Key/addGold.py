import logAnalysisUtil,configparser,os
base_dir = os.path.dirname(__file__)
config_path = os.path.join(base_dir, 'login.config')
login_configFile_path = config_path
# login_configFile_path = 'login.config'
def loadConfig():
    cf = configparser.ConfigParser()
    cf.read(login_configFile_path)
    loginConfig = cf.options('config')
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
        result = add_gold(userName, target_gold=target_gold,style = style)
    else:
        with open('usedNum.log', 'r') as f:
            usedNum = f.readline()
        realUserName = 's' + str(usedNum)
        userName = str(style) + '_' + realUserName
        result = add_gold(userName, target_gold=target_gold,style=style)
    return result
def add_gold(userName,target_gold,style = '1',actionType = '3'):
    try:
        currentGold = logAnalysisUtil.get_user_gold_by_userName(userName)
        target_gold = int(target_gold)
        money = round(target_gold - currentGold,2)
    except:
        money = target_gold
    data = dict(userName=userName, style=str(style), num=str(money), moneyType="1", actionType=actionType)
    print(data)
    url = BACK_STAGE_URL
    print(url)
    record = logAnalysisUtil.Record('admin', '123456', '', '', '')
    return record.AddGold(data, url=url,style = style)


def main():
    userNames = {132316: '241_s12466'}
    target_gold = 500
    if isinstance(userNames, dict):
        for userName in userNames.values():
            userGoldControl(userName=userName, target_gold = target_gold,style=STYLE)
    elif isinstance(userNames, lsit):
        for userName in userNames:
            userGoldControl(userName=userName, target_gold = target_gold,style=STYLE)
if __name__ == '__main__':
    main()