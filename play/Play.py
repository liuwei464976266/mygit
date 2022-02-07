import requests


class Game:

    def __init__(self, tk, sleep, gametype):
        self.tk = tk
        self.gamtype = gametype
        self.url = "http://192.168.10.25:8001//api/UserCore/CallLotteryModel"  # 小游戏接口
        self.HL_url = "http://43.231.7.174:8001//api/UserCore/CallLotteryFree"  # 红利接口
        self.U_gold = "http://192.168.10.25:8001/api/UserCore/AddPlayerGold"  # 金币接口
        self.U_one = "http://192.168.10.25:8001//api/usercore/CallLotteryRoteRow"  # 单次旋转接口
        self.U_one_data = {}
        self.U_data = {"tk": self.tk,
                       "gt": gametype,
                       "betScore": "3000",
                       "timestamp": "15976259898985"
                       }
        self.Ug_data = {"tk": self.tk, "type": 1, "gold": 10000000,
                        "timestamp": "1600914417600"}
        self.HL_data = {}
        self.sleep = sleep

    def speak(self):
        print(self.tk, self.url)

    def write(self):
        with open(r'E:\金流\log.txt', 'a')as f:
            f.write(self.log + '\n' * 2)

    def post(self, circulate=False):
        try:
            post = requests.post(self.url, json=self.U_data, timeout=self.sleep)
            while circulate:
                post = requests.post(self.url, json=self.U_data, timeout=self.sleep)
                self.log = post.text

            return post.text
        except Exception as e:
            print(e)

    def post_HL(self):
        try:
            post = requests.post(self.HL_url, json=self.HL_data, timeout=self.sleep)
            return post.text

        except Exception as e:
            print(e)

    def post_gold(self):
        post = requests.post(self.U_gold, json=self.Ug_data, timeout=self.sleep)
        self.log = post.text
        print(self.log)

    def only_one(self):
        try:
            post = requests.post(self.U_one, json=self.U_one_data, timeout=self.sleep)
            self.log = post.text
            return post.text

        except Exception as e:
            print(e)



if __name__ == '__main__':
    list_Id = ['EF51C6643384A024915589A039F53664F0E4',
               'BCF0579533CACBDEF5A81BE959062F93DEB4',
               'EF564D5DF8BAC1B627A427E19A8B49038FB5',
               'BA889F7DDA9EEABA8F78FD113F1A9D159503',
               '5D8D5117ED6E29453950152AFDBCB0675479',
               '659CB6F2B4066B902D3EED9D4130D69F0938',
               '38F6112BC230DB14121E170C7B7804F7CA3E',
               ]

    # dic = {}
    # for i in range(5):
    #     dic['ma'+str(i)] = Game(list_Id[i], 5, 135)

    # dic['ma0'].post()
    # print(dic['ma0'].log)
    # ma = Game(list_Id[0], 5, 135)
    # print(ma)
    ma = Game(list_Id[1], 5, 135)
    for i in range(1):
        a = ma.only_one()
        print(a)

    # print(ma.U_data)
    # for i in range(30):
    #     threading.Thread(ma.post())
    #
    #     print(ma.log)
    # ma.U_data['gametype'] = 132
    # print(ma.U_data)
    # ma.post()
    # print(ma.log)

    # ma.post()
    #
    # # ma.write()

    # print(type(ma.U_data))
