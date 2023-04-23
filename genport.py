from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import requests

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
options.add_argument("start-maximized")
options.add_argument("lang=ko_KR")
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument('--allow-insecure-localhost')
options.add_argument(f'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36')

browser = webdriver.Firefox(options=options)

browser.get("https://intro.newsystock.com/login/")

browser.find_element(By.NAME, "ctl00$ContentPlaceHolder1$loginID").send_keys("eun9805")
browser.find_element(By.NAME, "ctl00$ContentPlaceHolder1$loginPWD").send_keys("asdfne3467")
browser.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_btnLogin"]').click()
time.sleep(3)

browser.find_element(By.XPATH, '//*[@id="wrap"]/div[1]/div/div/div/div/div/div[1]/p').click()
browser.find_element(By.XPATH, '//*[@id="wrap"]/div[1]/div/div/div/div/div/div[2]/ul/li[3]/a').click()
# browser.find_element(By.XPATH, '//*[@id="MasterMainMenu"]/div[3]/p').click()

browser.get('http://genport.newsystock.com/GenPro/PortManage.aspx')
time.sleep(3)

browser.quit()