import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import SeleniumLibrary

# driver = webdriver.Chrome()
# driver.get('https://www.baidu.com/')
# driver.find_element(By.ID, 'kw').send_keys('虚竹')
# driver.find_element(By.XPATH, '//*[@id="su"]').click()



# 打开浏览器驱动
driver = webdriver.Chrome()
driver.implicitly_wait(10)


class ServiceConfig():
    # 定义prepareWork函数，做准备工作
    def prepareWork(self, url):
        driver.get(url)

    def click(self):
        driver.find_element(By.ID, 'kw').send_keys('虚竹')
        driver.find_element(By.XPATH, '//*[@id="su"]').click()


if __name__ == '__main__':
    url = 'https://www.baidu.com'
    sc = ServiceConfig()
    sc.prepareWork(url)
    sc.click()
