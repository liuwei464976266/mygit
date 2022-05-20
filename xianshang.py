import json

import requests


def adc(game):
    url = 'http://18.167.1.28:8056/api/values/betDetail'
    headers = {'Accept': '*/*',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Connection': 'keep-alive',
               'Content-Length': '94',
               'Content-Type': 'application/json',
               }

    data = {
        "style": 2,
        "pageIndex": 1,
        "pageSize": 200,
        "startTime": "2022-05-12 12:00:00",
        "endTime": "2022-05-12 13:50:59",
        "gameType": game
    }
    response = requests.post(url, headers=headers, json=data)
    response = response.text
    # print(response)
    return response


a = {
    # 2: "抢庄牛牛",
    30: "炸金花",
    31: "推筒子",
    32: "三公",
    33: "牌九",
    34: "百人牛牛",
    36: "通比牛牛",
    37: "极速炸金花",
    38: "二十一点",
    39: "十三水",
    41: "德州扑克",
    43: "新版斗牛",
    45: "欢乐炸金花",
    46: "港式梭哈",
    47: "红黑大战",
    48: "炸金牛",
    54: "血战骰宝",
    56: "赌场扑克",
    58: "百人骰宝",
    # 59: "百得之",
    125: "不朽情缘",
    126: "花花公子",
    130: "东方珍兽",
    131: "比基尼派对",
    132: "舞龙",
    133: "宝石转轴",
    134: "燃烧的欲望",
    135: "招财鞭炮",
    136: "幸运富豪",
    141: "篮球巨星",
    142: "幸运龙宝贝",
    143: "奇妙马戏团",
    144: "迷失拉斯维加斯",
    145: "爆破银行",
    200: "鱼虾蟹",
    201: "猜丁壳",
    202: "俄罗斯轮盘"
}
for i in a:
    print(i, a[i])
    data = json.loads(adc(i))
    Data = data['Data']
    for x in Data:
        print(x['roundId'], x)

