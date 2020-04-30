import yaml
import os
import pymysql
import pandas as pd
from sshtunnel import SSHTunnelForwarder

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

        def __init__(self, sql_hostname, sql_username, sql_password, sql_main_database, sql_port, ssh_host,
                     ssh_psw, ssh_user, ssh_port, sql_ip):
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

    config_conn = ConfigFile(config_source.sql_hostname, config_source.sql_username, config_source.sql_password,
                             config_source.sql_main_database, config_source.sql_port, config_source.ssh_host,
                             config_source.ssh_psw, config_source.ssh_user, config_source.ssh_port,
                             config_source.sql_ip)
    return config_conn


def loadData():
    config_conn = getConfigFile()

    with SSHTunnelForwarder(
            (config_conn.ssh_host.iloc[0], int(config_conn.ssh_port.iloc[0])),
            ssh_username=config_conn.ssh_user.iloc[0],
            ssh_password=config_conn.ssh_psw.iloc[0],
            remote_bind_address=(config_conn.sql_hostname.iloc[0], int(config_conn.sql_port.iloc[0]))) as tunnel:
        conn = pymysql.connect(host=config_conn.sql_hostname.iloc[0], user=config_conn.sql_username.iloc[0],
                               passwd=config_conn.sql_password.iloc[0], db=config_conn.sql_main_database.iloc[0],
                               port=tunnel.local_bind_port)
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
