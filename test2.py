import requests, json, threading, time, random,datetime
import operator
from functools import reduce
from queue import Queue
import copy
GT = 131



def call(tk,gametype):
    url = "http://192.168.10.212:8002/callInitialize"
    data = {
            "gt":gametype,
            "timestamp": 45646545654,
            'actionType': '0'
            }
    headers = {
        'token': tk,
        'Content-Type': 'application/json'
        }
    data = json.dumps(data)
    response = requests.post(url=url, data=data, headers=headers)
    response = response.json()
    print("初始化", response)
def register():
    url = "http://192.168.10.82:8031/registerUser"
    headers = {
        'Content-Type': 'application/json'
    }
    registerResponse = requests.get(url, headers=headers)
    username = registerResponse.json().get("username")
    password = "123456"
    if username:
        print(username, password)
        return username, password
    return None
def getToken(username,password):
    data = {
            "userName": username,
            "password": password
    }
    headers = {
        'Content-Type': 'application/json'
    }
    data = json.dumps(data)
    url = "http://192.168.10.212:8002/callToken"
    tokenResponse = requests.post(url = url, data = data, headers = headers)
    token = tokenResponse.json().get("ms")
    print(token)
    if token:
        return token
    return None
def main():
    url = "http://192.168.10.82:8031/getSlotData"
    username, password = register()
    tk = getToken(username, password)
    tokenid = tk
    requests.get(f'http://192.168.10.212:8002/pay/{tk}/50000000')
    gameType = GT
    betScore = 25
    call(tokenid, gameType)
    data = {
        "gt": gameType,
        "timestamp": 45646545654,
        'actionType': 0,
        "betScore": 2500,

        }
    headers = {
        'token': tk,
        'Content-Type': 'application/json'
        }

    data = json.dumps(data)

    while True:
        response = requests.post(url=url, data=data, headers=headers).text
        # response = response.json()
        # nGold = response['et']['data']['nGold']
        print(username, response)


if __name__ == '__main__':
    for i in range(1):
        # print(i)
        threading.Thread(target=main).start()




