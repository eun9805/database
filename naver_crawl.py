'''코스피주식종목코드(kospi_code.mst) 정제 파이썬 파일'''

import urllib.request
import ssl
import zipfile
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

base_dir = '/home/ubuntu/database'

def kospi_master_download(base_dir, verbose=False):
    cwd = os.getcwd()
    if (verbose): print(f"current directory is {cwd}")
    ssl._create_default_https_context = ssl._create_unverified_context

    urllib.request.urlretrieve("https://new.real.download.dws.co.kr/common/master/kospi_code.mst.zip",
                               base_dir + "/kospi_code.zip")

    os.chdir(base_dir)
    if (verbose): print(f"change directory to {base_dir}")
    kospi_zip = zipfile.ZipFile('kospi_code.zip')
    kospi_zip.extractall()

    kospi_zip.close()

    if os.path.exists("kospi_code.zip"):
        os.remove("kospi_code.zip")


def get_kospi_master_dataframe(base_dir):
    file_name = base_dir + "/kospi_code.mst"
    tmp_fil1 = base_dir + "/kospi_code_part1.tmp"
    tmp_fil2 = base_dir + "/kospi_code_part2.tmp"

    wf1 = open(tmp_fil1, mode="w")
    wf2 = open(tmp_fil2, mode="w")

    with open(file_name, mode="r", encoding="cp949") as f:
        for row in f:
            rf1 = row[0:len(row) - 228]
            rf1_1 = rf1[0:9].rstrip()
            rf1_2 = rf1[9:21].rstrip()
            rf1_3 = rf1[21:].strip()
            wf1.write(rf1_1 + ',' + rf1_2 + ',' + rf1_3 + '\n')
            rf2 = row[-228:]
            wf2.write(rf2)

    wf1.close()
    wf2.close()

    part1_columns = ['단축코드', '표준코드', '한글명']
    df1 = pd.read_csv(tmp_fil1, header=None, names=part1_columns, encoding='utf-8')

    field_specs = [2, 1, 4, 4, 4,
                   1, 1, 1, 1, 1,
                   1, 1, 1, 1, 1,
                   1, 1, 1, 1, 1,
                   1, 1, 1, 1, 1,
                   1, 1, 1, 1, 1,
                   1, 9, 5, 5, 1,
                   1, 1, 2, 1, 1,
                   1, 2, 2, 2, 3,
                   1, 3, 12, 12, 8,
                   15, 21, 2, 7, 1,
                   1, 1, 1, 1, 9,
                   9, 9, 5, 9, 8,
                   9, 3, 1, 1, 1
                   ]

    part2_columns = ['그룹코드', '시가총액규모', '지수업종대분류', '지수업종중분류', '지수업종소분류',
                     '제조업', '저유동성', '지배구조지수종목', 'KOSPI200섹터업종', 'KOSPI100',
                     'KOSPI50', 'KRX', 'ETP', 'ELW발행', 'KRX100',
                     'KRX자동차', 'KRX반도체', 'KRX바이오', 'KRX은행', 'SPAC',
                     'KRX에너지화학', 'KRX철강', '단기과열', 'KRX미디어통신', 'KRX건설',
                     'Non1', 'KRX증권', 'KRX선박', 'KRX섹터_보험', 'KRX섹터_운송',
                     'SRI', '기준가', '매매수량단위', '시간외수량단위', '거래정지',
                     '정리매매', '관리종목', '시장경고', '경고예고', '불성실공시',
                     '우회상장', '락구분', '액면변경', '증자구분', '증거금비율',
                     '신용가능', '신용기간', '전일거래량', '액면가', '상장일자',
                     '상장주수', '자본금', '결산월', '공모가', '우선주',
                     '공매도과열', '이상급등', 'KRX300', 'KOSPI', '매출액',
                     '영업이익', '경상이익', '당기순이익', 'ROE', '기준년월',
                     '시가총액', '그룹사코드', '회사신용한도초과', '담보대출가능', '대주가능'
                     ]

    df2 = pd.read_fwf(tmp_fil2, widths=field_specs, names=part2_columns)

    df = pd.merge(df1, df2, how='outer', left_index=True, right_index=True)

    # clean temporary file and dataframe
    del (df1)
    del (df2)
    os.remove(tmp_fil1)
    os.remove(tmp_fil2)
    
    print("KOSPI Done")

    return df

def kosdaq_master_download(base_dir, verbose=False):

    cwd = os.getcwd()
    if (verbose): print(f"current directory is {cwd}")
    ssl._create_default_https_context = ssl._create_unverified_context
    
    urllib.request.urlretrieve("https://new.real.download.dws.co.kr/common/master/kosdaq_code.mst.zip",
                               base_dir + "/kosdaq_code.zip")

    os.chdir(base_dir)
    if (verbose): print(f"change directory to {base_dir}")
    kosdaq_zip = zipfile.ZipFile('kosdaq_code.zip')
    kosdaq_zip.extractall()
    
    kosdaq_zip.close()

    if os.path.exists("kosdaq_code.zip"):
        os.remove("kosdaq_code.zip")

def get_kosdaq_master_dataframe(base_dir):
    file_name = base_dir + "/kosdaq_code.mst"
    tmp_fil1 = base_dir + "/kosdaq_code_part1.tmp"
    tmp_fil2 = base_dir + "/kosdaq_code_part2.tmp"

    wf1 = open(tmp_fil1, mode="w")
    wf2 = open(tmp_fil2, mode="w")

    with open(file_name, mode="r", encoding="cp949") as f:
        for row in f:
            rf1 = row[0:len(row) - 222]
            rf1_1 = rf1[0:9].rstrip()
            rf1_2 = rf1[9:21].rstrip()
            rf1_3 = rf1[21:].strip()
            wf1.write(rf1_1 + ',' + rf1_2 + ',' + rf1_3 + '\n')
            rf2 = row[-222:]
            wf2.write(rf2)

    wf1.close()
    wf2.close()

    part1_columns = ['단축코드','표준코드','한글종목명']
    df1 = pd.read_csv(tmp_fil1, header=None, names=part1_columns, encoding='utf-8')

    field_specs = [2, 1,
                   4, 4, 4, 1, 1,
                   1, 1, 1, 1, 1,
                   1, 1, 1, 1, 1,
                   1, 1, 1, 1, 1,
                   1, 1, 1, 1, 9,
                   5, 5, 1, 1, 1,
                   2, 1, 1, 1, 2,
                   2, 2, 3, 1, 3,
                   12, 12, 8, 15, 21,
                   2, 7, 1, 1, 1,
                   1, 9, 9, 9, 5,
                   9, 8, 9, 3, 1,
                   1, 1
                   ]

    part2_columns = ['증권그룹구분코드','시가총액 규모 구분 코드 유가',
                     '지수업종 대분류 코드','지수 업종 중분류 코드','지수업종 소분류 코드','벤처기업 여부 (Y/N)',
                     '저유동성종목 여부','KRX 종목 여부','ETP 상품구분코드','KRX100 종목 여부 (Y/N)',
                     'KRX 자동차 여부','KRX 반도체 여부','KRX 바이오 여부','KRX 은행 여부','기업인수목적회사여부',
                     'KRX 에너지 화학 여부','KRX 철강 여부','단기과열종목구분코드','KRX 미디어 통신 여부',
                     'KRX 건설 여부','(코스닥)투자주의환기종목여부','KRX 증권 구분','KRX 선박 구분',
                     'KRX섹터지수 보험여부','KRX섹터지수 운송여부','KOSDAQ150지수여부 (Y,N)','주식 기준가',
                     '정규 시장 매매 수량 단위','시간외 시장 매매 수량 단위','거래정지 여부','정리매매 여부',
                     '관리 종목 여부','시장 경고 구분 코드','시장 경고위험 예고 여부','불성실 공시 여부',
                     '우회 상장 여부','락구분 코드','액면가 변경 구분 코드','증자 구분 코드','증거금 비율',
                     '신용주문 가능 여부','신용기간','전일 거래량','주식 액면가','주식 상장 일자','상장 주수(천)',
                     '자본금','결산 월','공모 가격','우선주 구분 코드','공매도과열종목여부','이상급등종목여부',
                     'KRX300 종목 여부 (Y/N)','매출액','영업이익','경상이익','당기순이익','ROE',
                     '기준년월','시가총액','그룹사 코드','회사신용한도초과여부','담보대출가능여부','대주가능여부'
                     ]

    df2 = pd.read_fwf(tmp_fil2, widths=field_specs, names=part2_columns)

    df = pd.merge(df1, df2, how='outer', left_index=True, right_index=True)

    # clean temporary file and dataframe
    del (df1)
    del (df2)
    os.remove(tmp_fil1)
    os.remove(tmp_fil2)

    print("KOSDAQ Done")

    return df

def make_list():
    kospi_master_download(base_dir)
    df = get_kospi_master_dataframe(base_dir) 
    kospi_df = df[(df['그룹코드']=='ST') & (df['거래정지']=='N') & (df['정리매매']=='N') & (df['관리종목']=='N') & (df['불성실공시']=='N') & (df['저유동성']=='N') & (df['시장경고']==0) & (df['우선주']==0) & (df['SPAC']=='N')]

    kosdaq_master_download(base_dir)
    df = get_kosdaq_master_dataframe(base_dir)
    kosdaq_df = df[(df['증권그룹구분코드']=='ST') & (df['저유동성종목 여부']=='N') & (df['기업인수목적회사여부']=='N') & (df['거래정지 여부']=='N') & (df['정리매매 여부']=='N') & (df['관리 종목 여부']=='N') & (df['시장 경고 구분 코드']==0) & (df['불성실 공시 여부']=='N') & (df['우선주 구분 코드']==0)]

    ticker_list = kospi_df['단축코드'].tolist() + kosdaq_df['단축코드'].tolist()
    return ticker_list

import requests
from bs4 import BeautifulSoup
import pandas as pd

def crawling_data(ticker):
    url = f"https://finance.naver.com/item/main.nhn?code={ticker}"
    html = requests.get(url, headers={'User-agent':'Mozilla/5.0'})
    soup = BeautifulSoup(html.text, "lxml")
    per = soup.select("#_per")
    pbr = soup.select("#_pbr")
    market_sum = soup.select("#_market_sum")
    pers = []
    pbrs = []
    market_sums = []
    ticker_list = []

    ticker_list.append(ticker)

    if not per:  # 리스트가 비어있을 경우 None으로 변환
        per = [None]
    for pe in per:
        if pe != None:
            per_text = pe.text
            per_text = per_text.replace(",", "")  # float변환을 위해 따옴표 제거
            pers.append(float(per_text))
        else:
            per_text = pe
            pers.append(per_text)

    if not pbr:  # 리스트가 비어있을 경우 None으로 변환
        pbr = [None]
    for pb in pbr:
        if pb != None:
            pbr_text = pb.text
            pbr_text = pbr_text.replace(",", "")  # float변환을 위해 따옴표 제거
            pbrs.append(float(pbr_text))
        else:
            pbr_text = pb
            pbrs.append(pbr_text)

    if not market_sum:  # 리스트가 비어있을 경우 None으로 변환
        market_sum = [None]
    for d in market_sum:
        if d != None:
            market_sum_text = d.text
            market_sum_text = market_sum_text.replace("조", "")
            market_sum_text = market_sum_text.replace("\n", "")
            market_sum_text = market_sum_text.replace("\t", "")
            market_sum_text = market_sum_text.replace(",", "")
            market_sums.append(int(market_sum_text))
        else:
            market_sum_text = d
            market_sums.append(market_sum_text)
    
    stock_df = pd.DataFrame({"CODE":ticker_list,
                       "PER":pers,
                       "PBR":pbrs,
                       "SUM":market_sums})

    return stock_df

ticker_list = make_list()
stock_df = pd.DataFrame(columns=['CODE', 'PER', 'PBR', 'SUM'])

for i in ticker_list:
    stock_df = pd.concat([stock_df, crawling_data(i)])
    print(i, "Done")

stock_df = stock_df.dropna()
rank_df = stock_df.copy()
rank_df['PER_rank'] = rank_df['PER'].rank(ascending=False)
rank_df['PBR_rank'] = rank_df['PBR'].rank(ascending=False)
rank_df['SUM_rank'] = rank_df['SUM'].rank(ascending=False)
rank_df['Total_rank'] = rank_df['PER_rank'] + rank_df['PBR_rank'] + rank_df['SUM_rank']
rank_df = rank_df.sort_values(by='Total_rank', ascending=False)
today = datetime.now().date()
rank_df.to_csv(f'/home/ubuntu/database/{today}_rank.csv', index=False)
# test_df = pd.read_csv('/home/ubuntu/database/2023-04-22_rank.csv', dtype={'CODE':str})