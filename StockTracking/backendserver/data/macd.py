from ..config import *


def get_MACD(stockname, time_type, from_time, to_time):
    if time_type == 'historical':
        interval = 'daily'
    else:
        interval = '1min'
    data = ti.get_macd(symbol=stockname, interval=interval)[0]
    # print(data.loc[from_time:to_time])
    # data is pandas with columns
    # date(index) MACD_Signal MACD_Hist MACD
    return data


if __name__ == '__main__':
    print(get_MACD('AAPL', 'daily', '2013-01-01', '2014-01-01'))