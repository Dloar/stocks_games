import pandas as pd
from python_dev.functions import loadData, getCurrentSituation

stocks_data = loadData()

invested_amount = stocks_data.stocks_exposures['exposure'].sum()

stocks_volume_df = stocks_data.stocks_volume.loc[stocks_data.stocks_volume['curr_volume'] > 0]
owned_stocks_df = pd.merge(stocks_volume_df, stocks_data.stocks_list[['stock_name', 'stock_symbol']],
                           how='left', on='stock_name')

stocks_symbols_list = owned_stocks_df['stock_symbol']

portfolio_db = getCurrentSituation(stocks_symbols_list, stocks_volume_df, stocks_data)

daily_looser = portfolio_db.loc[portfolio_db['percentage_change'] == min(portfolio_db['percentage_change'])]
daily_gainer = portfolio_db.loc[portfolio_db['percentage_change'] == max(portfolio_db['percentage_change'])]
daily_result = portfolio_db['total_absolut_change'].sum()




