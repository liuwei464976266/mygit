# -*- coding: UTF-8 -*-
import json
import allure
import pytest
import requests
from request import api_key


def return_data():
    print(1)
    data = api_key.ApiKey().read_excel()
    return data


def return_msg(response):
    msg = api_key.ApiKey()
    msg = msg.get_text(response.text, '$.msg')
    return msg


@allure.feature('接口测试项目')
@allure.title('登录模块')
@pytest.mark.parametrize('data', return_data())
def test_login(data):
    allure.description('登录密码验证')
    url = data[1] + data[2]
    method = data[3]
    datas = json.loads(data[5])
    response = requests.request(method, url=url, json=datas)
    print(response.json())
    msg = return_msg(response)
    assert msg == data[8]


def teardown():
    print("后置用例")


if __name__ == '__main__':
    pytest.main(['-vs'])

