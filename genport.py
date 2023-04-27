from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()

ID = os.getenv('ID')
PW = os.getenv('PW')

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
options.add_argument("start-maximized")
options.add_argument("lang=ko_KR")
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument('--allow-insecure-localhost')
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
options.set_preference("general.useragent.override", user_agent)

service = Service(log_path='/home/ubuntu/.wdm/geckodriver.log')
browser = webdriver.Firefox(options=options, service=service)

browser.get("https://intro.newsystock.com/login/")

browser.find_element(By.NAME, "ctl00$ContentPlaceHolder1$loginID").send_keys(ID)
browser.find_element(By.NAME, "ctl00$ContentPlaceHolder1$loginPWD").send_keys(PW)
browser.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_btnLogin"]').click()
time.sleep(3)

browser.find_element(By.XPATH, '//*[@id="wrap"]/div[1]/div/div/div/div/div/div[1]/p').click()
browser.find_element(By.XPATH, '//*[@id="wrap"]/div[1]/div/div/div/div/div/div[2]/ul/li[3]/a').click()

browser.get('http://genport.newsystock.com/GenPro/PortManage.aspx')
time.sleep(3)
port = browser.find_element(By.XPATH, '//*[@id="listVT4069470"]/td[2]/p')
browser.execute_script("arguments[0].click();", port)
time.sleep(3)
tab = browser.find_element(By.CSS_SELECTOR,'#tabMenu4')
browser.execute_script("arguments[0].click();", tab)
time.sleep(3)

html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')
search_result = soup.select('#PortManageSection4 > div:nth-child(3) > ul > table')
table = search_result[0]
table_html = str(table)
table_df_list = pd.read_html(table_html)
table_df = table_df_list[0]
table_df.dropna(inplace=True)
table_df.to_csv('genport.csv', index=False)

browser.quit()

