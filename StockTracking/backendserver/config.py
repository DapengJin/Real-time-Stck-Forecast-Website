from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from sqlalchemy import create_engine


####################################################
# global variables definition
User = 'root'
PassWord = 'password'
Host = '127.0.0.1'
Port = '3306'
Database = 'SEProject'
api_key = 'EQ6GGWD5D4ME4283'


# get TimeSeries/TechIndicator object of Alpha Vantage API
ts = TimeSeries(key=api_key, output_format='pandas', retries=20)
ti = TechIndicators(key=api_key, output_format='pandas', retries=20)

# using alpha vantage finance api to save data into a pandas dataframe
stocks = ['AAPL', 'GOOGL', 'NVDA', 'AABA', 'AMZN', 'MSFT', 'BAC', 'NKE', 'NFLX', 'FB']




