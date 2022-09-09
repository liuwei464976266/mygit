# -*- coding: UTF-8 -*-
import itertools


def double():
    li = [
        '根',
        '杠上花',
        '杠上炮',
        '抢杠胡',
        '海底捞月',
        '门清',
        '中张',
        '夹心五',
        '自摸加番',
        '天胡',
        '地胡',
    ]
    d = 0

    for x in range(2, 8):
        print(f"{x}组数据")
        for i in itertools.combinations(li, x):
            d += 1
            if '天胡' in i and '抢杠胡' in i or '天胡' in i and '杠上炮' in i or '天胡' in i and '海底捞月' in i or '天胡' in i and '地胡' in i or '天胡' in i and '杠上花' in i or '天胡' in i and '根' in i:
                continue
            if '地胡' in i and '抢杠胡' in i or '地胡' in i and '海底捞月' in i or '地胡' in i and '根' in i or '地胡' in i and '杠上花' in i or '地胡' in i and '杠上炮' in i:
                continue
            if '自摸加番' in i and '抢杠胡' in i or '自摸加番' in i and '杠上炮' in i:
                continue
            if '杠上炮' in i and '杠上花' in i:
                continue
            if '抢杠胡' in i and '杠上炮' in i or '抢杠胡' in i and '杠上花':
                continue
            if '天胡' in i or '地胡' in i:
                fan = 3
                bei = (2 ** (len(i) - 1)) * 8
            else:
                fan = 1
                bei = 2 ** len(i)
            # sheet.cell(d, 1).value = i
            # sheet.cell(d, 2).value = fan
            # sheet.cell(d, 3).value = bei
            # print(i, "-", fan, "-", bei)
            # print(i)
            # print(fan)
            # print(bei)


def card_type():
    data = [
        '平胡',
        '对对胡',
        '清一色',
        '七对',
        '金钩钓',
        '龙七对',
        '幺九',
        '将对',
    ]
    for x in range(2, 9):
        print(f"{x}组数据")
        for i in itertools.combinations(data, x):
            if '平胡' in i and '幺九' not in i:
                continue
            if '对对胡' in i and '清一色' not in i or len(i)>2:
                continue
            if '七对' in i and '金钩钓' in i or '对对胡' in i and '七对' in i or '龙七对' in i and '七对' in i or '将对' in i and '七对' in i or '幺九' in i and '七对' in i:
                continue
            if '龙七对' in i and '金钩钓' in i or '金钩钓' in i and '幺九' in i or '金钩钓' in i and '将对' in i:
                continue
            if '幺九' in i and '龙七对' in i or '幺九' in i and '将对' in i:
                continue
            if '龙七对' in i and '将对' in i:
                continue
            print(i)


if __name__ == '__main__':
    card_type()
