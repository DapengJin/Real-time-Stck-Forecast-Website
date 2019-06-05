# written by all, debugged by Zhiwen Wang
from .neural_network import NeuralNetwork
import time
import sys
if sys.version_info[0] == 2:
    from urllib import urlopen
else:
    from urllib.request import urlopen
import subprocess
import numpy as np
from sklearn.svm import SVR
from datetime import datetime
from itertools import islice

# ================================================================

def normalizePrice(price, minimum, maximum):
    return ((2*price - (maximum + minimum)) / (maximum - minimum))

def denormalizePrice(price, minimum, maximum):
    return (((price*(maximum-minimum))/2) + (maximum + minimum))/2

# ================================================================

def rollingWindow(seq, windowSize):
    it = iter(seq)
    win = [next(it) for cnt in range(windowSize)] # First window
    yield win
    for e in it: # Subsequent windows
        win[:-1] = win[1:]
        win[-1] = e
        yield win

def getMovingAverage(values, windowSize):
    movingAverages = []

    for w in rollingWindow(values, windowSize):
        movingAverages.append(sum(w)/len(w))

    return movingAverages

def getMinimums(values, windowSize):
    minimums = []

    for w in rollingWindow(values, windowSize):
        minimums.append(min(w))

    return minimums

def getMaximums(values, windowSize):
    maximums = []

    for w in rollingWindow(values, windowSize):
        maximums.append(max(w))

    return maximums

# ================================================================

def getTimeSeriesValues(values, window):
    movingAverages = getMovingAverage(values, window)
    minimums = getMinimums(values, window)
    maximums = getMaximums(values, window)
    returnData = []
    # build items of the form [[average, minimum, maximum], normalized price]
    for i in range(0, len(movingAverages)):
        inputNode = [movingAverages[i], minimums[i], maximums[i]]
        price = normalizePrice(values[len(movingAverages) - (i + 1)], minimums[i], maximums[i])
        outputNode = [price]
        tempItem = [inputNode, outputNode]
        returnData.append(tempItem)

    return returnData

# ================================================================

def getHistoricalData(stockSymbol):
    historicalPrices = []

    # login to API
    urlopen("http://api.kibot.com/?action=login&user=guest&password=guest")

    # get 14 days of data from API (business days only, could be < 10)
    url = "http://api.kibot.com/?action=history&symbol=" + stockSymbol + "&interval=daily&period=365&unadjusted=1&regularsession=1"
    apiData = urlopen(url).read().decode("utf-8").split("\n")
    #print apiData
    for line in apiData:
        if len(line) > 0:
            tempLine = line.split(',')
            price = float(tempLine[1])
            historicalPrices.append(price)

    return historicalPrices

# ================================================================


def getTrainingData(stockSymbol,term):

    historicalData = getHistoricalData(stockSymbol)

    # reverse it so we're using the most recent data first, ensure we only have 9 data points
    historicalData.reverse()
    #del historicalData[9:]

    # get five 5-day moving averages, 5-day lows, and 5-day highs, associated with the closing price
    trainingData = getTimeSeriesValues(historicalData, term)

    return trainingData

def getPredictionData(stockSymbol, term):
    historicalData = getHistoricalData(stockSymbol)

    # reverse it so we're using the most recent data first, then ensure we only have 5 data points
    historicalData.reverse()
    del historicalData[term:]

    # get five 5-day moving averages, 5-day lows, and 5-day highs
    predictionData = getTimeSeriesValues(historicalData, term)
    # remove associated closing price
    predictionData = predictionData[0][0]

    return predictionData

# ================================================================

def analyze_symbol(stockSymbol, term):
    startTime = time.time()

    trainingData = getTrainingData(stockSymbol, term)

    network = NeuralNetwork(inputNodes = 3, hiddenNodes = 3, outputNodes = 1)

    network.train(trainingData)

    # get rolling data for most recent day
    predictionData = getPredictionData(stockSymbol, term)

    # get prediction
    returnPrice = network.test(predictionData)

    # de-normalize and return predicted stock price
    predictedStockPrice = denormalizePrice(returnPrice, predictionData[1], predictionData[2])

    # create return object, including the amount of time used to predict
    #returnData = {}
    returnData= predictedStockPrice
    #returnData['time'] = time.time() - startTime

    return returnData

# ================================================================

def SVMpredict(filename):
    input_file = open(filename)
    X = []
    y = []
    for line in islice(input_file, 1, None):
        for line in islice(input_file, 1, None):
            tempLine = line.split(',')
            date = tempLine[0]
            date = datetime.strptime(date, "%Y-%m-%d")
            compare = '2017-04-24'
            compare = datetime.strptime(compare, "%Y-%m-%d")
            days = (date - compare).days
            X.append(days)
            tempLine = line.split(',')
            price = float(tempLine[1])
            y.append(price)
    # transfer form of data
    X = np.asarray(X)
    X = np.reshape(X, (len(X), 1))
    y = np.asarray(y)
    # data to predict
    temp = X[-1]
    predict_X = [temp + 1, temp + 2, temp + 3, temp + 4, temp + 5]
    svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
    svr_rbf.fit(X, y)
    # y_rbf = svr_rbf.predict(X)
    y_preRbf = svr_rbf.predict(predict_X)
    y_preRbf = np.around(y_preRbf, decimals=2)
    return [predict_X, y_preRbf]


if __name__ == "__main__":
    print(analyze_symbol("GOOG",5))
