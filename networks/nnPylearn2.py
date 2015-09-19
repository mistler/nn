import numpy as np
import theano
from pylearn2.datasets.dense_design_matrix import DenseDesignMatrix


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
        self.ds = NeuralNetwork.TrainingDataset(self.data, self.N, self.predictionLength)
        self.trainer.setup(self.nn, self.ds)


    def train(self):
        while True:
            self.trainer.train(dataset=self.ds)
            self.nn.monitor.report_epoch()
            self.nn.monitor()
            if not self.trainer.continue_learning(self.nn):
                break


    def predict(self, start, end):
        sample, mainValue = self.data.contiguousArray(start, end)
        inputs = np.array([sample, ])
        nnOutputValue = self.nn.fprop(theano.shared(inputs, name='inputs')).eval() + mainValue
        return nnOutputValue