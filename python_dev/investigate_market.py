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
import os
from datetime import datetime
import boto3

log_filename = 'log_stocks_' + time.strftime("%Y-%m-%d %H;%M;%S", time.gmtime()) + '_run' + '.log'
if sys.platform == 'darwin':
    log_filepath = os.path.join(os.environ['PWD'] + "/stocks_logs/" + log_filename)
else:
    log_filepath = os.path.join(os.environ['STOCKS_HOME'] + "/stocks_logs/" + log_filename)
logging.basicConfig(filename=log_filepath, level=logging.DEBUG, format='%(asctime)s:%(lineno)d:%(message)s')

start = time.time()

# Load stock tickers
if sys.platform == 'darwin':
    from python_dev.functions import getConfigFile
else:
    from functions import getConfigFile

config_conn = getConfigFile()
conn = mysql.connector.connect(
    host=config_conn.sql_hostname.iloc[0],
    user=config_conn.sql_username.iloc[0],
    passwd=config_conn.sql_password.iloc[0],
    database=config_conn.sql_main_database.iloc[0],
    port=config_conn.sql_port[0]
)

query = '''SELECT * FROM existing_stocks;'''
stocks_list_all = pd.read_sql_query(query, conn)
conn.close()

selected_markets = ['United States', 'United Kingdom ' 'Ukraine', 'Switzerland', 'Sweden', 'Spain', 'Russia', 'Romania',
                    'Portugal', 'Poland', 'Norway', 'Netherlands', 'Monaco', 'Malta', 'Luxembourg', 'Lithuania',
                    'Liechtenstein', 'Latvia', 'Italy', 'Isle of Man', 'Ireland', 'Iceland', 'Hungary', 'Greece',
                    'Germany', 'France', 'Finland', 'Estonia', 'Denmark', 'Czech Republic', 'Cyprus', 'Belgium',
                    'Austria']

stocks_list_all.dropna(subset=['country'], inplace=True)
stocks_list = stocks_list_all.loc[stocks_list_all['country'].isin(selected_markets)]
stocks_list = stocks_list.loc[stocks_list['market_cap'] > 150000000]
stocks_list.reset_index(drop=True, inplace=True)
# stocks_list = stocks_list.head(100)
ticker_list = list(stocks_list.loc[:, 'symbol'])

start = time.time()
data = yf.download(
        tickers=ticker_list,
        period='1y',
        interval='1d',
        auto_adjust=True,
        prepost=False,
        threads=False,
        proxy=None
    )
print('It took', time.time()-start, 'seconds to download the data.')

data_close = data['Close'].copy()
data_volume = data['Volume']

# parameters_df = pd.DataFrame(columns=['symbol', 'alfa', 'beta', 'omega'])
selected_stocks = list()
for stock_name in data_close.columns:
    column_temp = data_close.loc[:, stock_name]
    dataframe_temp = pd.DataFrame(data=column_temp)
    dataframe_temp['t-1'] = dataframe_temp[stock_name].shift(1)
    dataframe_temp['t-m'] = dataframe_temp[stock_name].shift(+20)
    dataframe_temp['t-q'] = dataframe_temp[stock_name].shift(+60)
    dataframe_temp['∆_1'] = ((dataframe_temp[stock_name] - dataframe_temp['t-1'])/dataframe_temp[stock_name])
    dataframe_temp['∆_m'] = ((dataframe_temp['t-1'] - dataframe_temp['t-m'])/dataframe_temp['t-1'])
    dataframe_temp['∆_q'] = ((dataframe_temp['t-m'] - dataframe_temp['t-q'])/dataframe_temp['t-m'])
    dataframe_temp['indi_1'] = np.where(dataframe_temp['∆_1'] < -0.1, 1, 0)
    dataframe_temp['indi_m'] = np.where(dataframe_temp['∆_m'] < -0, 1, 0)
    dataframe_temp['indi_q'] = np.where(dataframe_temp['∆_q'] < -0, 1, 0)
    dataframe_temp['indi_tot'] = np.where((dataframe_temp['indi_q'] == 1) | (dataframe_temp['indi_m'] == 1),
                                           np.where(dataframe_temp['indi_1'] == 1, 1, 0),
                                           0)
    # temp_df = dataframe_temp.loc[dataframe_temp['indi_tot'] ==1]
    # parameters = [np.mean(temp_df['∆_1']), np.mean(temp_df['∆_3']), np.mean(temp_df['∆_5'])]

    if any(dataframe_temp['indi_tot'] == 1):
        selected_stocks += [stock_name]

data_close_df = data['Close'][selected_stocks]

delay = 1
daily_price = pd.DataFrame({'Close_td': data_close_df.iloc[-(delay), :]}).merge(
    pd.DataFrame({'Close_1d': data_close_df.iloc[-(delay+1), :]}),
    how='inner', right_index=True, left_index=True).merge(
    pd.DataFrame({'Close_5d': data_close_df.iloc[-(delay+5), :]}), how='inner', right_index=True,
    left_index=True).merge(
    pd.DataFrame({'Close_10d': data_close_df.iloc[-(delay+10), :]}), how='inner', right_index=True,
    left_index=True).merge(
    pd.DataFrame({'Close_20d': data_close_df.iloc[-(data_close_df.shape[0]-1), :]}), how='inner', right_index=True,
    left_index=True).merge(
    pd.DataFrame({'Close_Vol': data_volume.iloc[-delay, :]}), how='inner', right_index=True, left_index=True)

daily_price['rel_change_1day'] = ((daily_price['Close_td'] - daily_price['Close_1d'])/daily_price['Close_1d'])*100
daily_price['rel_change_5day'] = ((daily_price['Close_1d'] - daily_price['Close_5d'])/daily_price['Close_5d'])*100
daily_price['rel_change_10day'] = ((daily_price['Close_5d'] - daily_price['Close_10d'])/daily_price['Close_10d'])*100
daily_price['rel_change_20day'] = ((daily_price['Close_10d'] - daily_price['Close_20d'])/daily_price['Close_20d'])*100
filtered_prices_df = daily_price.loc[daily_price['rel_change_1day'] < -8]
filtered_prices_df['extreme_values'] = np.where(filtered_prices_df['rel_change_1day'] < -300, 1, 0)

stocks_interest_df = filtered_prices_df.merge(stocks_list[['symbol', 'shortName', 'longName', 'market_cap']],
                                              how='inner', left_index=True, right_on='symbol')
stocks_interest_df = stocks_interest_df.loc[stocks_interest_df['market_cap'] > 200000]
stocks_interest_df.reset_index(drop=True, inplace=True)
top_pics_df = stocks_interest_df.loc[stocks_interest_df['extreme_values'] == 0].sort_values(['rel_change_1day']).head(5)

# Saving results to S3
if sys.platform == 'darwin':
    s3 = boto3.client('s3')
else:
    ACCESS_KEY = config_conn.s3_access_key.iloc[0]
    SECRET_KEY = config_conn.s3_secret_key.iloc[0]
    s3 = boto3.client('s3',
                      aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY
                      )

s3.put_object(
    Body=stocks_interest_df.to_json(orient='records', lines=True),
    Bucket=config_conn.s3_bucket_name.iloc[0],
    Key='selected-stocks/daily-selection/stocks_output.json'
)

if len(top_pics_df) > 0:

    top_tickers_list = list(top_pics_df['symbol'])

    start = time.time()
    data = yf.download(
            tickers=top_tickers_list,
            period='1y',
            interval='1d',
            auto_adjust=True,
            prepost=False,
            threads=False,
            proxy=None
        )

    print('It took', time.time()-start, 'seconds to download the data.')

    data_sel = data['Close'].unstack().reset_index()

    data_sel.columns = ['Symbol', 'Date', 'Price']
    data_sel['Date'] = str(data_sel['Date'])

    s3.put_object(
         Body=data_sel.to_json(orient='records', lines=True),
         Bucket=config_conn.s3_bucket_name.iloc[0],
         Key='selected-stocks/top_picks/top_picks_stocks.json'
    )
