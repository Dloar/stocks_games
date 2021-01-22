import yfinance as yf
import logging
import pandas as pd
from datetime import datetime
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

yest_day = datetime.today().strftime('%Y-%m-%d')
invested_amount = -469000
withdraw_amount = 171000

class currentPortfolio():
    current_exposure = int
    invested_amount = int

    def __init__(self, current_exposure, invested_amount):
        self.current_exposure = current_exposure
        self.invested_amount = invested_amount


curr_port = currentPortfolio(current_exposure=(invested_amount - invested_amount),
                             invested_amount=abs(invested_amount))

portfolio_df_current = pd.DataFrame(columns={'stock_name', 'stock_abr', 'volume', 'exposure', 'current_price'})

# VOLUME
avast_vol = 2000
intel_vol = 35
activ_vol = 24
alib_vol = 8
veol_vol = 50
tota_vol = 13
kb_vol = 25
arot_vol = 300
stoc_vol = 315
amgn_vol = 6
amzn_vol = 1
mnt_vol = 100
lts_vol = 17


#define the ticker symbol
# Past stocks
past_symbols = ['BABA', 'AMGN', 'ATVI', 'INTC', 'KOMB.PR', 'LMT']
# tickerSymbol = 'BABA'
# tickerSymbol = 'AMGN'
# tickerSymbol = 'ATVI'
# tickerSymbol = 'INTC'

# tickerSymbol = 'CEZ.PR'
# tickerSymbol = 'TSLA'
# tickerSymbol = 'AAPL'
# tickerSymbol = 'CL=F'
# tickerSymbol = 'GC=F'


# Current stocks
current_symbols = ['FP.PA', 'VIE.PA', 'AMZN', 'MRK', 'KOMB.PR', 'AVST.PR']
# tickerSymbol = 'FP.PA'
# tickerSymbol = 'VIE.PA'
tickerSymbol = 'AMZN'
# tickerSymbol = 'MRK'
# tickerSymbol = 'KOMB.PR'
# tickerSymbol = 'AVST.PR'

stocks_data = {name: pd.DataFrame() for name in current_symbols}
for symbol in current_symbols:
    # get data on this ticker
    logging.warning(' Downloading ' + symbol)
    tickerData = yf.Ticker(tickerSymbol)

    # get the historical prices for this ticker
    tickerDf = tickerData.history(period='1d', start='2019-1-1', end=yest_day)
    tickerDf['deviation'] = ((tickerDf['High']-tickerDf['Low'])/tickerDf['Low'])*100
    tickerDf['differenceOC'] = (tickerDf['Open']-tickerDf['Close'])
    tickerDf['differenceHL'] = (tickerDf['High']-tickerDf['Low'])
    tickerDf['mean'] = ((tickerDf['Open']+tickerDf['Close'])/2)
    tickerDf['MA_per5'] = tickerDf['mean'].rolling(window=5).mean()
    tickerDf['MA_per3'] = tickerDf['mean'].rolling(window=3).mean()
    tickerDf = tickerDf[['mean', 'deviation', 'differenceOC', 'differenceHL', 'MA_per3', 'MA_per5']]

    stocks_data[symbol] = tickerDf
    print(tickerDf.index[-1])

# #get the historical prices for this ticker
# tickerDf = tickerData.history(period='1d', start='2010-1-1', end=yest_day)
# print(tickerDf.index[-1])
#
#see your data
print(tickerDf.tail())


x = tickerDf.index
y = (tickerDf.loc[:, 'MA_per5'])
plt.plot(x, y)
plt.title(tickerData.get_info()['shortName'])
plt.show()

# #info on the company
# print(tickerData.info)
#
# #get event data for ticker
# print(tickerData.calendar)
#
# #get recommendation data for ticker
# print(tickerData.recommendations)
