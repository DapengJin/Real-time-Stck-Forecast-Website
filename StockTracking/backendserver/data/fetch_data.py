# written and debugged by all
import os
import mysql.connector  # using mysql connector should install it first(python 2.7/3.3/3.4)
import pandas as pd
from sqlalchemy.types import VARCHAR, DateTime
import time
# from StockTracking.backendserver.config import *
from sqlalchemy import create_engine
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
####################################################
# global variables definition
User = 'root'
PassWord = 'password'
Host = '127.0.0.1'
Port = '3306'
Database = 'SEProject'
api_key = 'EQ6GGWD5D4ME4283'

# define database engines
sqlite_engine = create_engine(
    'sqlite:///database_stock.db',
    convert_unicode=True,
    echo=True
)
# MYSQL_engine = create_engine(
#     'mysql+mysqlconnector://' + User + ':' + PassWord +
#     '@' + Host + ':' + Port + '/' + Database, echo=False)
# get TimeSeries/TechIndicator object of Alpha Vantage API
ts = TimeSeries(key=api_key, output_format='pandas', retries=20)
ti = TechIndicators(key=api_key, output_format='pandas', retries=20)

# using alpha vantage finance api to save data into a pandas dataframe
stocks = ['AAPL', 'GOOGL', 'NVDA', 'AABA', 'AMZN', 'MSFT', 'BAC', 'NKE', 'NFLX', 'FB']


def init_db():
    # initialize database and create schema if using mysql, if using sqlite it's not necessary
    try:
        cnx = mysql.connector.connect(user=User, password=PassWord, host=Host)  # using configuration of sever
    except mysql.connector.Error:
        print('Can Not Connect With Database Sever.')
        raise SystemExit()
    cursor = cnx.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS ' + Database)  # creat database if not exists
    cursor.execute('USE ' + Database)  # select the database

    for name in stocks:
        # using mysql to create real time data
        create_realtime_data = 'CREATE TABLE IF NOT EXISTS ' + name + '_realtime' + \
                                '''(`date` DATETIME,
                                `open` REAL,
                                `high` REAL,
                                `low` REAL,
                                `close` REAL,
                                `volume` INTEGER,
                                `sym` CHAR(20),
                                PRIMARY KEY(sym,date)
                                );'''

        # using mysql to create historical data
        create_historical_data = 'CREATE TABLE IF NOT EXISTS ' + name + '_historical' + \
                                '''(`date` DATE,
                                `open` REAL,
                                `high` REAL,
                                `low` REAL,
                                `close` REAL,
                                `volume` INTEGER,
                                `sym` CHAR(20),
                                PRIMARY KEY(sym,date)
                                );'''
        cursor.execute(create_realtime_data)  # create table
        cursor.execute(create_historical_data)  # create table


def create_db(stock=stocks, engine=sqlite_engine, realtime_loading=True):
    # create database using mysql or sqlite engine
    print('Reading Data and Putting them in Database. Exit with Ctrl+C.')
    try:
        # returns current price and volume quotes for a given symbol in a dataframe
        df_historical = get_hist_data(stock)
        print('Creating historical database.')
        for i in range(0, len(stock)):
            df = df_historical[i]
            if not os.path.exists('csv'):
                os.makedirs('csv')
            df.to_csv('csv/' + stock[i] + '_historical.csv')
            # df.to_sql(name=stock[i] + '_historical', con=engine, if_exists='replace',
            #           dtype={'date': VARCHAR(df.index.get_level_values('date').str.len().max())})
            df.to_sql(name=stock[i] + '_historical', con=engine, if_exists='replace')

        # ============= code for real-time quotes ==============
        print('Loading real-time data.')
        df_realtime = get_realtime_data(stock)
        last_ones = []
        for i in range(0, len(stock)):
            df = df_realtime[i]
            df.to_csv('csv/' + stock[i] + '_realtime.csv')
            df.to_sql(name=stock[i] + '_realtime', con=engine, if_exists='replace',
                      dtype={'date': VARCHAR(df.index.get_level_values('date').str.len().max())})
            last_ones.append(df_realtime[i].iloc[-1:])

        while realtime_loading:
            print('Continue loading.')
            df_realtime = get_realtime_data(stock)
            for i in range(len(stock)):
                df_newest = pd.DataFrame(df_realtime[i].iloc[-1:])
                if df_newest.values.tolist()[0] == last_ones[i].values.tolist()[0]:
                    continue
                else:
                    last_ones[i] = df_newest
                with open('csv/' + stock[i] + '_realtime.csv', 'a') as file:
                    df_newest.to_csv(file, header=False, index=True)
                df_newest.to_sql(name=stock[i] + '_realtime', con=engine, if_exists='append')
            time.sleep(3)

    except KeyboardInterrupt:
        print('User asked to exit')
        raise SystemExit()
    except ValueError:
        print('Retry if invalid API calls are raised. It might be caused by faulty connection'
              ' or unresponsive server. Or change retries in TimeSeries to a greater number.')
        raise SystemExit()


def get_realtime_data(stock):
    # function for getting realtime data, returns a dataframe of realtime data
    realtime = []
    for ticker in stock:
        print("loading " + ticker)
        df, meta = ts.get_intraday(symbol=ticker, interval='1min', outputsize='compact')
        df['sym'] = meta['2. Symbol']
        realtime.append(df)
    return realtime


def get_hist_data(stock):
    # function for getting realtime data, returns a dataframe of historical data
    historical = []
    for ticker in stock:
        print("loading " + ticker)
        df, meta = ts.get_daily(symbol=ticker, outputsize='full')
        df['sym'] = meta['2. Symbol']
        historical.append(df)
    return historical


def main():
    # init_db()
    create_db(stock=stocks, engine=sqlite_engine, realtime_loading=True)


def add_stock(stockname):
    # add new stock to csv and database if necessary
    create_db(stock=[stockname], engine=sqlite_engine, realtime_loading=False)


if __name__ == '__main__':
    main()
