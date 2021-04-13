#####
#
#'''''''
#
#######
import yaml
import os
import pandas as pd
import pandas_datareader.data as web
import mysql.connector
import logging
import yfinance as yf
import sys
from datetime import datetime, date, timedelta


def getConfigFile():
    """
    
    :return:
    """
    if sys.platform == 'darwin':
        with open(os.path.join(os.environ['PWD'] + "/stock_config.yaml")) as yml_file:
            cfg = yaml.safe_load(yml_file)
    else:
        with open(os.path.join("/home/pi/Documents/GitHub/stocks_games/python_dev/stock_config.yaml")) as yml_file:
            cfg = yaml.safe_load(yml_file)

    config_source = pd.DataFrame(cfg, index=[0])

    class ConfigFile(object):
        sql_hostname = str()
        sql_username = str()
        sql_password = str()
        sql_main_database = str()
        sql_port = int()
        ssh_host = str()
        ssh_psw = str()
        ssh_user = str()
        ssh_port = int()
        sql_ip = str()
        email_user = str()
        email_psw = str()
        s3_access_key = str()
        s3_secret_key = str()
        s3_bucket_name = str()

        def __init__(self, sql_hostname, sql_username, sql_password, sql_main_database, sql_port, ssh_host,
                     ssh_psw, ssh_user, ssh_port, sql_ip, email_user, email_psw, s3_access_key, s3_secret_key,
                     s3_bucket_name):
            self.sql_hostname = sql_hostname
            self.sql_username = sql_username
            self.sql_password = sql_password
            self.sql_main_database = sql_main_database
            self.sql_port = sql_port
            self.ssh_host = ssh_host
            self.ssh_psw = ssh_psw
            self.ssh_user = ssh_user
            self.ssh_port = ssh_port
            self.sql_ip = sql_ip
            self.email_user = email_user
            self.email_psw = email_psw
            self.s3_access_key = s3_access_key
            self.s3_secret_key = s3_secret_key
            self.s3_bucket_name = s3_bucket_name

    config_conn = ConfigFile(config_source.sql_hostname, config_source.sql_username, config_source.sql_password,
                             config_source.sql_main_database, config_source.sql_port, config_source.ssh_host,
                             config_source.ssh_psw, config_source.ssh_user, config_source.ssh_port,
                             config_source.sql_ip, config_source.email_user, config_source.email_psw,
                             config_source.s3_access_key, config_source.s3_secret_key, config_source.s3_bucket_name)
    return config_conn


def loadData():
    config_conn = getConfigFile()
    conn = mysql.connector.connect(
        host=config_conn.sql_hostname.iloc[0],
        user=config_conn.sql_username.iloc[0],
        passwd=config_conn.sql_password.iloc[0],
        database=config_conn.sql_main_database.iloc[0],
        port=config_conn.sql_port[0]
    )

    query = '''SELECT * FROM stocks_list;'''
    stocks_list = pd.read_sql_query(query, conn)
    query = '''SELECT * FROM exposures;'''
    stocks_exposures = pd.read_sql_query(query, conn)
    query = '''SELECT * FROM stocks_purchases;'''
    stocks_purchases = pd.read_sql_query(query, conn)
    query = '''SELECT * FROM stocks_sells;'''
    stocks_sells = pd.read_sql_query(query, conn)
    query = '''SELECT * FROM stocks_volume;'''
    stocks_volume = pd.read_sql_query(query, conn)
    query = '''SELECT * FROM exchange_rates;'''
    exchange_rates = pd.read_sql_query(query, conn)
    conn.close()

    class sourceData(object):
        stocks_list = pd.DataFrame()
        stocks_exposures = pd.DataFrame()
        stocks_purchases = pd.DataFrame()
        stocks_sells = pd.DataFrame()
        stocks_volume = pd.DataFrame()
        exchange_rates = pd.DataFrame()

        def __init__(self, stocks_list, stocks_exposures, stocks_purchases, stocks_sells, stocks_volume,
                     exchange_rates):
            self.stocks_list = stocks_list
            self.stocks_exposures = stocks_exposures
            self.stocks_purchases = stocks_purchases
            self.stocks_sells = stocks_sells
            self.stocks_volume = stocks_volume
            self.exchange_rates = exchange_rates

    stocks_data = sourceData(stocks_list, stocks_exposures, stocks_purchases, stocks_sells, stocks_volume,
                             exchange_rates)

    return stocks_data


def getCurrencyRates(currencies_list, yesterday):
    """
    Downloading actual currency from the yahoo webpages.
    :param currencies_list:
    :param yest_day:
    :return:
    """
    exchange_rates = pd.DataFrame(columns=['Close'])
    for cur in currencies_list:
        cur_name = cur + '=X'
        print(cur_name)
        rate = web.DataReader(name=cur_name, data_source='yahoo', start=yesterday, end=yesterday).loc[:,
               ['Close']]
        rate['cur_name'] = cur
        exchange_rates = exchange_rates.append(rate)
    max_date = max(exchange_rates.index)
    exchange_rates = exchange_rates.loc[exchange_rates.index == max_date]
    exchange_rates.index.name = 'source_date'
    exchange_rates.reset_index(inplace=True)
    exchange_rates.rename(columns={'Close': 'cur_rate'}, inplace=True)
    exchange_rates = exchange_rates.loc[:, ['cur_name', 'source_date', 'cur_rate']]

    return exchange_rates


def updateExchangeRates(exchange_rate):
    """

    :param exchange_rate:
    :param yesterday:
    :return:
    """
    config_conn = getConfigFile()
    conn = mysql.connector.connect(
        host=config_conn.sql_hostname.iloc[0],
        user=config_conn.sql_username.iloc[0],
        passwd=config_conn.sql_password.iloc[0],
        database=config_conn.sql_main_database.iloc[0],
        port=config_conn.sql_port[0]
    )

    query = '''SELECT * FROM exchange_rates;'''
    exchange_date = pd.read_sql_query(query, conn)
    if exchange_date.shape[0] > 0:
        exchange_date_max = max(pd.read_sql_query(query, conn)['source_date'])
    else:
        exchange_date_max = datetime(1600, 1, 11, 00, 00)

    cursor = conn.cursor()
    if max(exchange_rate['source_date']) > exchange_date_max:
        exchange_rate = exchange_rate.astype(str)
        query_s = "INSERT INTO exchange_rates (cur_name, source_date, cur_rate) values (%s, %s, %s)"

        for i in range(len(exchange_rate)):
            cursor.execute(query_s, (exchange_rate.iloc[i, 0], exchange_rate.iloc[i, 1], float(exchange_rate.iloc[i,
                                                                                                                  2])))
            conn.commit()
    cursor.close()
    conn.close()
    return 'Exchange Rates updated.'


def getCurrentSituation(stocks_symbols_list, stocks_volume_df, stocks_data):
    """

    :param stocks_symbols_list:
    :param stocks_volume_df:
    :param stocks_data:
    :return:
    """
    sold_stock = getSoldStocksList(stocks_data=stocks_data)

    stocks_data_res = pd.DataFrame()
    stocks_symbols_all_list = list(stocks_symbols_list) + list(sold_stock['stock_symbol'].unique())
    stocks_symbols_all_list = set(stocks_symbols_all_list)

    for symbol in stocks_symbols_all_list:
        # get data on this ticker
        logging.warning(' Downloading ' + symbol)
        tickerData = yf.Ticker(symbol)
        tickerDf = tickerData.history()
        if symbol == 'WIZZ.L':
            tickerDf['Close'] = tickerDf['Close']/100
            tickerDf['Open'] = tickerDf['Open']/100
        tickerDf_filtered = tickerDf.iloc[len(tickerDf.index)-1]
        tickerDf_filtered['period'] = tickerDf_filtered.name.strftime('%Y-%m-%d')
        tickerDf_filtered['stock_symbol'] = symbol
        stocks_data_res = stocks_data_res.append(tickerDf_filtered)

    stocks_prices_df = pd.merge(stocks_data.stocks_list[['stock_name', 'stock_symbol', 'currency']],
                                stocks_data_res[['stock_symbol', 'Close', 'Open', 'period']],
                                how='right', on='stock_symbol')

    exchange_rates_df = stocks_data.exchange_rates.loc[
        stocks_data.exchange_rates['source_date'] == max(stocks_data.exchange_rates['source_date'])]
    logging.warning('Exchange rates are from '+ str(exchange_rates_df['source_date'].iloc[0]))
    stocks_prices_df = pd.merge(stocks_prices_df, exchange_rates_df, how='left', left_on='currency', right_on='cur_name')
    stocks_prices_df['Open_USD'] = stocks_prices_df['Open']/stocks_prices_df['cur_rate']
    stocks_prices_df['Close_USD'] = stocks_prices_df['Close']/stocks_prices_df['cur_rate']

    portfolio_db = pd.merge(stocks_prices_df[['stock_name', 'period', 'stock_symbol', 'Open_USD', 'Close_USD']],
                            stocks_volume_df, how='left', on='stock_name')

    portfolio_db['absolut_change'] = portfolio_db['Close_USD'] - portfolio_db['Open_USD']
    portfolio_db['total_absolut_change'] = (portfolio_db['Close_USD'] - portfolio_db['Open_USD']) * portfolio_db['curr_volume']
    portfolio_db['percentage_change'] = (portfolio_db['absolut_change']/portfolio_db['Close_USD'])*100

    sold_stock_tab = pd.merge(sold_stock, stocks_prices_df[['stock_symbol', 'Close_USD']], how='left',
                              on='stock_symbol')
    sold_stock_tab['curr_sit'] = (sold_stock_tab['price_usd'] - sold_stock_tab['Close_USD']) * sold_stock_tab['volume']

    return portfolio_db, sold_stock_tab


def getSoldStocksList(stocks_data):
    """

    :param stocks_data:
    :return:
    """
    exchange_rates_df = stocks_data.exchange_rates.loc[
        stocks_data.exchange_rates['source_date'] == max(stocks_data.exchange_rates['source_date'])]

    sold_stocks = pd.merge(stocks_data.stocks_sells[['stock_name', 'volume', 'currency', 'price']],
                           exchange_rates_df[['cur_name', 'cur_rate']],
                           left_on='currency', right_on='cur_name')
    sold_stocks['price_usd'] = sold_stocks['price'] / sold_stocks['cur_rate']
    sold_stocks = pd.merge(sold_stocks, stocks_data.stocks_list[['stock_name', 'stock_symbol']],
                           on='stock_name')
    sold_stocks = sold_stocks[['stock_name', 'stock_symbol', 'volume', 'price_usd']]
    return sold_stocks


def getDailyChange():
    """

    :return:
    """
    stocks_data = loadData()

    invested_amount = stocks_data.stocks_exposures['exposure'].sum()

    stocks_volume_df = stocks_data.stocks_volume.loc[stocks_data.stocks_volume['curr_volume'] > 0]
    owned_stocks_df = pd.merge(stocks_volume_df, stocks_data.stocks_list[['stock_name', 'stock_symbol']],
                               how='left', on='stock_name')

    stocks_symbols_list = owned_stocks_df['stock_symbol']

    portfolio_db, sold_stock_tab = getCurrentSituation(stocks_symbols_list=stocks_symbols_list,
                                                       stocks_volume_df=stocks_volume_df,
                                                       stocks_data=stocks_data)

    daily_looser = portfolio_db.loc[portfolio_db['percentage_change'] == min(portfolio_db['percentage_change'])]
    daily_looser = daily_looser.to_html()
    daily_gainer = portfolio_db.loc[portfolio_db['percentage_change'] == max(portfolio_db['percentage_change'])]
    daily_gainer = daily_gainer.to_html()
    daily_result = portfolio_db['total_absolut_change'].sum()
    percentage_change = (((portfolio_db['Close_USD'] * portfolio_db['curr_volume']).sum()/
                          (portfolio_db['Open_USD'] * portfolio_db['curr_volume']).sum()) - 1) * 100
    portfolio_db = portfolio_db.to_html()

    return daily_looser, daily_gainer, daily_result, percentage_change, portfolio_db





