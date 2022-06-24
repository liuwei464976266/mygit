import hashlib
import json
import random
from decimal import Decimal
import loginBobao, requests


def get_headers(tk):  # 获取一个通用请求头
    headers = {'token': tk,
               'Content-Type': 'application/json'}
    return headers


def get_url(ip_address, port, api):  # 通过ip 端口 api路径组装一个url
    host = "http://" + ip_address + ":" + port
    if host.endswith(r"/"):
        url = host + api
    else:
        url = host + r"/" + api
    return url


def call_initialize(ip_address, port, tk, gt):  # 初始化接口
    api = "callInitialize"
    init_url = get_url(ip_address, port, api)
    body = {"tk": tk, "gt": gt, "timestamp": "1654771679269"}
    headers = get_headers(tk)
    body = json.dumps(body)
    response = requests.post(url=init_url, data=body, headers=headers)
    response = response.json()
    return response


def refresh_seed(ip_address, port, tk, gt):  # 刷新客户端种子
    api = "refreshSeed"
    headers = get_headers(tk)
    refresh_url = get_url(ip_address, port, api)
    body = {"tk": tk, "gt": gt, "timestamp": "1654771679269"}
    body = json.dumps(body)
    response = requests.post(url=refresh_url, data=body, headers=headers)
    response = response.json()
    return response


def get_slot_data(ip_address, port, tk, gt, bet_score, bet_type, bet_point):
    api = "getSlotData"
    headers = get_headers(tk)
    get_slot_url = get_url(ip_address, port, api)
    body = {"tk": tk, "gt": gt, "timestamp": "1654771679269", "betScore": bet_score, "betType": bet_type,
            "data": {"betPoint": bet_point}}
    body = json.dumps(body)
    response = requests.post(url=get_slot_url, data=body, headers=headers)
    response = response.json()
    return response


def get_history(ip_address, port, tk, gt):
    api = "getHistory"
    headers = get_headers(tk)
    get_slot_url = get_url(ip_address, port, api)
    body = {"tk": tk, "gt": gt}
    body = json.dumps(body)
    response = requests.post(url=get_slot_url, data=body, headers=headers)
    response = response.json()
    return response


def check_gold(bet_score, gold, odds):
    expected_gold = int(Decimal(str(bet_score)) * Decimal(str(odds)))
    assert expected_gold == gold, "预期gold {} 与gold {} 不符".format(expected_gold, gold)


def get_odds(game_type, level, lottery, response):
    et = response["et"]
    outer_odds = et["odds"]
    current_odds = {}
    for odds in outer_odds:
        if odds["gameType"] == game_type and odds["level"] == level:  # 定位到难度这个维度
            inner_odds = odds["odds"]
            current_odds = inner_odds.get(str(lottery))
    return current_odds


def check_getslot_history(initialize, getslot, history):
    print("------------------")
    print(json.dumps(initialize))
    print(json.dumps(getslot))
    print(json.dumps(history))
    data = getslot.get('et').get("data").get("hashInfo").get("1")
    data1 = initialize.get("et")
    data2 = history["et"]['recent'][0]
    has_test(data2)
    for x, y in data.items():
        if x == 'serverSeed':
            break
        assert data1.get(x) == y

    for x, y in data.items():
        assert data2.get(x) == y


def check_getslot_initialize(getslot, initialize):
    data = getslot.get('et').get("data").get("hashInfo").get("2")
    data1 = initialize.get("et")
    for x, y in data.items():
        if x == 'serverSeed':
            break
        assert data1.get(x) == y


def has_test(seed):
    # seed = response['et']['recent'][0]
    c = seed['serverSeed']+":"+seed["clientSeed"]+":"+seed["nonce"]+":"+seed["winPoint"]
    serverSeedHash = seed["serverSeedHash"]
    s = hashlib.sha256()
    s.update(c.encode())
    b = s.hexdigest()
    assert b == serverSeedHash, "seed合成错误"


def check_lottery(lottery, wintype):
    assert lottery == wintype, f"预期lottery {lottery} 与wintype {wintype} 不符"


def check_ngold(ngold, last_ngold, gold, bet_score):
    assert last_ngold + gold - bet_score == ngold or last_ngold + gold - bet_score + 1 == ngold, "预期ngold {} 与ngold {} 不符".format(
        last_ngold + gold - bet_score, ngold)


def check_refresh_seed(seed, last_seed):
    assert seed != last_seed, "两次seed一致 {} {}".format(seed, last_seed)


def check_initialize_response(quantity, server_seed_hash, init_client_seed, difficulty_type, nonce,
                              last_quantity, last_server_seed_hash, last_init_client_seed, last_difficulty_type,
                              last_nonce
                              ):
    assert quantity == last_quantity, "预期quantity {} 与last_quantity {} 不符".format(quantity, last_quantity)
    # assert init_client_seed == last_init_client_seed, f"预期init_client_seed {init_client_seed} 与last_init_client_seed {last_init_client_seed} 不符"
    # assert difficulty_type == last_difficulty_type
    # assert nonce == last_nonce


def main():
    # global init
    lottery_point = [[0, 0, 0], [0, 0, 1], [0, 0, 2], [0, 1, 2], [0, 1, 1], [0, 2, 2], [1, 1, 2], [1, 1, 1], [1, 2, 2],
                     [2, 2, 2]]
    ip_address = "192.168.10.25"
    port = "9008"
    gt = 154
    tk = loginBobao.register_user()

    for i in range(200000):
        bet_score = random.randint(100, 10000)
        bet_type = random.randint(0, 2)
        bet_type = 0
        bet_point = random.sample(range(1, 37), 3)
        if i == 0:
            response = call_initialize(ip_address, port, tk, gt)
            init = response
            # print("call_initialize", init)
        response = get_slot_data(ip_address, port, tk, gt, bet_score, bet_type, bet_point)
        get = response
        # print("getslot", get)
        his = get_history(ip_address, port, tk, gt)
        # print("history", his)
        check_getslot_history(init, get, his)
        if response.get("code", 0) == 20000:
            et = response.get("et", 0)
            gold = et.get("gold", 0)
            data = et.get("data", 0)
            ngold = et.get("nGold", 0)
            order_id = data.get("orderId", 0)
            wintype = data.get("winType", 0)
            hashInfo = data.get("hashInfo", 0)
            win_points = data.get("winPoints", 0)
            client_seed = hashInfo.get("1", 0).get("clientSeed", 0)
            server_seed_hash = data.get("serverSeedHash", 0)
            nonce = data.get("nonce", 0)
            win_ps = sorted([win_points[x - 1] for x in bet_point])  # 开奖点组合
            lottery = lottery_point.index(win_ps) + 1
            print(win_ps)
            # refresh_seed(ip_address, port, tk, gt)
            response = call_initialize(ip_address, port, tk, gt)
            init = response
            if response.get("code", 0) == 20000:
                check_getslot_initialize(get, init)
                quantity = response["et"]["quantity"]
                init_server_seed_hash = response["et"]["serverSeedHash"]
                init_client_seed = response["et"]["clientSeed"]
                difficulty_type = response["et"]["type"]
                init_nonce = response["et"]["nonce"]
                odds = get_odds(gt, bet_type, lottery, response)
            else:
                return

            check_gold(bet_score, gold, odds)
            check_lottery(lottery, wintype)
            if  i == 0:
                last_ngold = ngold
                last_seed = client_seed
            else:
                check_ngold(ngold, last_ngold, gold, bet_score)
                last_ngold = ngold
                check_refresh_seed(client_seed, last_seed)
                last_seed = client_seed
            last_quantity = bet_score
            last_server_seed_hash = server_seed_hash
            last_init_client_seed = client_seed
            last_difficulty_type = bet_type
            last_nonce = nonce
            check_initialize_response(quantity, init_server_seed_hash, init_client_seed, difficulty_type, init_nonce,
                                      last_quantity, last_server_seed_hash, last_init_client_seed,
                                      last_difficulty_type,
                                      last_nonce
                                      )
        else:
            return


if __name__ == '__main__':
    main()
