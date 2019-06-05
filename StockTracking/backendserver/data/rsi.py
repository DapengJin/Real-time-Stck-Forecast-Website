# written and debugged by all
import numpy as np
import os
from .data_manager import DataManager


def calculate_rsi(prices, n=14):
    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed>=0].sum()/n
    down = -seed[seed<0].sum()/n
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100./(1.+rs)

    for i in range(n, len(prices)):
        delta = deltas[i-1] # cause the diff is 1 shorter
        if delta>0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up*(n-1) + upval)/n
        down = (down*(n-1) + downval)/n
        rs = up/down
        rsi[i] = 100. - 100./(1.+rs)
    return rsi


def read_historical(stockname, from_time, to_time):
    dirname = os.path.dirname(__file__)
    path = '/csv/' + stockname + '_historical.csv'
    dm = DataManager(dirname + path)
    column_name = dm.column_names
    dm._data = dm._data.loc[:, ['date', '4. close']]
    dm._back_up = dm._data.copy()
    dm.filter_by_range('date', from_time, to_time, include_max=True)
    historical_prices = dm.data['4. close'].tolist()
    # print(historical_prices)
    return historical_prices

def read_realtime(stockname, from_time, to_time):
    dirname = os.path.dirname(__file__)
    path = '/csv/' + stockname + '_realtime.csv'
    dm = DataManager(dirname + path)
    column_name = dm.column_names
    dm._data = dm._data.loc[:, ['date', '4. close']]
    dm._back_up = dm._data.copy()
    dm.filter_by_range('date', from_time, to_time, include_max=True)
    realtime_prices = dm.data['4. close'].tolist()
    # print(historical_prices)
    return realtime_prices

def get_RSI(stockname, time_type, from_time, to_time):
    if time_type == 'historical':
        data = read_historical(stockname, from_time, to_time)
    else:
        data = read_realtime(stockname, from_time, to_time)
    return calculate_rsi(data).tolist()

