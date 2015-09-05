from nn import getNN
from data import Data

nnFilename = "-n5-dEURUSD.hst-12.pkl"
dataFilename = "EURUSD.hst"

nn = getNN(True, nnFilename)
data = Data(dataFilename)

averageVolume = data.averageVolume()
averageBarSize = data.averageBarSize();

def normalizeData(self, sample):
	mainValue = (sample[3] + sample[0]) / 2.
	for i in range(len(sample)):
		if i != 0 and (i % 4) == 0:
			sample[i] = sample[i] / averageVolume
		else:
			sample[i] = (sample[i] - mainValue) / averageBarSize
	return sample, mainValue


def predict(list):
	sample, mainValue = normalizeData(list)
	low, high = nn.activate(sample) * averageBarSize + mainValue
	return (low, high)