import os
import pytest

if __name__ == '__main__':
    # 指定生成数据的目录
    pytest.main(['-vs', 'test_only.py', '--alluredir', './temp'])
    # 找到生成测试数据，找到生成的目录（就是测试报告生成在哪里）。将之前测试数据删除掉--clean,再生成测试报告
    os.system('allure generate ./temp -o ./reports --clean')
