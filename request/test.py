import json

import requests, openpyxl
import api_key


class Apitest:
    def __init__(self, url, data):
        self.url = url
        self.data = json.loads(data)

    def msg(self):

        response = requests.request('POST', url=self.url, json=self.data)
        success_token = api_key.ApiKey()
        success_token = success_token.get_text(response.text, '$.msg')
        return success_token


xls = openpyxl.load_workbook(r'C:\Users\Liuwei\Desktop\API.xlsx')
sheet = xls['Sheet1']
num = 0
for xlsl in sheet.values:
    num += 1
    if type(xlsl[0]) is str:
        continue
    url = xlsl[1]+xlsl[2]
    data = xlsl[5]
    succe = Apitest(url, data)
    success = succe.msg()
    assert success == xlsl[8]
    sheet.cell(num, 10).value = "通过"
xls.save(r'C:\Users\Liuwei\Desktop\API.xlsx')
xls.close()



