import pytest
import requests
import jsonpath
from request import api_key


class TestSendRequest:
    # 类变量：通过类名访问
    success_token = ''
    # 电商登录接口

    def test_login(self):
        url = 'http://39.98.138.157:5000/api/login'
        data = {"password": "123456", "username": "admin"}
        response = requests.request('POST', url, json=data)
        print(response.json())
        # TestSendRequest.success_token = response.json()['token']
        # TestSendRequest.success_token = jsonpath.jsonpath(response.json(), '$.token')[0]
        TestSendRequest.success_token = api_key.ApiKey().get_text(response.text, '$.token')
        print(TestSendRequest.success_token)


    # 获取用户列表
    def test_user(self):
        url = 'http://39.98.138.157:5000/api/getuserinfo'
        header = {"token": TestSendRequest.success_token}
        response = requests.request('GET', url, headers=header)
        print(response.json())

    def test_2(self):
        url = 'http://39.98.138.157:5000'
        response = requests.request('GET', url)
        print(response.status_code)


if __name__ == '__main__':
    pytest.main()
