import json, jsonpath

import openpyxl


class ApiKey:

    def get_text(self,data,key):
        dict_data = json.loads(data)
        value_list = jsonpath.jsonpath(dict_data, key)
        return value_list[0]

    def read_excel(self):
        list_tulpe = []
        xls = openpyxl.load_workbook(r'C:\Users\Liuwei\Desktop\API.xlsx')
        sheet = xls['Sheet1']
        for value in sheet.values:
            if type(value[0]) is int:
                list_tulpe.append(value)
        return list_tulpe






