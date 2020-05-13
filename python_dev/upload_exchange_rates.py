import logging
from datetime import date, timedelta
from python_dev.functions import loadData, getCurrencyRates, updateExchangeRates
logging.basicConfig(format='%(asctime)s:%(lineno)d:%(message)s', level=logging.DEBUG)

stocks_data = loadData()

yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
today = date.today().strftime('%Y-%m-%d')
list_of_cur = list(stocks_data.stocks_purchases['currency'].unique())

exchange_rate = getCurrencyRates(currencies_list=list_of_cur, yesterday=yesterday)

updateExchangeRates(exchange_rate=exchange_rate)
