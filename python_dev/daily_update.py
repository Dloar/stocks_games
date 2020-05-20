import yfinance as yfgetCurrencyRates
import pandas as pd
from python_dev.functions import loadData

stocks_data = loadData()

invested_amount = stocks_data.stocks_exposures['exposure'].sum()

stocks_volume_df = stocks_data.stocks_volume.loc[stocks_data.stocks_volume['curr_volume'] > 0]

