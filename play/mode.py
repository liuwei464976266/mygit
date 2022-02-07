import json, threading, time
import requests
import queue


class Game:

    def __init__(self, tk, sleep, gametype):
        self.tk = tk
        self.gametype = gametype
        self.url = "http://192.168.10.25:8001//api/UserCore/CallLotteryModel"  # 小游戏接口
        self.HL_url = "http://43.231.7.174:8001//api/UserCore/CallLotteryFree"  # 红利接口
        self.U_gold = "http://192.168.10.25:8001/api/UserCore/AddPlayerGold"  # 金币接口
        self.U_one = "http://192.168.10.25:8001//api/usercore/CallLotteryRoteRow"  # 单次旋转接口
        self.U_data = {"tk": self.tk,
                       "gt": gametype,
                       "betScore": "3000",
                       "timestamp": "15976259898985"
                       }
        self.Ug_data = {"tk": self.tk, "type": 1, "gold": 10000000,
                        "timestamp": "1600914417600"}
        self.sleep = sleep

    def speak(self):
        print(self.tk, self.url)

    def write(self):
        with open(r'E:\金流\log.txt', 'a')as f:
            f.write(self.log + '\n' * 2)

    def post(self, circulate=False):
        global lx
        try:
            post = requests.post(self.url, json=self.U_data, timeout=self.sleep)
            while circulate:
                post = requests.post(self.url, json=self.U_data, timeout=self.sleep)
                self.log = post.text
            lx = post.text
            return lx
        except Exception as e:
            print(e)

    def post_HL(self):
        HL_data = {}
        try:
            post = requests.post(self.HL_url, json=HL_data, timeout=self.sleep)
            return post.text

        except Exception as e:
            print(e)

    def post_gold(self):

        post = requests.post(self.U_gold, json=self.Ug_data, timeout=self.sleep)
        self.log = post.text
        print(self.log)

    def only_one(self, RoteRow, ):

        one_data = {"tk": self.tk,
                    "gt": self.gametype,
                    "betScore": "3000",
                    "timestamp": 4645645,
                    "RoteRow": RoteRow,
                    'RoteKey': 'ddd'
                    }
        try:
            post = requests.post(self.U_one, json=one_data, timeout=self.sleep)
            return post.text

        except Exception as e:
            print(e)


if __name__ == '__main__':
    list_Id = ['BC8FB3F860173995CAB0BE68435A5AE95AB0',
               'BCF0579533CACBDEF5A81BE959062F93DEB4',
               'EF564D5DF8BAC1B627A427E19A8B49038FB5',
               'BA889F7DDA9EEABA8F78FD113F1A9D159503',
               '5D8D5117ED6E29453950152AFDBCB0675479',
               '659CB6F2B4066B902D3EED9D4130D69F0938',
               '38F6112BC230DB14121E170C7B7804F7CA3E',
               ]

    # dic = {}
    # for i in range(5):
    #     dic['object'+str(i)] = Game(list_Id[i], 5, 135)
    #     threading.Thread(target=dic['object'+str(i)].post, ).start()
    #     # print()



    ma = Game(list_Id[0], 5, 135)
    ma.post()
    print(ma.log)




    # print(ma.only_one(1))

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
