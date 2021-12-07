"""
This use fb prophet models to forecast the stock time series
"""
import logging
import pandas as pd
import numpy as np

from matplotlib import pyplot as plt
from fbprophet import Prophet
from fbprophet.diagnostics import cross_validation, performance_metrics
from datetime import datetime
from dateutil.relativedelta import relativedelta
from statsmodels.tsa.stattools import adfuller, acf, pacf
from statsmodels.tsa.arima.model import ARIMA
from sklearn.model_selection import train_test_split
from pandas.tseries.offsets import DateOffset
from load_data import load_yf_data


logging.basicConfig(format='%(asctime)s:%(lineno)d:%(message)s', level=logging.DEBUG)

try:
    stocks_data_f, stocks_data = load_yf_data()
    stocks_volume_df = stocks_data.stocks_volume.loc[stocks_data.stocks_volume['curr_volume'] > 0]
    owned_stocks_df = pd.merge(stocks_volume_df, stocks_data.stocks_list[['stock_name', 'stock_symbol']],
                               how='left', on='stock_name')
except Exception:
    logging.error('The data were not loaded.')
    logging.exception("message")
else:
    logging.info('Data loaded and passed for modeling.')


bear_mark = {}
for key in stocks_data_f.keys():
    logging.info(f'{key} in progress.')
    # skip stocks that have no data
    if not stocks_data_f[key].empty:
        # skip stocks that have incomplete data
        if stocks_data_f[key].index[-2].month < int(datetime.now().strftime('%m')) - 1:
            logging.info(f'Data incomplete for {key}')
            continue
        ts_close = stocks_data_f[key].reset_index()[['Date', 'Close']]
        ts_close_ma = ts_close.rolling(3, center=True, closed='both').mean().dropna()
        # initiate prophet modeling part
        model = Prophet()
        model.fit(ts_close_ma.rename(columns={'Date': 'ds', 'Close': 'y'}))

        # model validation - state cuts for cross-validation
        cuts = pd.to_datetime([datetime.now() - relativedelta(months=1),
                               datetime.now() - relativedelta(months=3),
                               datetime.now() - relativedelta(months=6)])
        ts_validate = cross_validation(model, cutoffs=cuts, horizon='15 days', period='5d')
        per_m = performance_metrics(ts_validate)
        if np.mean(per_m['mape']) > 0.1:
            logging.info(f'Forecast not to trust for {key}, mape: {np.mean(per_m["mape"])}.')
            continue
        model.predict()

        # forecasting
        future = model.make_future_dataframe(periods=15, freq='D')
        forecast = model.predict(future)
        # Marking stocks that are interesting for further investigation
        if (np.mean(ts_close_ma.iloc[-15:]['Close']) > np.mean(forecast.iloc[-15:]['trend'])) and \
                (key in owned_stocks_df['stock_symbol']):
            bear_mark[key] = (ts_close.iloc[-1]['Close'] - ts_close_ma.iloc[-15]['Close'])/ts_close_ma.iloc[-15]['Close']
        elif np.mean(ts_close_ma.iloc[-15:]['Close'])/np.mean(forecast.iloc[-15:]['trend']) > 1.05:
            bear_mark[key] = np.mean(ts_close_ma.iloc[-15:]['Close'])/np.mean(forecast.iloc[-15:]['trend'])


        # model.plot(forecast, uncertainty=True)
        # plt.title(f'{key} Forecast and Fitting')
        # plt.show()
        del model, forecast


# Single time series analysis.

# key = 'NVDA'
# select_ts = stocks_data_f[key]['Close']
# # select_ts_ma = select_ts.rolling(3, center=True, closed='both').mean().dropna()
# # Testing stationarity by unit root test
# plt.plot(select_ts)
# plt.show()
# select_ts_diff = select_ts.diff().dropna()
# plt.plot(select_ts_diff)
# plt.show()
# adf_t = adfuller(select_ts)
# print('p-value: %f' % adf_t[1]) #  Non stationary
# adf_diff_t = adfuller(select_ts.diff().dropna())
# print('p-value: %f' % adf_diff_t[1])
#
# # Autocorelation
# acf_tsla = acf(select_ts_diff, nlags=32)
# acf_tsla
# pacf_tsla = pacf(select_ts_diff, nlags=32)
# pacf_tsla
#
# # Building model
# # Split DF
# train, test = train_test_split(select_ts, train_size=0.8, shuffle=False)
# train.reset_index(inplace=True, drop=True)
# model = ARIMA(train, order=(1, 1, 1))
# model_fit = model.fit()
# model_fit.summary()
# plt.plot(model_fit.predict(start=791, end=898))
# plt.show()
#
# pred_date = [select_ts.index[-1] + DateOffset(days=x) for x in range(0, 30)]
# pred_date = pd.Series(index=pred_date[1:])
# data_a = pd.concat([select_ts, pred_date])
# data_a.columns = ['Close', 'Forecast']
# pred_date['Forecast'] = model_fit.predict(start=select_ts.index[-1], end=pred_date.index[-1])
# print('Done')
