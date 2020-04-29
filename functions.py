import yaml
import os
import pandas as pd

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