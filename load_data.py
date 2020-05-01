##################################################################################
# This is a project to display a current situation regarding my stock situation.
# Done by OK

import logging
import yfinance as yf
import pandas as pd
import pandas as pd
from datetime import date, timedelta
from functions import loadData, getCurrencyRates
logging.basicConfig(format='%(asctime)s:%(lineno)d:%(message)s', level=logging.DEBUG)

print('AAA')
logging.info('The process initiated.')

stocks_data = loadData()

# yesterday = date.today() - timedelta(days=1)
yest_day = date.today().strftime('%Y-%m-%d')

exchange_rate = getCurrencyRates(yest_day=yest_day)

list_of_stocks = stocks_data.stocks_list['stock_symbol'].tolist()
print(list_of_stocks)

stocks_data = {name: pd.DataFrame() for name in list_of_stocks}
for symbol in list_of_stocks:
    # get data on this ticker
    logging.info(' Downloading ' + symbol)
    tickerData = yf.Ticker(symbol)

    # get the historical prices for this ticker
    tickerDf = tickerData.history(period='1d', start='2020-3-28', end='2020-4-30')
    # tickerDf['deviation'] = ((tickerDf['High']-tickerDf['Low'])/tickerDf['Low'])*100
    # tickerDf['differenceOC'] = (tickerDf['Open']-tickerDf['Close'])
    # tickerDf['differenceHL'] = (tickerDf['High']-tickerDf['Low'])
    # tickerDf['mean'] = ((tickerDf['Open']+tickerDf['Close'])/2)
    # tickerDf['MA_per5'] = tickerDf['mean'].rolling(window=5).mean()
    # tickerDf['MA_per3'] = tickerDf['mean'].rolling(window=3).mean()
    # tickerDf = tickerDf[['mean', 'deviation', 'differenceOC', 'differenceHL', 'MA_per3', 'MA_per5']]

    stocks_data[symbol] = tickerDf
    print(tickerDf.index[-1])

