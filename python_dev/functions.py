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
from datetime import datetime


def getConfigFile():
    """
    
    :return:
    """
    with open(os.path.join(os.environ['STOCKS_PATH'] + "/stock_config.yaml")) as yml_file:
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

        def __init__(self, sql_hostname, sql_username, sql_password, sql_main_database, sql_port, ssh_host,
                     ssh_psw, ssh_user, ssh_port, sql_ip, email_user, email_psw):
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

    config_conn = ConfigFile(config_source.sql_hostname, config_source.sql_username, config_source.sql_password,
                             config_source.sql_main_database, config_source.sql_port, config_source.ssh_host,
                             config_source.ssh_psw, config_source.ssh_user, config_source.ssh_port,
                             config_source.sql_ip, config_source.email_user, config_source.email_psw)
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
    conn.close()

    class sourceData(object):
        stocks_list = pd.DataFrame()
        stocks_exposures = pd.DataFrame()
        stocks_purchases = pd.DataFrame()
        stocks_sells = pd.DataFrame()
        stocks_volume = pd.DataFrame()

        def __init__(self, stocks_list, stocks_exposures, stocks_purchases, stocks_sells, stocks_volume):
            self.stocks_list = stocks_list
            self.stocks_exposures = stocks_exposures
            self.stocks_purchases = stocks_purchases
            self.stocks_sells = stocks_sells
            self.stocks_volume = stocks_volume

    stocks_data = sourceData(stocks_list, stocks_exposures, stocks_purchases, stocks_sells, stocks_volume)

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




