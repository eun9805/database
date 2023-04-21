from crawl import *
import FinanceDataReader as fdr

def get_stock_list():
    kospi_master_download(base_dir)
    df = get_kospi_master_dataframe(base_dir) 
    kospi_df = df[(df['그룹코드']=='ST') & (df['거래정지']=='N') & (df['정리매매']=='N') & (df['관리종목']=='N') & (df['불성실공시']=='N') & (df['저유동성']=='N') & (df['시장경고']==0) & (df['우선주']==0) & (df['당기순이익']>0) & (df['SPAC']=='N')]

    kosdaq_master_download(base_dir)
    df = get_kosdaq_master_dataframe(base_dir)
    kosdaq_df = df[(df['증권그룹구분코드']=='ST') & (df['저유동성종목 여부']=='N') & (df['기업인수목적회사여부']=='N') & (df['거래정지 여부']=='N') & (df['정리매매 여부']=='N') & (df['관리 종목 여부']=='N') & (df['시장 경고 구분 코드']==0) & (df['불성실 공시 여부']=='N') & (df['우선주 구분 코드']==0) & (df['단기순이익']>0)]

    stock_list = []
    for code in kospi_df['단축코드']:
        stock_list.append(code)
    for code in kosdaq_df['단축코드']:
        stock_list.append(code)

    df = fdr.StockListing('KRX')
    df = df[df['Code'].isin(stock_list)]

    stock_length = len(stock_list)
    df = df.iloc[-int(stock_length*0.1):]

    stock_list = []
    for code in df['Code']:
        stock_list.append(code)
    return stock_list

def get_db(dbname='2023-04-19_naver_stock.db', table_name='stock_year', stock_list=get_stock_list()):
    con = sqlite3.connect(dbname)
    c = con.cursor()
    df = pd.read_sql(f"SELECT * FROM {table_name}", con)

    df = df[df['code'].isin(stock_list)]
    df = df[(df['연도'] == '2022/12  (IFRS연결)') | (df['연도'] == '2022/12  (IFRS별도)')]
    return df

def get_rank(df):
    raw_df = df.copy()
    raw_df = raw_df[['code','영업이익률', '순이익률', 'ROE(%)', 'ROA(%)', 'EPS(원)', 'BPS(원)','부채비율', 'PER(배)', 'PBR(배)']]
    high_good = ['영업이익률', '순이익률', 'ROE(%)', 'ROA(%)', 'EPS(원)', 'BPS(원)']
    low_good = ['부채비율', 'PER(배)', 'PBR(배)']
    for i in raw_df.columns:
        if i in high_good:
            raw_df[i+'_rank']=raw_df.loc[:,i].rank(ascending=True)
        elif i in low_good:
            raw_df[i+'_rank']=raw_df.loc[:,i].rank(ascending=False)
        else:
            pass
    raw_df['총합'] = raw_df.iloc[:,10:].sum(axis=1)
    raw_df = raw_df.sort_values(by='총합', ascending=False).iloc[0:21]
    return raw_df

get_rank(get_db())