import pandas as pd
import pandas_datareader.data as web
from datetime import datetime

start = datetime(2020, 4, 30)
end = datetime(2020, 4, 30)
eur = web.DataReader('EUR=X', 'yahoo', start, end)['Close']