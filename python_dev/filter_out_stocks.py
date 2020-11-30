import pandas as pd
import os
import logging
import yfinance as yf
import time
import numpy as np
import mysql.connector
import logging
from datetime import datetime
import sys

log_filename = 'log_irp_' + time.strftime("%Y-%m-%d %H;%M;%S", time.gmtime()) + '_run' + '.log'
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

results = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits', 'absolut_change',
                                'Company', '6m_history', 'market_cap'])
try:
    n_bulks = 10
    for bulk in range(n_bulks):
        stocks_list_df = pd.DataFrame(columns=['symbol', 'shortName', 'longName', 'currency', 'country', 'market_cap', 'sector'])
        for line in range(int(len(tickers_df)/n_bulks)):
            i=bulk * int(len(tickers_df)/n_bulks) + line
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

                stocks_list_df.loc[len(stocks_list_df)] = [symbol, shortName, longName,
                                                           currency, country, market_cap, sector]
            except Exception:
                logging.warning('Stock skipped' + tickers_df.loc[i, 'Ticker'])

            tickerDf = tickerData.history(period="6mo")
        logging.warning('Data upload initiated.')
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
        logging.warning(f"The bulk number {bulk} has been updated.")
except Exception as e:
    logging.warning(f"The line {i} could not be loaded.")
    logging.error(e)


print('It took', time.time()-start, 'seconds.')
