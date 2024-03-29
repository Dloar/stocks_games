import pandas as pd
import os
import logging
import yfinance as yf
import time
import numpy as np
import mysql.connector
import logging
import sys
from datetime import datetime

log_filename = 'log_stocks_' + time.strftime("%Y-%m-%d %H;%M;%S", time.gmtime()) + '_run' + '.log'
if sys.platform == 'darwin':
    log_filepath = os.path.join("/Users/ondrejkral/GitHub/stocks_games" + "/stocks_logs/" + log_filename)
else:
    log_filepath = os.path.join("/home/pi/Documents/GitHub/stocks_games" + "/stocks_logs/" + log_filename)
logging.basicConfig(filename=log_filepath, level=logging.DEBUG, format='%(asctime)s:%(lineno)d:%(message)s')

start = time.time()
# Load stock tickers
if sys.platform == 'darwin':
    tickers_df = pd.read_csv('/Users/ondrejkral/GitHub/stocks_games/stock_list.csv', encoding="ISO-8859-1")
    from python_dev.functions import getConfigFile
else:
    tickers_df = pd.read_csv('/home/pi/Documents/GitHub/stocks_games/stock_list.csv', encoding="ISO-8859-1")
    from functions import getConfigFile
tickers_df_index = tickers_df.set_index('Ticker')

config_conn = getConfigFile()
conn = mysql.connector.connect(
    host=config_conn.sql_hostname.iloc[0],
    user=config_conn.sql_username.iloc[0],
    passwd=config_conn.sql_password.iloc[0],
    database=config_conn.sql_main_database.iloc[0],
    port=config_conn.sql_port[0]
)

query = '''SELECT * FROM existing_stocks;'''
stocks_list = pd.read_sql_query(query, conn)
conn.close()

stocks_list.dropna(subset=['country'], inplace=True)
stocks_list = stocks_list.loc[stocks_list['market_cap'] > 200000]
ticker_list = list(stocks_list.loc[:, 'symbol'])

data = yf.download(
        tickers=ticker_list,
        period='1y',
        interval='1d',
        auto_adjust=True,
        prepost=False,
        threads=True,
        proxy=None
    )

data_close = data['Close']
data_close.iloc[1,:]
data_close.iloc[-1,:]

data_open = data['Open']
data_open.iloc[1,:]
data_open.iloc[-1,:]

daily_price = pd.DataFrame(data=data_open.iloc[-1, :]).merge(pd.DataFrame(data=data_close.iloc[-1, :]), how='inner',
                                                            right_index=True, left_index=True)
daily_price.columns = ['Open', 'Close']
daily_price['change_day[%]'] = ((daily_price['Close'] - daily_price['Open'])/daily_price['Close'])*100
filtered_prices_df = daily_price.loc[daily_price['change_day[%]'] < -5]

stocks_interest_df = filtered_prices_df.merge(stocks_list[['symbol', 'shortName', 'longName', 'market_cap']],
                                              how='inner', left_index=True, right_on='symbol')
stocks_interest_df = stocks_interest_df.loc[stocks_interest_df['market_cap'] > 150000000]
stocks_interest_df.reset_index(drop=True, inplace=True)

data_volume = data['Volume']
data_volume.iloc[1,:]
data_volume.iloc[-1,:]

# for ticker in ticker_list:
#     data.loc[(ticker,),].T.to_csv('yhist/' + ticker + '.csv', sep=',', encoding='utf-8')
#
#
# results = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits', 'absolut_change',
#                                 'Company', '6m_history', 'market_cap'])
# try:
#     n_bulks = 10000
#     for bulk in range(n_bulks):
#         stocks_list_df = pd.DataFrame(columns=['symbol', 'shortName', 'longName', 'currency', 'country', 'market_cap', 'sector'])
#         for line in range(int(len(tickers_df)/n_bulks)):
#             i=bulk * int(len(tickers_df)/n_bulks) + line
#             # get data on this ticker
#             ticker_str = tickers_df.loc[i, 'Ticker']
#             logging.warning(' Downloading ' + ticker_str)
#             tickerData = yf.Ticker(ticker_str)
#             try:
#                 tickerData.get_info()['symbol']
#                 try:
#                     market_cap = int(tickerData.get_info()['marketCap'])
#                 except Exception:
#                     market_cap = int(0)
#                 try:
#                     symbol = tickerData.get_info()['symbol']
#                 except Exception:
#                     symbol = None
#                 try:
#                     sector = tickerData.get_info()['sector']
#                 except Exception:
#                     sector = None
#                 try:
#                     country = tickerData.get_info()['country']
#                 except Exception:
#                     country = None
#                 try:
#                     currency = tickerData.get_info()['currency']
#                 except Exception:
#                     currency = None
#                 try:
#                     shortName = tickerData.get_info()['shortName']
#                 except Exception:
#                     shortName = None
#                 try:
#                     longName = tickerData.get_info()['longName']
#                 except Exception:
#                     longName = None
#
#                 stocks_list_df.loc[len(stocks_list_df)] = [symbol, shortName, longName,
#                                                            currency, country, market_cap, sector]
#             except Exception:
#                 logging.warning('Stock skipped' + tickers_df.loc[i, 'Ticker'])
#
#             tickerDf = tickerData.history(period="6mo")
#
#         #     if np.mean(tickerDf['Volume']) >= int(1750000):
#         #         if tickerDf.iloc[:1]['Open'].iloc[0]*0.65 >= tickerDf.iloc[len(tickerDf)-1:]['Open'].iloc[0]:
#         #             print(ticker_str)
#         #             past_value = tickerDf.iloc[len(tickerDf)-1:]['Open'].iloc[0]
#         #             ticker_line = tickerDf.iloc[:1]
#         #             ticker_line['absolut_change'] = ticker_line['Close'] - ticker_line['Open']
#         #             ticker_line['Company'] = tickers_df_index.loc[ticker_str]['Name']
#         #             ticker_line['6m_history'] = past_value
#         #             ticker_line['market_cap'] = market_cap
#         #             results = results.append(ticker_line)
#         # logging.info('All stocks downloaded.')
#
#
#             # tickerDf_filtered = tickerDf.iloc[len(tickerDf.index)-1]
#             # tickerDf_filtered['period'] = tickerDf_filtered.name.strftime('%Y-%m-%d')
#             # tickerDf_filtered['stock_symbol'] = symbol
#             # stocks_data_res = stocks_data_res.append(tickerDf_filtered)
#
#         logging.warning('Data upload initiated.')
#         config_conn = getConfigFile()
#         conn = mysql.connector.connect(
#             host=config_conn.sql_hostname.iloc[0],
#             user=config_conn.sql_username.iloc[0],
#             passwd=config_conn.sql_password.iloc[0],
#             database=config_conn.sql_main_database.iloc[0],
#             port=config_conn.sql_port[0]
#         )
#
#         cursor = conn.cursor()
#         query_s = """INSERT INTO existing_stocks (symbol, shortName, longName, currency, country, market_cap, sector) values (%s, %s, %s, %s, %s, %s, %s)"""
#
#         for i in range(len(stocks_list_df)):
#             cursor.execute(query_s, (stocks_list_df.iloc[i, 0],
#                                      stocks_list_df.iloc[i, 1],
#                                      stocks_list_df.iloc[i, 2],
#                                      stocks_list_df.iloc[i, 3],
#                                      stocks_list_df.iloc[i, 4],
#                                      int(stocks_list_df.iloc[i, 5]),
#                                      stocks_list_df.iloc[i, 6]))
#             conn.commit()
#         cursor.close()
#         conn.close()
#         logging.warning(f"The bulk number {bulk} has been updated.")
# except Exception as e:
#     logging.warning(f"The line {i} could not be loaded.")
#     logging.error(e)


print('It took', time.time()-start, 'seconds.')
