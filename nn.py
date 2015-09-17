try:
    import cPickle as pickle
except ImportError:
    import pickle

from data import Data

from math import sqrt

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
    loss = 0.
    lossSize = 1.
    for n in range(iterations):
        dataSet = SupervisedDataSet(5 * N, 1)
        start = 1. * (len(data) - validationSize - 1 - N - predictionLength) / iterations * n
        end = 1. * (len(data) - validationSize - 1 - N - predictionLength) / iterations * (n + 1) - validationSize
        validation = end + validationSize
        start = int(start)
        end = int(end)
        validation = int(validation)
        for i in range(start, end):
            sample, mainValue = data.contiguousArray(i, i + N)
            output = data.normalizedMax(i + N + 1, i + N + predictionLength + 1, mainValue)
            dataSet.addSample(sample, (output,))
        print "iteration: ", n, " start: ", start, " end: ", end
        trainer = BackpropTrainer(nn, dataSet)
        trainer.train()
        dataSet.clear()
        for i in range(end, validation):
            sample, mainValue = data.contiguousArray(i, i + N)
            realOutput = data.max(i + N + 1, i + N + predictionLength + 1)
            nnOutputValue = nn.activate(sample)[0] + mainValue
            dt = data.date(i + N + 1)
            currentLoss = nnOutputValue - realOutput
            loss += currentLoss * currentLoss
            print '============================'
            print dt
            print "NN: ", "{0:.10f}".format(nnOutputValue), " Real: ", "{0:.10f}".format(realOutput)
            print "LOSS: ", "{0:.10f}".format(currentLoss)
            print "LOSS TOTAL: ", "{0:.10f}".format(sqrt(loss / lossSize))
            print '============================'
            lossSize += 1.

def trainUntilConvergence(nn, data, N, predictionLength):
    dataSet = SupervisedDataSet(5 * N, 1)
    start = 0
    end = 1 - N - predictionLength
    for i in range(start, end):
        sample, mainValue = data.contiguousArray(i, i + N)
        output = data.normalizedMax(i + N + 1, i + N + predictionLength + 1, mainValue)
        dataSet.addSample(sample, (output,))
    trainer = BackpropTrainer(nn, dataSet)
    trainer.trainUntilConvergence()
    dataSet.clear()

def activateNN(nn, data, start, end):
    sample, mainValue = data.contiguousArray(start, end)
    nnOutputValue = nn.activate(sample)[0] + mainValue
    return nnOutputValue