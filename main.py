import sys
from optparse import OptionParser
try:
    import cPickle as pickle
except ImportError:
    import pickle


from data import Data

parser = OptionParser()
parser.add_option('-r', '--resume', dest='resume', action='store_true', default=False)
parser.add_option('-d', '--data', dest='dataFileName')
parser.add_option('-i', '--iterations', dest='iterations', default=200)
parser.add_option('-v', '--validation', dest='validation', default=1)
parser.add_option('-n', '--network', dest='network')
parser.add_option('-p', '--prediction', dest='prediction', default=3)

(options, args) = parser.parse_args()


print 'Building network...'
if options.resume:
    print 'Resume training'
    with open(options.network, 'rb') as f:
        nn = pickle.load(f)
else:
    print 'Loading data...'
    data = Data(options.dataFileName)
    print 'Data size: ', len(data)
    import importlib
    networkClass = importlib.import_module('Network', package='networks.' + options.network)
    nn = networkClass(data)

print 'Training...'
nn.train()

print "saving nn..."
name = ''
for s in sys.argv[1:]:
    name += s
name += '.pkl'
with open(name, 'w') as f:
    pickle.dump(nn, f)

