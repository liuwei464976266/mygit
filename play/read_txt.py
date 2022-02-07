import re
text = open(r"E:\小游戏\07.log", "r")
a = text.read()

OrderId_list = re.findall('"OrderId":"(\d+)"', a)
OrderId_list = list(map(lambda x : x.replace(",", " "), OrderId_list))

Points_list = re.findall('"Points":\[([\d+,]+)', a)
print(Points_list)

AdPoints_list = re.findall('"(AdPoints":.*)"Plan', a)
LinePoints_list = re.findall('"(LinePoints":.*)"ApiPoints"', a)
LinePoints_list = list(map(lambda x: x.replace(",", " "), LinePoints_list))
AdPoints_list = list(map(lambda x: x.replace(",", " "), AdPoints_list))
# print(LinePoints_list)


# Points_list = list(map(lambda x:x.replace(",", ""), Points_list))
ApiPoints_list = re.findall('"ApiPoints":\[([\[\]\d+,]+)', a)
ApiPoints_list = list(map(lambda x:x.replace("[", "").replace("]", ""), ApiPoints_list))
# print(ApiPoints_list[0])
Gold_list = re.findall('"Gold":(\d+),"Type"', a)
Gold_list = list(map(lambda x:x.replace(",", ""), Gold_list))
ApiGold_list = re.findall('"ApiGold":(\d+)', a)
ApiGold_list = list(map(lambda x:x.replace(",", " "), ApiGold_list))
Residue = re.findall('"Residue":(\d+)', a)

txt = open("E:\开奖为旧整体+2.csv", "a")
# txt1 = open("E:\结果1.txt", "a")
txt.write("局号"+","+"Gold"+","+"红利次数"+","+"本地牌"+","+"原始牌"+"AdPoints"+"LinePoints"+"\n")
# txt1.write("局号"+","+"Gold"+","+"红利次数"+","+"本地牌"+","+"原始牌"+"\n")
for i in range(0, len(Gold_list)):
    txt.write(OrderId_list[i]+"a"+","+Gold_list[i]+","+Residue[i]+","+Points_list[i]+","","+ApiPoints_list[i]+","+AdPoints_list[i]+","+LinePoints_list[i]+",""\n")
txt.close()
# txt1.close()
