import socket
import struct
import sys
try:
    import cPickle as pickle
except ImportError:
    import pickle

nnFilename = sys.argv[1]

print 'Loading nn...'

with open(nnFilename, 'rb') as f:
    nn = pickle.load(f)

print 'Waiting for connection...'

sock = socket.socket()
sock.bind(('', 1488))
sock.listen(1)
conn, addr = sock.accept()

print 'Connected: ', addr

while True:
    dt = conn.recv(48)
    if not dt:
        break
    b = struct.unpack('qddddq', dt)
    nn.data.appendBar(b[0], b[1], b[2], b[3], b[4], b[5])
    result = nn.predict(len(nn.data) - nn.dataLength, len(nn.data))
    print 'add: ', b[0], ' result: ', result
    toSend = struct.pack('d', result)
    conn.send(toSend)

conn.close()
