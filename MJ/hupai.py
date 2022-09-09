# -*- coding: UTF-8 -*-
# 胡牌算法
##万：1-9
##条：11-19
##饼：21-29

def hupaiAlgorithm(handStr):
    a = handStr[:]
    # 牌数检查。
    if len(a) % 3 != 2:
        # print('和牌失败：牌数不正确。')
        return False

    # 是否有对子检查。
    double = []
    for x in set(a):
        if a.count(x) >= 2:
            double.append(x)
    # print(double)
    if len(double) == 0:
        # print('和牌失败：无对子')
        return False

    # 7对子检查（由于不常见，可以放到后面进行判断）
    # 对子的检查，特征1：必须是14张；特征2:一个牌型，有2张，或4张。特别注意有4张的情况。

    qidui = True
    if len(a) == 14:
        for x in set(a):
            if a.count(x) not in [2, 4]:
                qidui = False
                break
    else:
        qidui = False

    if qidui:
        # print("和牌,七对!!!")
        return True

        # 常规和牌检测。
    a1 = a.copy()
    a2 = []  # a2用来存放和牌后分组的结果。
    for x in double:
        # print('double',x)
        # print(a1[0] in a1 and (a1[0]+1) in a1 and (a1[0]+2) in a1)
        a1.remove(x)
        a1.remove(x)
        a2.append((x, x))
        for i in range(int(len(a1) / 3)):
            # print('i-',i)
            if a1.count(a1[0]) == 3:
                # 列表移除，可以使用remove,pop，和切片，这里切片更加实用。
                a2.append((a1[0],) * 3)
                a1 = a1[3:]
                # print(a1)
            elif a1[0] in a1 and a1[0] + 1 in a1 and a1[
                0] + 2 in a1:  # 这里注意，11,2222,33，和牌结果22,123,123，则连续的3个可能不是相邻的。
                a2.append((a1[0], a1[0] + 1, a1[0] + 2))
                a1.remove(a1[0] + 2)
                a1.remove(a1[0] + 1)
                a1.remove(a1[0])
                # print(a1)

            else:
                a1 = a.copy()
                a2 = []
                # print('重置')
                break
        else:
            # print('和牌成功,结果：',a2)
            return True

    # 如果上述没有返回和牌成功，这里需要返回和牌失败。
    else:
        # print('和牌失败：遍历完成。')
        return False