# import json
# import requests
# url = "http://192.168.10.213:9002/api/Service/callRecord4Client"
# payload = {"page":1,"len":"10000000","gameType":230,"roomConfigId":275}
# headers = {
#   'token': '95180DB115731941C9154D72699036E05C74',
#   'Content-Type': 'application/json'
# }
# response = requests.request("POST", url, headers=headers, json=payload)
# response = json.loads(response.text)
# data = response["data"]
# for i in data:
#   print(i)


# cc = [1, 3, 5, 7]
# x = [-1, 1]
# ii = 100000
# import random
# dd  = {}
# for i in range(10):
#     c = []
#     for i in range(ii):
#         num = 0
#         for y in range(7):
#             a = random.randint(0, 1)
#             num += x[a]
#         # print(num)
#         c.append(abs(num))
#     ccc = 0
#     for i in cc:
#         counts = c.count(i)
#         dd[i] = counts
#         if i == 1:
#             ccc += counts/2*0.2 + counts/2*0.3
#         elif i == 3:
#             ccc += counts/2*0.3 + counts/2*1.5
#         elif i == 5:
#             ccc += counts/2*1.5 + counts/2*4
#         elif i == 7:
#             ccc += counts/2*4 + counts/2*29
#     print(dd)
#     print(ccc,ccc/ii-1)
import random
count = 100000

# for y in range(1):
#     gold2 = 0
#     for n in range(1, 31):
#         gold = 0
#         for i in range(count):
#             number = 0
#             for x in range(n):
#                 num = random.randint(0, 1)
#                 if num == 0:
#                     gold += 0
#                     continue
#                 number += num
#                 if number == n:
#                     gold += 1.94**n
#         print(n, '---', gold)
#         gold2 += gold
#     print(gold2, gold2/count)

