import numpy as np
import theano
from pylearn2.datasets.dense_design_matrix import DenseDesignMatrix

from math import sqrt

from data import Data

class NeuralNetwork:
    class TrainingDataset(DenseDesignMatrix):
        def __init__(self, data, N, predictionLength):
            start = 0
            end = len(data) - N - predictionLength
            X = []
            y = []
            for i in range(start, end):
                sample, mainValue = data.contiguousArray(i, i + N)
                output = data.normalizedMax(i + N, i + N + predictionLength, mainValue)
                X.append(sample)
                y.append([output,])
            X = np.array(X)
            y = np.array(y)
            super(NeuralNetwork.TrainingDataset, self).__init__(X=X, y=y)

    def __init__(self, data, nn, trainer):
        self.data = data
        self.nn = nn
        self.trainer = trainer
        self.dataLength = self.N / 5

    def train(self):
        ds = NeuralNetwork.TrainingDataset(self.data, self.dataLength, self.predictionLength)
        self.trainer.setup(self.nn, ds)
        while True:
            self.trainer.train(dataset=ds)
            self.nn.monitor.report_epoch()
            self.nn.monitor()
            if not self.trainer.continue_learning(self.nn):
                break


    def predict(self, start, end):
        sample, mainValue = self.data.contiguousArray(start, end)
        inputs = np.array([sample, ])
        nnOutputValue = self.nn.fprop(theano.shared(inputs, name='inputs')).eval() + mainValue
        return nnOutputValue

    def validate(self):
        size = len(self.data)
        stride = size / 25.
        loss = 0.
        lossSize = 1.
        for i in range(0, size, stride):
            sample, mainValue = self.data.contiguousArray(i, i + self.dataLength)
            realOutput = self.data.max(i + self.dataLength + 1, i + self.dataLength + self.predictionLength + 1)
            inputs = np.array([sample, ])
            nnOutputValue = self.nn.fprop(theano.shared(inputs, name='inputs')).eval() + mainValue
            dt = self.data.date(i + self.dataLength + 1)
            currentLoss = nnOutputValue - realOutput
            loss += currentLoss * currentLoss
            print '============================'
            print dt
            print "NN: ", "{0:.10f}".format(nnOutputValue), " Real: ", "{0:.10f}".format(realOutput)
            print "LOSS: ", "{0:.10f}".format(currentLoss)
            print "LOSS TOTAL: ", "{0:.10f}".format(sqrt(loss / lossSize))
            print '============================'
            lossSize += 1.