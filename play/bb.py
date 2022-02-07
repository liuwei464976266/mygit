#encoding:utf-8
from queue import Queue

import datetime
import json
import requests
import threading
import time


class Procuder(threading.Thread):
    def __init__(self,response_queue,tokenid,betScore,*args,**kwargs):#重写init方法
        super(Procuder, self).__init__(*args , **kwargs)
        self.response_queue = response_queue
        self.tokenid = tokenid
        self.betScore = betScore
    def run(self):
        while True:#死循环，一直调用接口
            self.parse_url(self.tokenid)
    def parse_url(self,tokenid):
        url = "http://192.168.10.25:8001/api/UserCore/callLotteryV2"
        millis = int(round(time.time() * 1000))
        data = {
            "tk": tokenid,
            "gt": 129,
            "timestamp": millis,
            "betScore": self.betScore
        }
        data = json.dumps(data)
        try:
            response = requests.post(url, data=data)
            response = response.json()
            self.response_queue.put(response)#将响应放入queue里
            print(threading.current_thread())
        except Exception as e:
            times = datetime.datetime.now()
            print(str(times) + str(e) + "\n")
            with open("orderId.txt", "a") as f:
                f.write(str(times) + str(e) + "\n")
class Consumer(threading.Thread):
    def __init__(self,response_queue,betScore,*args,**kwargs):
        super(Consumer, self).__init__(*args , **kwargs)
        self.response_queue = response_queue
        self.betScore = betScore
    def run(self):
        award_dic = {#type和赔率构成的字典
            1:0,
            2:15,
            3:10,
            4:9,
            5:8,
            6:7,
            7:6,
            8:5,
            9:4,
            10:3,
            11:2,
            12:1,
            13:0.2,
        }
        while True:
            if not self.response_queue.empty():#queue不为空
                response = self.response_queue.get()#从queue里取出response
                if response.get("code") == 20000:#判断code是否为20000
                    et = response.get("et")
                    areaNum = et.get("areaNum")
                    order_data = et.get("data")
                    order_type = self.get_type(order_data)
                    awardAmount = et.get("awardAmount")
                    gold = et.get("gold")
                    orderId = et.get("orderId")
                    with open("orderId.txt","a") as f:
                        f.write(str(orderId) + "," + str(areaNum) + "," + str(order_data) + "\n")
                    model = et.get("Model")
                    pointer = model.get("Pointer")
                    point_list = model.get("Queue")
                    # account = 0
                    # for i in point_list:
                    #     if i == 1:
                    #         account -= self.betScore
                    #     else:
                    #         account = account - self.betScore + award_dic.get(i) * self.betScore
                    #     if account < 0:
                    #         with open("ErrorData.txt", "a") as f:
                    #             f.write("accountError" + str(point_list) + str(i) + "\n")
                    #         print("accountError" , str(point_list) , str(i))
                    if 'initial_point_list' not in dir():#第一次运行脚本initial_point_list未定义
                        initial_point_list = point_list
                    if pointer == 0:#如果到新的一轮 queue刷新
                        initial_point_list = point_list
                    if 'initial_pointer' not in dir():#第一次运行脚本initial_pointer未定义
                        initial_pointer = pointer
                    if 'initial_gold' not in dir():#第一次运行脚本initial_gold未定义
                        initial_gold = gold
                        award = award_dic.get(order_type) * self.betScore
                        current_gold = gold
                        if award != awardAmount:#返回awardAmount错误
                            with open("ErrorData.txt", "a") as f:
                                f.write("GoldError" + "," + str(orderId) + "," + str(initial_gold) + "," + str(current_gold) + "," + str(gold) + "," + str(award) + "," + str(awardAmount) + "," + str(self.betScore) + "," + str(areaNum) +"\n")
                            print("GoldError", orderId, current_gold, gold, award, awardAmount, self.betScore,areaNum)
                    else:
                        award = award_dic.get(order_type) * self.betScore
                        if areaNum == 1:
                            current_gold = initial_gold - self.betScore + award
                        else:
                            current_gold = initial_gold + award
                        if award != awardAmount or current_gold != gold:#返回awardAmount错误或筹码计算错误
                            with open("ErrorData.txt", "a") as f:
                                f.write("GoldError" + "," + str(orderId) + "," + str(initial_gold) + "," + str(current_gold) + "," + str(gold) + "," + str(award) + "," + str(awardAmount) + "," + str(self.betScore)+","+str(areaNum)+"\n")
                            print("GoldError", orderId, current_gold, gold, award, awardAmount,self.betScore,areaNum)
                    initial_gold = gold
                    print(threading.current_thread()) #order_data, areaNum, order_type, gold,current_gold,awardAmount,award, pointer,initial_pointer,point_list,initial_point_list)
                    if self.check_Queue(point_list) == False or len(point_list) != 2012 or point_list[pointer] != areaNum or initial_point_list != point_list or (pointer - initial_pointer) > 1:#如果queue长度不等于2012或queue里元素不符合需求文档或前后两局queue不一致或本局开奖点不等于实际开奖点或pointer不连续增长
                        with open("ErrorData.txt", "a") as f:
                            f.write("PointError" + ",局号为" + str(orderId) + ",列表检查" + str(self.check_Queue(point_list)) + ",列表长度" + str(len(point_list)) + ",列表元素" + str(point_list[pointer]) + ",开奖点类型" + str(areaNum) + ",上局pointer" + str(initial_pointer) + ",本局pointer" + str(pointer) + "\n")
                        print("PointError", orderId, order_data, areaNum, order_type)
                    # with open("ErrorData.txt", "a") as f:
                    #     f.write(str(threading.current_thread()) + ",局号为" + str(orderId) + ",上局pointer" + str(initial_pointer) + ",本局pointer" + str(pointer) + "\n")
                    if pointer != 0:#纪录本局queue，留作与下局queue对比
                        initial_point_list = point_list
                    if pointer != 2011:
                        initial_pointer = pointer + 1
                    else:
                        initial_pointer = 0
                    if order_type != areaNum:
                        with open("ErrorData.txt", "a") as f:
                            f.write("TypeError" + "," + str(orderId) + "," + str(order_data) + "," + str(
                                areaNum) + "," + str(order_type) + "\n")
                        print("TypeError", orderId, order_data, areaNum, order_type)
                else:#返回code不等于20000
                    with open("ErrorData.txt", "a") as f:
                        f.write(str(response).replace("{", '').replace("}", '') + "\n")
                    print("CodeError", response)
    def get_type(self,order_data):#判断开奖点类型
        if len(order_data) == 6:
            if self.chajinhua(order_data):
                return 2
            elif self.hongliubo(order_data):
                return 3
            elif self.biandijin(order_data):
                return 4
            elif self.heiliubo(order_data):
                return 5
            elif self.wuhong(order_data):
                return 6
            elif self.wuzi(order_data):
                return 7
            elif self.sihong(order_data):
                return 8
            elif self.duitang(order_data):
                return 9
            elif self.sanhong(order_data):
                return 10
            elif self.sijin(order_data):
                return 11
            elif self.erju(order_data):
                return 12
            elif self.yiju(order_data):
                return 13
            else:
                return 1
        else:
            return 0

    def chajinhua(self,order_data):#插金花
        num_4 = order_data.count(4)
        num_1 = order_data.count(1)
        if num_4 == 4 and num_1 == 2:
            return True
        return False

    def hongliubo(self,order_data):#红六勃
        num_4 = order_data.count(4)
        if num_4 == 6:
            return True
        return False

    def biandijin(self,order_data):#遍地锦
        num_1 = order_data.count(1)
        if num_1 == 6:
            return True
        return False

    def heiliubo(self,order_data):#黑六勃
        no1 = order_data[0]
        if no1 != 1 and no1 != 4:
            num_no = order_data.count(no1)
            if num_no == 6:
                return True
        return False

    def wuhong(self,order_data):#五红
        num_4 = order_data.count(4)
        if num_4 == 5:
            return True
        return False

    def wuzi(self,order_data):#五子
        no1 = order_data[0]
        no6 = order_data[-1]
        num_no1 = order_data.count(no1)
        num_no6 = order_data.count(no6)
        if num_no1 == 5 and num_no1 != 4:
            return True
        elif num_no6 == 5 and num_no6 != 4:
            return True
        return False

    def sihong(self,order_data):#四红
        num_4 = order_data.count(4)
        num_1 = order_data.count(1)
        if num_4 == 4 and num_1 != 2:
            return True
        return False

    def duitang(self,order_data):#对堂
        num_4 = order_data.count(4)
        num_1 = order_data.count(1)
        num_2 = order_data.count(2)
        num_3 = order_data.count(3)
        num_5 = order_data.count(5)
        num_6 = order_data.count(6)
        if num_1 == num_2 == num_3 == num_4 == num_5 == num_6 == 1:
            return True
        return False

    def sanhong(self,order_data):#三红
        num_4 = order_data.count(4)
        if num_4 == 3:
            return True
        return False

    def sijin(self,order_data):#四进
        frequencies = {}
        for num in order_data:
            if num not in frequencies:
                frequencies[num] = 1
            else:
                frequencies[num] += 1
        for key, value in frequencies.items():
            if value == 4 and key != 4:
                return True
        return False

    def erju(self,order_data):#二举
        num_4 = order_data.count(4)
        if num_4 == 2:
            return True
        return False

    def yiju(self,order_data):#一举
        num_4 = order_data.count(4)
        if num_4 == 1:
            return True
        return False
    def check_Queue(self,point_list):#判断开奖点列表是否符合需求文档说明
        if point_list.count(1) != 1182:
            return False
        if point_list.count(2) != 5:
            return False
        if point_list.count(3) != 5:
            return False
        if point_list.count(4) != 5:
            return False
        if point_list.count(5) != 5:
            return False
        if point_list.count(6) != 5:
            return False
        if point_list.count(7) != 5:
            return False
        if point_list.count(8) != 20:
            return False
        if point_list.count(9) != 30:
            return False
        if point_list.count(10) != 50:
            return False
        if point_list.count(11) != 100:
            return False
        if point_list.count(12) != 200:
            return False
        if point_list.count(13) != 400:
            return False
        return True

def main():
    response_queue1 = Queue()
    response_queue2 = Queue()
    response_queue3 = Queue()
    response_queue = [response_queue1,response_queue2,response_queue3]
    users = {
        "53352D31C77FB1E9214A231E575DF90894F1":1000,#tk和下注底注
        "9C459E2915849519C200390AE5CF02694EDD": 5000,
        "B4AECFF8A5A6999546549162394A4F972276": 20000
    }
    i = 0
    for key,value in users.items():
        tokenid = key
        betScore = value
        t = Procuder(response_queue[i], tokenid, betScore)#实例化生产者对象
        t.start()
        i += 1
    i = 0
    for key,value in users.items():
        betScore = value
        t = Consumer(response_queue[i], betScore)#实例化消费者对象
        t.start()
        i += 1
if __name__ == '__main__':
    main()


