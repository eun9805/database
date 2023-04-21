import requests
from bs4 import BeautifulSoup as bs
import FinanceDataReader as fdr
import crawl as cr
import os
import time

base_dir = os.getcwd()

def get_stock_list():
    cr.kospi_master_download(base_dir)
    df = cr.get_kospi_master_dataframe(base_dir) 
    kospi_df = df[(df['그룹코드']=='ST') & (df['거래정지']=='N') & (df['정리매매']=='N') & (df['관리종목']=='N') & (df['불성실공시']=='N') & (df['저유동성']=='N') & (df['시장경고']==0) & (df['우선주']==0) & (df['당기순이익']>0) & (df['SPAC']=='N')]

    cr.kosdaq_master_download(base_dir)
    df = cr.get_kosdaq_master_dataframe(base_dir)
    kosdaq_df = df[(df['증권그룹구분코드']=='ST') & (df['저유동성종목 여부']=='N') & (df['기업인수목적회사여부']=='N') & (df['거래정지 여부']=='N') & (df['정리매매 여부']=='N') & (df['관리 종목 여부']=='N') & (df['시장 경고 구분 코드']==0) & (df['불성실 공시 여부']=='N') & (df['우선주 구분 코드']==0) & (df['단기순이익']>0)]

    stock_list = []
    for code in kospi_df['단축코드']:
        stock_list.append(code)
    for code in kosdaq_df['단축코드']:
        stock_list.append(code)

    df = fdr.StockListing('KRX')
    df = df[df['Code'].isin(stock_list)]

    stock_length = len(stock_list)
    df = df.iloc[-int(stock_length*0.2):]

    stock_list = []
    for code in df['Code']:
        stock_list.append(code)
    return stock_list

raw_dict={}

for i in get_stock_list():
    url_base = 'https://rank.newsystock.com/NewsyPageNew/StockRank.aspx?SCode=A{code}#none'
    url = url_base.format(code=i)
    req = requests.get(url)
    html = req.text
    soup = bs(html, 'html.parser')
    fund = soup.find('span', id='ctl00_lbScoreFund').text
    raw_dict[i] = fund
    print(i, fund)
    time.sleep(0.5)

newsy_dict = sorted(raw_dict.items(), key=lambda x: x[1], reverse=True)
target_list = []
for i in range(10):
    target_list.append(newsy_dict[i][0])

print(target_list)


