from pylearn2.models import mlp
from pylearn2.training_algorithms import sgd
from pylearn2.termination_criteria import EpochCounter

from nnPylearn2 import NeuralNetwork


class SimpleOneHidden5(NeuralNetwork):
    def __init__(self, data):
        self.N = 5
        self.predictionLength = 2
        # create hidden layer with 2 nodes, init weights in range -0.1 to 0.1 and add
        # a bias with value 1
        hidden_layer = mlp.Sigmoid(layer_name='hidden', dim=25, irange=.1, init_bias=1.)
        # create Softmax output layer
        output_layer = mlp.Softmax(1, 'output', irange=.1)
        # create Stochastic Gradient Descent trainer that runs for 400 epochs
        trainer = sgd.SGD(learning_rate=.05, batch_size=10, termination_criterion=EpochCounter(10))
        layers = [hidden_layer, output_layer]
        # create neural net that takes two inputs
        nn = mlp.MLP(layers, nvis=self.N)
        super(self.__class__, self).__init__(data, nn, trainer)