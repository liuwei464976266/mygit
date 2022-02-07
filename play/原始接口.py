import os, sys, json, copy
import requests
import redis
import time
import threading

Max = [(),
       (1, [(3, 0.08), (4, 0.48), (5, 4)]),
       (2, [(3, 0.08), (4, 0.48), (5, 4)]),
       (3, [(3, 0.16), (4, 0.8), (5, 6)]),
       (4, [(3, 0.16), (4, 0.8), (5, 6)]),
       (5, [(3, 0.2), (4, 1.2), (5, 8)]),
       (6, [(3, 0.2), (4, 1.2), (5, 8)]),
       (7, [(3, 0.4), (4, 4), (5, 20)]),
       (8, [(3, 0.6), (4, 6), (5, 40)]),
       (9, [(3, 0.8), (4, 0.8), (5, 80)]),
       (10, [(2, 1.3), (3, 5.9), (4, 59), (5, 590)]),
       (11, [(2, 1), (3, 2), (4, 10), (5, 100)]),
       ]

WILD = [12]

threadLock = threading.Lock()


def getColsSymbol(points):  # 取出各列中奖位置
    symbol13_list = []
    col1, col2, col3, col4, col5 = {}, {}, {}, {}, {}
    for i in range(len(points)):
        if points[i] == 11:
            symbol13_list.append(i)
        elif i % 5 == 0:
            col1[i] = points[i]
        elif i % 5 == 1:
            col2[i] = points[i]
        elif i % 5 == 2:
            col3[i] = points[i]
        elif i % 5 == 3:
            col4[i] = points[i]
        elif i % 5 == 4:
            col5[i] = points[i]
    return col1, col2, col3, col4, col5, symbol13_list


def checkAwardSymbol(points):  # 核对adpoints
    col1, col2, col3, col4, col5, symbol13_list = getColsSymbol(points)
    adpoints = {}
    for col1_key, col1_value in col1.items():
        if col1_value not in adpoints.keys():  # 字典里没有该符号
            if col1_value not in WILD:
                for col2_key, col2_value in col2.items():
                    if col1_value == col2_value or col2_value in WILD:
                        for col3_key, col3_value in col3.items():
                            if col1_value == col3_value or col3_value in WILD:
                                try:
                                    adpoints[col1_value].append(col1_key)
                                except:
                                    adpoints[col1_value] = [col1_key]
                                adpoints[col1_value].append(col2_key)
                                adpoints[col1_value].append(col3_key)
                                '''10号2连'''
                            elif col1_value == 10:
                                try:
                                    adpoints[col1_value].append(col1_key)
                                except:
                                    adpoints[col1_value] = [col1_key]
                                adpoints[col1_value].append(col2_key)
            else:
                for col2_key, col2_value in col2.items():
                    if (col1_value == col2_value) or (col2_value in WILD):
                        for col3_key, col3_value in col3.items():
                            try:
                                adpoints[col3_value].append(col1_key)
                            except:
                                adpoints[col3_value] = [col1_key]
                            adpoints[col3_value].append(col2_key)
                            adpoints[col3_value].append(col3_key)
                    else:
                        for col3_key, col3_value in col3.items():
                            if (col2_value == col3_value) or (col3_value in WILD):
                                try:
                                    adpoints[col2_value].append(col1_key)
                                except:
                                    adpoints[col2_value] = [col1_key]
                                adpoints[col2_value].append(col2_key)
                                adpoints[col2_value].append(col3_key)
        else:
            if col1_value not in WILD:
                adpoints[col1_value].append(col1_key)
    temAdpoints = copy.deepcopy(adpoints)
    for key, value in temAdpoints.items():
        if 2 in value or 7 in value or 12 in value:
            for col4_key, col4_value in col4.items():
                if key == col4_value or col4_value in WILD:
                    adpoints[key].append(col4_key)
                for col5_key, col5_value in col5.items():
                    if key in WILD:
                        if col4_value in WILD and col5_value not in WILD:
                            try:
                                adpoints[col5_value].append(col5_key)
                            except:
                                adpoints[col5_value] = [col5_key]
                            adpoints[col5_value].append(col4_key)
                            adpoints[col5_value] += value
                        if (col4_value not in WILD) and (col5_value == col4_value or col5_value in WILD):
                            try:
                                adpoints[col4_value].append(col4_key)
                            except:
                                adpoints[col4_value] = [col4_key]
                            adpoints[col4_value].append(col5_key)
                            adpoints[col5_value] += value
                        if (col4_value not in WILD) and (col5_value != col4_value and col5_value not in WILD):
                            try:
                                adpoints[col4_value].append(col4_key)
                            except:
                                adpoints[col4_value] = [col4_key]
                            adpoints[col4_value] += value
                    if key == col4_value or col4_value in WILD:
                        adpoints[key].append(col4_key)
                        if key == col5_value or col5_value in WILD:
                            adpoints[key].append(col5_key)
    for key, value in adpoints.items():
        if len([x for x in adpoints[key] if x in col5.keys()]) > 0:
            for col1_key, col1_value in col1.items():
                if col1_value in WILD:
                    adpoints[key].append(col1_key)
            for col2_key, col2_value in col2.items():
                if col2_value in WILD:
                    adpoints[key].append(col2_key)
            for col3_key, col3_value in col3.items():
                if col3_value in WILD:
                    adpoints[key].append(col3_key)
            for col4_key, col4_value in col4.items():
                if col4_value in WILD:
                    adpoints[key].append(col4_key)
            for col5_key, col5_value in col5.items():
                if col5_value in WILD:
                    adpoints[key].append(col5_key)
        elif len([x for x in adpoints[key] if x in col4.keys()]) > 0:
            for col1_key, col1_value in col1.items():
                if col1_value in WILD:
                    adpoints[key].append(col1_key)
            for col2_key, col2_value in col2.items():
                if col2_value in WILD:
                    adpoints[key].append(col2_key)
            for col3_key, col3_value in col3.items():
                if col3_value in WILD:
                    adpoints[key].append(col3_key)
            for col4_key, col4_value in col4.items():
                if col4_value in WILD:
                    adpoints[key].append(col4_key)
        elif len([x for x in adpoints[key] if x in col3.keys()]) > 0:
            for col1_key, col1_value in col1.items():
                if col1_value in WILD:
                    adpoints[key].append(col1_key)
            for col2_key, col2_value in col2.items():
                if col2_value in WILD:
                    adpoints[key].append(col2_key)
            for col3_key, col3_value in col3.items():
                if col3_value in WILD:
                    adpoints[key].append(col3_key)
        adpoints[key] = list(set(value))
    if len(symbol13_list) >= 2:
        adpoints[11] = symbol13_list
    my_adpoints = {}
    for key, value in adpoints.items():
        my_adpoints[str(key)] = value
    cc = checkLinePoints(my_adpoints, points)
    return cc


def checkLinePoints(adpoints, points):  # 核对LinePoints，具体赢赏分线
    Myalllines = {}
    myadpoints = copy.deepcopy(adpoints)  # 拷贝一个 myadpoints 避免后续直接修改adpoints对象
    for key, value in myadpoints.items():
        if key != '11':
            col1, col2, col3, col4, col5 = [], [], [], [], []
            for i in value:
                if i % 5 == 0:
                    col1.append(i)
                elif i % 5 == 1:
                    col2.append(i)
                elif i % 5 == 2:
                    col3.append(i)
                elif i % 5 == 3:
                    col4.append(i)
                elif i % 5 == 4:
                    col5.append(i)
            if len(col5) > 0:
                mylinepoints = [[a, b, c, d, e] for a in col1 for b in col2 for c in col3 for d in col4 for e in col5]
            elif len(col4) > 0:
                mylinepoints = [[a, b, c, d] for a in col1 for b in col2 for c in col3 for d in col4]
            elif len(col3) > 0:
                mylinepoints = [[a, b, c] for a in col1 for b in col2 for c in col3]
            elif len(col2) > 0:
                mylinepoints = [[a, b] for a in col1 for b in col2]
            else:
                mylinepoints = []

            removeLines = []
            for i in mylinepoints:
                if len([x for x in i if points[x] not in WILD]) <= 0 and key != '12':
                    removeLines.append(i)
            for i in removeLines:
                mylinepoints.remove(i)
            Myalllines[key] = {str(len(mylinepoints[0])): len(mylinepoints)}
            # Myalllines[key] = mylinepoints
        else:
            Myalllines[key] = {str(len(value)): 1}
    return Myalllines


def Add():
    for i in range(15000):
        object = requests.get('http://192.168.10.25:8001/api/usercore/CallUrl').text
        print(object)
        time.sleep(0.1)
        threadLock.acquire()  # 加锁
        r.lpush(f'GameHistory{ti}', object)
        threadLock.release()  # 释放锁


def Addfree():
    for i in range(15000):
        object = requests.get('http://192.168.10.25:8001/api/usercore/CallFreeUrl').text
        print(object)
        time.sleep(0.1)
        threadLock.acquire()  # 加锁
        rs.lpush(f'GameFree{ti}', object)
        threadLock.release()  # 释放锁


def yy():
    li = (r.lrange('GameHistory' + ti, 0, 150000))
    lis = (rs.lrange('GameFree' + ti, 0, 150000))
    MyAllLines = {}
    for i in lis:
        x3 = json.loads(i)
        a = x3["list"]
        lis = a['1'] + a['2'] + a["3"]
        lis = [int(x) for x in lis]
        linePoints = checkAwardSymbol(lis)
        print(lis)
        for key, value in linePoints.items():
            if key not in MyAllLines.keys():
                MyAllLines[key] = value
            else:
                for key1, value1 in value.items():
                    if key1 not in MyAllLines[key]:
                        MyAllLines[key][key1] = value1
                    else:
                        MyAllLines[key][key1] += value1
        print('总和', MyAllLines)
    num = 0
    for x, y in MyAllLines.items():
        x = int(x)
        for x1, y1 in y.items():
            x1 = int(x1)
            print(x1, y1)
            if x == 11:
                num += (Max[x][1][x1 - 2][1]) * y1
            else:
                num += (Max[x][1][x1 - 3][1]) * y1
    num = round(num, 2)
    ratio = str(round((num / 150000), 2))
    r2.hset(f'ALLGameFree', ti + "__" + str(num) + "___" + ratio, str(MyAllLines))

    MyAllLines = {}
    for i in li:
        x3 = json.loads(i)
        a = x3["list"]
        lis = a['1'] + a['2'] + a["3"]
        lis = [int(x) for x in lis]
        linePoints = checkAwardSymbol(lis)
        print(lis)
        for key, value in linePoints.items():
            if key not in MyAllLines.keys():
                MyAllLines[key] = value
            else:
                for key1, value1 in value.items():
                    if key1 not in MyAllLines[key]:
                        MyAllLines[key][key1] = value1
                    else:
                        MyAllLines[key][key1] += value1
        print('总和', MyAllLines)
    num = 0
    for x, y in MyAllLines.items():
        x = int(x)
        for x1, y1 in y.items():
            x1 = int(x1)
            print(x1, y1)
            if x == 11:
                num += (Max[x][1][x1 - 2][1]) * y1
            else:
                num += (Max[x][1][x1 - 3][1]) * y1
    num = round(num, 2)
    ratio = str(round((num / 150000), 2))
    r2.hset(f'ALLGameHistory', ti + "__" + str(num) + "___" + ratio, str(MyAllLines))


def start():
    thread = []
    for i in range(10):
        a = threading.Thread(target=Add, args=())
        b = threading.Thread(target=Addfree, args=())
        thread.append(a)
        thread.append(b)
        a.start()
        b.start()
    for x in thread:
        x.join()
    yy()


if __name__ == '__main__':
    ti = time.strftime("%m-%d")
    pool = redis.ConnectionPool(host='localhost', password='123456', port=6379, decode_responses=True)
    r = redis.Redis(host='localhost', password='123456', port=6379, db=0, decode_responses=True)
    rs = redis.Redis(host='localhost', password='123456', port=6379, db=1, decode_responses=True)
    r2 = redis.Redis(host='localhost', password='123456', port=6379, db=2, decode_responses=True)
    start()
    # yy()