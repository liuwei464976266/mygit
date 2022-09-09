# -*- coding: UTF-8 -*-
import itertools
import json
import time


def cc():
    c = []
    for i in itertools.combinations_with_replacement(range(1, 7), 2):
        # a = (''.join(i))
        c.append(i)
    print(c)

    a = [[i, x] for i in range(1, 7) for x in range(1, 7) if i <= x]
    print(a)

    h = []
    j = []
    k = []

    for i in a:
        if sum(i) in [1, 3, 5, 7, 9, 11]:
            h.append(i)

        elif sum(i) in [2, 6, 10]:
            j.append(i)

        else:
            k.append(i)

    print('奇数对换', h)
    print('2/6/10逆时针', j)
    print('4/8/12顺时针', k)


# wan = [x for x in range(1, 10)]
# tiao = [x for x in range(11, 20)]
# tong = [x for x in range(21, 30)]
#
# print(wan)
# print(tiao)
# print(tong)


# a = 6
# b = 14
# c = []
# for i in range(2):
#     c.append(a-i)
# print(c)
d = 0

#
# for i in itertools.combinations(range(1, 55), 5):
#     d += 1
#     print(f'第{d}局', i)

# a = [[i, x] for i in range(1, 7) for x in range(1, 7) if i <= x]
# jiang = [11,22,33,44,55,66,77,88,99,110,220,330,440,550,660,770,880,990]
# san = ['w123','w234',]
# while True:
#     a = input("请输入")
#     print(a)
#     print(type(a))
#     print(json.dump(a))
