from vnstock3 import Vnstock
import pandas as pd
import numpy as np
from datetime import datetime
def create_period(year, quarter): # Function to create the period column
    if quarter == 1:
        return f"{year}0331"
    elif quarter == 2:
        return f"{year}0630"
    elif quarter == 3:
        return f"{year}0930"
    elif quarter == 4:
        return f"{year}1231"

def extract_financial_statement(company):
    df_stock = pd.DataFrame()
    for code in company:
        stock = Vnstock().stock(symbol=code, source='VCI')
        ic = stock.finance.income_statement(period='quarter', lang = 'en')
        bs = stock.finance.balance_sheet(period='quarter', lang = 'en')
        cf = stock.finance.cash_flow(period='quarter', lang = 'en')
        ratio = stock.finance.ratio(period='quarter')
        ratio.columns = ratio.columns.get_level_values(1)
        df = pd.concat([bs, ic.iloc[:, 3:], cf.iloc[:, 3:], ratio.iloc[:, 3:]], axis=1)
        df.loc[:, ~df.columns.duplicated(keep='first')]
        df_stock = pd.concat([df_stock, df], ignore_index=True)
    df_stock = df_stock.replace(np.nan, 0.0)
    return df_stock

def extract_historical_price(company):
    end_date = datetime.now().date()
    df_stock = pd.DataFrame()
    for code in company:
        stock = Vnstock().stock(symbol=code, source='VCI')
        hc = stock.quote.history(start='2013-01-01', end=str(end_date), interval='1D')
        hc['Ma CK'] = code.upper()
        df_stock = pd.concat([df_stock, hc], ignore_index=True)
    return df_stock

def extract_stock_data(company):
    df_fs = extract_financial_statement(company)
    df_hp = extract_historical_price(company)
    return df_fs, df_hp

if __name__ == '__main__':
    #financial_statement = extract_financial_statement(['acb','mbb','vcb'])
    #historical_price = extract_historical_price(['acb','mbb','vcb'])
    financial_statement,historical_price = extract_stock_data(['acb','mbb','vcb'])

