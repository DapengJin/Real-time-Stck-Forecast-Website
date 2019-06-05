# author: Yixuan Duan
import csv
import os
from StockTracking.backendserver.data import data_manager as DM

stockNameSet = ['AABA', 'AAPL', 'AMZN', 'BAC', 'FB', 'GOOGL', 'MSFT', 'NFLX', 'NKE', 'NVDA']


def getStock(sys):
    dirname = os.path.dirname(__file__)
    path = '/csv/'+sys+'_historical.csv'
    # print(dirname)
    dm = DM.DataManager(dirname+path)
    typeSet = dm.column_names
    dataSet = dict()
    dateSet = []
    echartDataSet = []
    for item in typeSet:
        dataSet[item] = []
    lenSize, itemSize = dm.data.shape
    for i in range(lenSize):
        dataItem = dm.data.iloc[i, :]
        dateSet.append(dataItem[0])
        for j in range(itemSize):
            dataSet[typeSet[j]].append(dataItem[j])
    print(dataSet)
    resultSet = dict()
    resultSet['typeName'] = typeSet
    print(resultSet['typeName'])
    resultSet['tableData'] = dataSet
    resultSet['date'] = dateSet
    for i in range(1,itemSize-2):
        echartItem = dict()
        echartItem['name'] = typeSet[i]
        echartItem['type'] = 'line'
        echartItem['smooth'] = True
        echartItem['data'] = dataSet[typeSet[i]]
        echartDataSet.append(echartItem)
    resultSet['echartData'] = echartDataSet
    return resultSet


def getStocks():
    dirname = os.path.dirname(__file__)
    resultSet = []
    typeSet = None
    result = dict()
    for item in stockNameSet:
        path = '/csv/'+item+'_historical.csv'
        dm = DM.DataManager(dirname+path)
        dataItem = dict()
        typeSet = dm.column_names
        lenSize,itemSize = dm.data.shape
        tempItem = dm.data.iloc[lenSize-1, :]
        for j in range(itemSize):
            dataItem[typeSet[j]]=tempItem[j]
        resultSet.append(dataItem)
    result['data'] = resultSet
    result['colName'] = typeSet
    return result

def get_fav_stocks(stocks_set):
    dirname = os.path.dirname(__file__)
    resultSet = []
    typeSet = None
    result = dict()
    for item in stocks_set:
        path = '/csv/'+item+'_historical.csv'
        dm = DM.DataManager(dirname+path)
        dataItem = dict()
        typeSet = dm.column_names
        lenSize,itemSize = dm.data.shape
        tempItem = dm.data.iloc[lenSize-1, :]
        for j in range(itemSize):
            dataItem[typeSet[j]]=tempItem[j]
        resultSet.append(dataItem)
    result['data'] = resultSet
    result['colName'] = typeSet
    return result


def read_historical(stockSymbol, from_time, to_time):
    dirname = os.path.dirname(__file__)
    path = '/csv/' + stockSymbol + '_historical.csv'
    dm = DM.DataManager(dirname + path)
    column_name = dm.column_names
    historical_prices = dm.data[column_name[5]].tolist()
    # print(historical_prices)
    return historical_prices

def formatDate(date):
    dateSet = date.split('-')
    result = dateSet[1]+'/'+dateSet[2]+'/'+dateSet[0]
    return result

def getYearRange(stockSymbol):
    dirname = os.path.dirname(__file__)
    path = '/csv/' + stockSymbol + '_historical.csv'
    print(dirname)
    dm = DM.DataManager(dirname + path)
    #initial 
    dateSet = []
    lenSize, itemSize = dm.data.shape
    for i in range(lenSize):
        dataItem = dm.data.iloc[i, :]
        dateSet.append(dataItem[0])
    resultSet = dict()
    resultSet['min'] = formatDate(dateSet[0])
    resultSet['max'] = formatDate(dateSet[lenSize-1])
    print(resultSet)
    return resultSet


if __name__ == '__main__':
    print(getStock("AMZN"))
