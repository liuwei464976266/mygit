# -*- coding: utf-8 -*-
# @Time     :2022/2/18 14:15
# @Author   :LuoLin01


class PmaJong(object):
    def __init__(self):
        self.m_TypeNum = []
        self.m_CardNum = []
        self.HasCouple = False
        for i in range(3):
            self.m_TypeNum.append(0)
            self.m_CardNum.append([0]*9)

        self.g_typedef = ['w', 't', 'd']  # 万、条、筒
        self.m_GangNum = 0

    def InitData(self, cards_str):
        if not len(cards_str) or len(cards_str) % 2:  # 必然是偶数才能判断是否完成
            print("数据初始化出错")
            return

        cur_idx = 0
        while cur_idx < len(cards_str):
            cur_c = cards_str[cur_idx]

            nNum = ord(cur_c) - ord('0')
            cType = cards_str[cur_idx + 1]
            for i in range(3):
                if cType == self.g_typedef[i]:
                    self.m_TypeNum[i] += 1
                    self.m_CardNum[i][nNum - 1] += 1
                    break

            cur_idx += 2

    def IsSevenCouple(self):
        if 14 == self.m_TypeNum[0] + self.m_TypeNum[1] + self.m_TypeNum[2]:
            for i in range(3):
                for j in range(9):
                    if self.m_CardNum[i][j] != 0 and self.m_CardNum[i][j] != 2:
                        return False

    def IsWin(self):
        if self.m_TypeNum[0] and self.m_TypeNum[1] and self.m_TypeNum[2]:
            print("不是缺一门\n")
            return False
        if self.IsSevenCouple():
            print("七小对\n")
            return True

        for i in range(3):
            if not self.IsOneTypeWin(self.m_CardNum[i], self.m_TypeNum[i], i):
                print("花色:%s不满足胡牌\n" % self.g_typedef[i])
                return False

        if not self.HasCouple:
            print("没有对子，不能胡牌\n")
            return False

        if self.m_TypeNum[0] + self.m_TypeNum[1] + self.m_TypeNum[2] - 14 != self.m_GangNum:
            print("你丫诈和，牌的数量不对.\n")
            return False

        print("正常胡牌\n")
        return True

    def IsOneTypeWin(self, pCards, Num, type):
        print(pCards)
        if not Num:
            return True
        tmp = ""
        for i in range(9):
            if pCards[i] >= 2 and not self.HasCouple:
                pCards[i] -= 2
                self.HasCouple = True
                if self.IsOneTypeWin(pCards, Num - 2, type):
                    tmp += str(i+1) + self.g_typedef[type] + str(i+1) + self.g_typedef[type]
                    print("当前牌：%s\n", tmp)
                    return True
                pCards[i] += 2
                self.HasCouple = False

            if pCards[i] == 4:
                pCards[i] -= 4
                if self.IsOneTypeWin(pCards, Num - 4, type):
                    self.m_GangNum += 1
                    tmp += (str(i + 1) + self.g_typedef[type]) * 4
                    print("当前牌：%s\n", tmp)
                    return True
                pCards[i] += 4

            if pCards[i] >= 3:
                pCards[i] -= 3
                if self.IsOneTypeWin(pCards, Num - 3, type):
                    tmp += (str(i + 1) + self.g_typedef[type]) * 3
                    print("当前牌：%s\n", tmp)
                    return True
                pCards[i] += 3

            if i < 7 and pCards[i] and pCards[i + 1] and pCards[i + 2]:
                pCards[i] -= 1
                pCards[i + 1] -= 1
                pCards[i + 2] -= 1
                if self.IsOneTypeWin(pCards, Num - 3, type):
                    tmp += str(i + 1) + self.g_typedef[type] + str(i + 2) + self.g_typedef[type] + str(i + 3) + self.g_typedef[type]
                    print("当前牌：%s\n", tmp)
                    return True
                pCards[i] += 1
                pCards[i + 1] += 1
                pCards[i + 2] += 1

        return False


if __name__ == "__main__":
    cur_s = "1w1w1w2d3d4d2w3w4w7d8d9d5w5w"
    mahJong = PmaJong()
    mahJong.InitData(cur_s)
    if mahJong.IsWin():
        print("win !!!!!")
    else:
        print("False !!!!!")


