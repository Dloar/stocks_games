import pandas as pd
import os
import logging
import yfinance as yf
import time
import numpy as np
import mysql.connector
from datetime import datetime
from functions import getConfigFile

start = time.time()
# Load stock tickers
tickers_df = pd.read_csv('/home/pi/Documents/GitHub/stocks_games/stock_list.csv', encoding="ISO-8859-1")
tickers_df_index = tickers_df.set_index('Ticker')
# tickers_df.shape
#
# ticker_list = list(tickers_df.loc[:, 'Ticker'])
#
# data = yf.download(
#         tickers=ticker_list,
#         period='1y',
#         interval='1d',
#         group_by='ticker',
#         auto_adjust=False,
#         prepost=False,
#         threads=True,
#         proxy=None
#     )
#
# data = data.T
#
# for ticker in ticker_list:
#     data.loc[(ticker,),].T.to_csv('yhist/' + ticker + '.csv', sep=',', encoding='utf-8')


results = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits', 'absolut_change',
                                'Company', '6m_history', 'market_cap'])
stocks_list_df = pd.DataFrame(columns=['symbol', 'shortName', 'longName', 'currency', 'country', 'market_cap',
                                       'sector'])

# for i in range(len(tickers_df)):
for i in range(4):
    # get data on this ticker
    ticker_str = tickers_df.loc[i, 'Ticker']
    logging.warning(' Downloading ' + ticker_str)
    tickerData = yf.Ticker(ticker_str)
    try:
        tickerData.get_info()['symbol']
        try:
            market_cap = int(tickerData.get_info()['marketCap'])
        except Exception:
            market_cap = int(0)
        try:
            symbol = tickerData.get_info()['symbol']
        except Exception:
            symbol = None
        try:
            sector = tickerData.get_info()['sector']
        except Exception:
            sector = None
        try:
            country = tickerData.get_info()['country']
        except Exception:
            country = None
        try:
            currency = tickerData.get_info()['currency']
        except Exception:
            currency = None
        try:
            shortName = tickerData.get_info()['shortName']
        except Exception:
            shortName = None
        try:
            longName = tickerData.get_info()['longName']
        except Exception:
            longName = None
        stocks_list_df.loc[len(stocks_list_df)] = [symbol, shortName, longName, currency, country, market_cap, sector]
    except Exception:
        print('Stock skipped')

    tickerDf = tickerData.history(period="6mo")

    if np.mean(tickerDf['Volume']) >= int(1750000):
        if tickerDf.iloc[:1]['Open'].iloc[0]*0.65 >= tickerDf.iloc[len(tickerDf)-1:]['Open'].iloc[0]:
            print(ticker_str)
            past_value = tickerDf.iloc[len(tickerDf)-1:]['Open'].iloc[0]
            ticker_line = tickerDf.iloc[:1]
            ticker_line['absolut_change'] = ticker_line['Close'] - ticker_line['Open']
            ticker_line['Company'] = tickers_df_index.loc[ticker_str]['Name']
            ticker_line['6m_history'] = past_value
            ticker_line['market_cap'] = market_cap
            results = results.append(ticker_line)



    # tickerDf_filtered = tickerDf.iloc[len(tickerDf.index)-1]
    # tickerDf_filtered['period'] = tickerDf_filtered.name.strftime('%Y-%m-%d')
    # tickerDf_filtered['stock_symbol'] = symbol
    # stocks_data_res = stocks_data_res.append(tickerDf_filtered)


config_conn = getConfigFile()
conn = mysql.connector.connect(
    host=config_conn.sql_hostname.iloc[0],
    user=config_conn.sql_username.iloc[0],
    passwd=config_conn.sql_password.iloc[0],
    database=config_conn.sql_main_database.iloc[0],
    port=config_conn.sql_port[0]
)

cursor = conn.cursor()
query_s = """INSERT INTO existing_stocks (symbol, shortName, longName, currency, country, market_cap, sector) values (%s, %s, %s, %s, %s, %s, %s)"""

for i in range(len(stocks_list_df)):
    cursor.execute(query_s, (stocks_list_df.iloc[i, 0],
                             stocks_list_df.iloc[i, 1],
                             stocks_list_df.iloc[i, 2],
                             stocks_list_df.iloc[i, 3],
                             stocks_list_df.iloc[i, 4],
                             int(stocks_list_df.iloc[i, 5]),
                             stocks_list_df.iloc[i, 6]))
    conn.commit()
cursor.close()
conn.close()


print('It took', time.time()-start, 'seconds.')
