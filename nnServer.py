import socket
import struct
from nn import getNN
from data import Data


nnFilename = "-n5-dEURUSD.hst-l2.pkl"
dataFilename = "EURUSD.hst"

print 'loading data and nn...'

nn = getNN(True, nnFilename)
data = Data(dataFilename)

averageVolume = data.getAverageVolume()
averageBarSize = data.getAverageBarSize();


def normalizeData(sample):
    mainValue = (sample[3] + sample[0]) / 2.
    result = []
    for i in range(len(sample)):
        if (i % 5) == 4:
            result.append(sample[i] / averageVolume)
        else:
            result.append((sample[i] - mainValue) / averageBarSize)
    return result, mainValue


def predict(list):
    sample, mainValue = normalizeData(list)
    low, high = nn.activate(sample)
    low = low * averageBarSize + mainValue
    high = high * averageBarSize + mainValue
    return low, high



print 'waiting for connection...'

sock = socket.socket()
sock.bind(('', 1488))
sock.listen(1)
conn, addr = sock.accept()

print 'connected: ', addr

NN_INPUT_SIZE = struct.unpack('i', conn.recv(4))[0]
print 'NN_INPUT_SIZE: ', NN_INPUT_SIZE


while True:
    dt = conn.recv(NN_INPUT_SIZE * 8)
    if not dt:
        break
    sample = struct.unpack('d' * NN_INPUT_SIZE, dt)
    normalizeData(sample)
    low, high = predict(sample)
    print 'low: ', low, ' high: ', high
    toSend = struct.pack('dd', low, high)
    conn.send(toSend)

conn.close()
