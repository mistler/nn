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

print 'waiting for connection...'

sock = socket.socket()
sock.bind(('', 1488))
sock.listen(1)
conn, addr = sock.accept()

print 'connected: ', addr

NN_INPUT_SIZE = struct.unpack('i', conn.recv(4))[0]
print 'NN_INPUT_SIZE: ', NN_INPUT_SIZE

while True:
    dt = conn.recv(48)
    if not dt:
        break
    b = struct.unpack('qddddq', dt)
    data.appendBar(b[0], b[1], b[2], b[3], b[4], b[5])
    sample, mainValue, averageBar = data.contiguousArray(len(data) - NN_INPUT_SIZE, len(data))
    low, high = nn.activate(sample) * averageBar + mainValue
    toSend = struct.pack('dd', low, high)
    conn.send(toSend)

conn.close()
