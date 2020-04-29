##################################################################################
# This is a project to display a current situation regarding my stock situation.
# Done by OK

import logging
import pymysql
import pandas as pd
from sshtunnel import SSHTunnelForwarder
from functions import getConfigFile

print('AAA')
logging.info('The process initiated.')

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
    data = pd.read_sql_query(query, conn)
    print(data)
    conn.close()