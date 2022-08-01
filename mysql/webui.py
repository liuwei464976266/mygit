from selenium import webdriver
from selenium.webdriver.common.by import By
import SeleniumLibrary
driver = webdriver.Chrome()
driver.get('https://www.baidu.com/')
driver.find_element(By.ID, 'kw').send_keys('虚竹')
driver.find_element(By.XPATH, '//*[@id="su"]').click()
driver.close()
