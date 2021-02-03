import pandas as pd
import os
import logging
import yfinance as yf
import time
import json
import numpy as np
import mysql.connector
import logging
import sys
from datetime import datetime
import boto3

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
stocks_list = stocks_list.head(n=50)
ticker_list = list(stocks_list.loc[:, 'symbol'])

start = time.time()
data = yf.download(
        tickers=ticker_list,
        period='20d',
        interval='1d',
        auto_adjust=True,
        prepost=False,
        threads=False,
        proxy=None
    )
print('It took', time.time()-start, 'seconds to download the data.')

data_close = data['Close']
data_open = data['Open']
data_volume = data['Volume']

daily_price_temp = pd.DataFrame(data=data_close.iloc[-3, :]).merge(pd.DataFrame(data=data_close.iloc[-2, :]),
                                                                   how='inner', right_index=True, left_index=True)
daily_price = daily_price_temp.merge(pd.DataFrame(data=data_volume.iloc[-2, :]),
                                     how='inner', right_index=True, left_index=True)


daily_price.columns = ['Open', 'Close', 'Volume']
daily_price['change_day[%]'] = ((daily_price['Close'] - daily_price['Open'])/daily_price['Close'])*100
filtered_prices_df = daily_price.loc[daily_price['change_day[%]'] < -5]


stocks_interest_df = filtered_prices_df.merge(stocks_list[['symbol', 'shortName', 'longName', 'market_cap']],
                                              how='inner', left_index=True, right_on='symbol')
stocks_interest_df = stocks_interest_df.loc[stocks_interest_df['market_cap'] > 150000000]
stocks_interest_df.reset_index(drop=True, inplace=True)
stocks_json = stocks_interest_df.to_json()


if sys.platform == 'darwin':
    s3 = boto3.client('s3')
else:
    ACCESS_KEY = config_conn.Access_key_ID.iloc[0]
    SECRET_KEY = config_conn.Secret_access_key.iloc[0]
    s3 = boto3.client('s3',
                      aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY
                      )

s3.put_object(
     Body=stocks_interest_df.to_json(orient='records', lines=True),
     Bucket='stocks-list-poi',
     Key='selected-stocks/stocks_output_rPi.json'
)
