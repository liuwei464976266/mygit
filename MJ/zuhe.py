# -*- coding: UTF-8 -*-
import itertools


def cc():
    c = []
    for i in itertools.combinations_with_replacement(range(1, 7), 2):
        # a = (''.join(i))
        ci = sum(i) % 4
        sit = ''
        if ci == 0:
            sit = '南'
        elif ci == 1:
            sit = '东'
        elif ci == 2:
            sit = '北'
        elif ci == 3:
            sit = '西'
        # print(i, ci, sit)
        c.append(i)
        # c.append(sit)
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

cc()
