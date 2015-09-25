import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from data import Data
import sys


dataFile = sys.argv[1]
data = Data(dataFile)

resultUp = [0. for _ in range(1000)]
resultDown = [0. for _ in range(1000)]

def addValue(counter, up):
    if up:
        for i in range(1, counter + 1):
            resultUp[i] += 1.
    else:
        for i in range(1, counter + 1):
            resultDown[i] += 1.

counter = 1
up = True
for i in range(len(data)):
    if up:
        if data[i].white():
            counter += 1
        else:
            addValue(counter, up)
            up = False
            counter = 1
    else:
        if not data[i].white():
            counter += 1
        else:
            addValue(counter, up)
            up = True
            counter = 1

print 'up'
for i in range(1, 99):
    if resultUp[i + 1] < 10:
        break;
    print i, ':', resultUp[i + 1], ';', resultUp[i + 1] / resultUp[i] * 100.

print 'down'
for i in range(1, 99):
    if resultDown[i + 1] < 10:
        break;
    print i, ':', resultDown[i + 1], ';', resultDown[i + 1] / resultDown[i] * 100.