import json
import random
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


def check_gold(bet_type, bet_score, bet_points, gold, odds, win_point):
    win_point_count = 0
    for bet_point in bet_points:
        if bet_point in win_point:
            win_point_count += 1
    expected_gold = odds[str(win_point_count)] * bet_score
    expected_gold = int(expected_gold)
    assert expected_gold == gold, "预期gold {} 与gold {} 不符".format(expected_gold, gold)


def get_odds(game_type, level, bet_point, response):
    et = response["et"]
    outer_odds = et["odds"]
    current_odds = {}
    for odds in outer_odds:
        if odds["gameType"] == game_type and odds["level"] == level:  # 定位到难度这个维度
            inner_odds = odds["odds"]
            for k, v in inner_odds.items():
                if k == str(len(bet_point)):
                    current_odds = v
    return current_odds


def check_ngold(ngold, last_ngold, gold, bet_score):
    assert last_ngold + gold - bet_score == ngold, "预期ngold {} 与ngold {} 不符".format(last_ngold + gold, ngold)


def check_refresh_seed(seed, last_seed):
    assert seed != last_seed, "两次seed一致 {} {}".format(seed, last_seed)


def check_initialize_response(quantity, server_seed_hash, init_client_seed, difficulty_type, nonce,
                              last_quantity, last_server_seed_hash, last_init_client_seed, last_difficulty_type,
                              last_nonce
                              ):
    assert quantity == last_quantity, "预期quantity {} 与last_quantity {} 不符".format(quantity, last_quantity)
    # assert init_client_seed == last_init_client_seed
    assert difficulty_type == last_difficulty_type
    # assert nonce == last_nonce


def main():
    ip_address = "192.168.10.25"
    port = "9008"
    gt = 151
    tk = loginBobao.register_user()
    for i in range(10000):
        bet_score = random.randint(100, 5000)
        bet_type = random.randint(0, 2)
        bet_type = 0
        bet_point = random.sample(range(1, 41), random.randint(1, 3))
        if i == 0:
            response = call_initialize(ip_address, port, tk, gt)
        response = get_slot_data(ip_address, port, tk, gt, bet_score, bet_type, bet_point)
        print(response)
        if response.get("code", 0) == 20000:
            et = response.get("et", 0)
            gold = et.get("gold", 0)
            data = et.get("data", 0)
            ngold = et.get("nGold", 0)
            order_id = data.get("orderId", 0)
            win_points = data.get("winPoints", 0)
            client_seed = data.get("clientSeed", 0)
            server_seed_hash = data.get("serverSeedHash", 0)
            nonce = data.get("nonce", 0)

            # refresh_seed(ip_address, port, tk, gt)
            response = call_initialize(ip_address, port, tk, gt)
            if response.get("code", 0) == 20000:
                print("call_initialize", response)
                # print(response)
                # exit(-1)
                quantity = response["et"]["quantity"]
                init_server_seed_hash = response["et"]["serverSeedHash"]
                init_client_seed = response["et"]["clientSeed"]
                difficulty_type = response["et"]["type"]
                init_nonce = response["et"]["nonce"]
                odds = get_odds(gt, bet_type, bet_point, response)
            else:
                return
            check_gold(bet_type, bet_score, bet_point, gold, odds, win_points)
            if i == 0:
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
# x = [[a, b] for a in (-1, 1) for b in (-1, 1)]
# print(x)
# print(len(x))
# for i in x:
#     sum_ = sum(i)
#     print(sum_)