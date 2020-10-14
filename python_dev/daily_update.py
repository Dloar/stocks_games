import pandas as pd
from python_dev.functions import loadData, getCurrentSituation

stocks_data = loadData()

invested_amount = stocks_data.stocks_exposures['exposure'].sum()

stocks_volume_df = stocks_data.stocks_volume.loc[stocks_data.stocks_volume['curr_volume'] > 0]

owned_stocks_df = pd.merge(stocks_volume_df, stocks_data.stocks_list[['stock_name', 'stock_symbol']],
                           how='left', on='stock_name')

stocks_symbols_list = owned_stocks_df['stock_symbol']

portfolio_db, sold_stock_tab = getCurrentSituation(stocks_symbols_list, stocks_volume_df, stocks_data)

daily_looser = portfolio_db.loc[portfolio_db['percentage_change'] == min(portfolio_db['percentage_change'])]
daily_gainer = portfolio_db.loc[portfolio_db['percentage_change'] == max(portfolio_db['percentage_change'])]
daily_result = portfolio_db['total_absolut_change'].sum()

# Get the situation of the stocks I owned
stocks_sells_tab = stocks_data.stocks_sells.copy()
stocks_sells_tab['gain'] = (stocks_sells_tab['price'] * stocks_sells_tab['volume'])

stocks_sells_tab = stocks_sells_tab.groupby(['provider', 'stock_name', 'market', 'currency']).sum()

stocks_symbols_sold_list = pd.merge(stocks_volume_df, stocks_data.stocks_list[['stock_name', 'stock_symbol']],
                           how='left', on='stock_name')

