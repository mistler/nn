import sys
from optparse import OptionParser

from data import Data
from nn import getNN, saveNN, train, trainUntilConvergence

parser = OptionParser()
parser.add_option('-r', '--resume', dest='resume', action='store_true', default=False)
parser.add_option('-n', '--number', dest='N')
parser.add_option('-t', '--trained', dest='netFileName')
parser.add_option('-d', '--data', dest='dataFileName')
parser.add_option('-i', '--iterations', dest='iterations', default=200)
parser.add_option('-v', '--validation', dest='validation', default=1)
parser.add_option('-l', '--layers', dest='layers')
parser.add_option('-p', '--prediction', dest='prediction', default=3)
parser.add_option('-c', '--convergence', dest='convergence', action='store_true', default=False)

(options, args) = parser.parse_args()

print 'Building network...'
if options.resume:
    nn = getNN(True, options.netFileName)
else:
    layersString = str(int(options.N) * 5) + '.' + options.layers + '.1'
    layers = layersString.split('.')
    layers = [int(s) for s in layers]
    nn = getNN(False, layers)
print nn

print 'Loading data...'
data = Data(options.dataFileName)
print 'Data size: ', len(data)

if options.convergence:
    print 'Training until convergence...'
    trainUntilConvergence(nn, data, int(options.N), int(options.prediction))
else:
    print 'Training...'
    train(nn, data, int(options.N), int(options.prediction), int(options.iterations), int(options.validation))

print "saving nn..."
name = ''
for s in sys.argv[1:]:
    name += s
name += '.pkl'
saveNN(nn, name)

