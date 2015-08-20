import cPickle as pickle
from data import Data

from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer


def getNN(loadFromFile, arg):
    if loadFromFile:
        with open(arg, 'rb') as f:
            nn = pickle.load(f)
    else:
        nn = buildNetwork(*arg)
    return nn

def saveNN(nn, filename):
    with open(filename, 'w') as f:
        pickle.dump(nn, f)

def train(nn, data, N, predictionLength, iterations, validationSize):
    highLoss = 0.
    lowLoss = 0.
    lossSize = 1.
    for n in range(iterations):
        dataSet = SupervisedDataSet(5 * N, 2)
        start = 1. * (len(data) - validationSize - 1 - N - predictionLength) / iterations * n
        end = 1. * (len(data) - validationSize - 1 - N - predictionLength) / iterations * (n + 1) - validationSize
        validation = end + validationSize
        start = int(start)
        end = int(end)
        validation = int(validation)
        for i in range(start, end):
            sample, mainValue, averageBar = data.contiguousArray(i, i + N)
            output1 = data.normalizedMin(i + N + 1, i + N + predictionLength + 1, mainValue)
            output2 = data.normalizedMax(i + N + 1, i + N + predictionLength + 1, mainValue)
            dataSet.addSample(sample, (output1, output2))
        print "iteration: ", n, " start: ", start, " end: ", end
        trainer = BackpropTrainer(nn, dataSet)
        trainer.train()
        dataSet.clear()
        for i in range(end, validation):
            sample, mainValue, averageBar = data.contiguousArray(i, i + N)
            output1 = data.min(i + N + 1, i + N + predictionLength + 1)
            output2 = data.max(i + N + 1, i + N + predictionLength + 1)
            low, high = nn.activate(sample) * averageBar + mainValue
            dt = data.date(i + N + 1)
            currentHighLoss = high - output2
            currentLowLoss = low - output1
            highLoss += currentHighLoss
            lowLoss += currentLowLoss
            print '============================'
            print dt
            print "Spread: ", "{0:.10f}".format(output2 - output1)
            print "Predct: ", "{0:.10f}".format(high - low)
            print "L: ", "{0:.10f}".format(low), " H: ", "{0:.10f}".format(high)
            print "A: ", "{0:.10f}".format(output1), " A: ", "{0:.10f}".format(output2)
            print "LOSS low: ", "{0:.10f}".format(currentLowLoss), " high: ", "{0:.10f}".format(currentHighLoss)
            print "LOSS TOTAL low: ", "{0:.10f}".format(lowLoss / lossSize * 2.), " high: ", "{0:.10f}".format(highLoss / lossSize * 2.)
            print "LOSS TOTAL: ", "{0:.10f}".format((lowLoss + highLoss) / lossSize)
            print '============================'
            lossSize += 1.