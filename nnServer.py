import socket
import struct
import sys
from nn import getNN, activateNN
from data import Data

NN_INPUT_SIZE = int(sys.argv[1])
nnFilename = sys.argv[2]
dataFilename = sys.argv[3]

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

while True:
    dt = conn.recv(48)
    if not dt:
        break
    b = struct.unpack('qddddq', dt)
    data.appendBar(b[0], b[1], b[2], b[3], b[4], b[5])
    result = activateNN(nn, data, len(data) - NN_INPUT_SIZE, len(data))
    print 'add: ', b[0], ' result: ', result
    toSend = struct.pack('d', result)
    conn.send(toSend)

conn.close()
