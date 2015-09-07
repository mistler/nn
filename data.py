import struct
import datetime
from bar import Bar

class Data:

    def __init__(self, filename):
        self.filename = filename
        self.data = []
        self.readData()
        self.averageVolume = 0.
        self.averageBarSize = 0.
        for d in self.data:
            self.averageBarSize += d.high - d.low
            self.averageVolume += d.volume
        self.averageVolume /= len(self.data)
        self.averageBarSize /= len(self.data)

    def __len__(self):
        return len(self.data)

    def data(self):
        return self.data

    def array(self, start, end):
        return self.data[start: end]

    def contiguousArray(self, start, end):
        array = []
        subArray = self.data[start: end]
        mainValue = (subArray[0].high + subArray[0].low) / 2.
        for i in range(end - start):
            tmp = subArray[i]
            array.append((tmp.low - mainValue) / self.averageBarSize)
            array.append((tmp.open - mainValue) / self.averageBarSize)
            array.append((tmp.close - mainValue) / self.averageBarSize)
            array.append((tmp.high - mainValue) / self.averageBarSize)
            array.append(tmp.volume / self.averageVolume)
        return array, mainValue, self.averageBarSize

    def getAverageBarSize(self):
        return self.averageBarSize

    def getAverageVolume(self):
        return self.averageVolume

    def normalizedMin(self, start, end, average):
        min = 1000000.
        for b in self.data[start: end]:
            if b.low < min:
                min = b.low
        return (min - average) / self.averageBarSize

    def normalizedMax(self, start, end, average):
        max = 0.
        for b in self.data[start: end]:
            if b.high > max:
                max = b.high
        return (max - average) / self.averageBarSize

    def min(self, start, end):
        min = 1000000.
        for b in self.data[start: end]:
            if b.low < min:
                min = b.low
        return min

    def max(self, start, end):
        max = 0.
        for b in self.data[start: end]:
            if b.high > max:
                max = b.high
        return max

    def date(self, index):
        return datetime.datetime.fromtimestamp(self.data[index].datetime).strftime('%m-%d %H:%M:%S')

    def readData(self):
        with open(self.filename, 'rb') as f:
            header = f.read(148)
            while 1:
                first = f.read(4)
                if not first:
                    break
                datetime = struct.unpack('I', first)[0]
                tmp = struct.unpack('ddddq', f.read(40))

                bar = Bar(datetime, tmp[0], tmp[1], tmp[2], tmp[3], tmp[4])
                self.data.append(bar)

    def appendBar(self, datetime, lo, op, cl, hi, vl):
        bar = Bar(datetime, lo, op, cl, hi, vl)
        if self.data[len(data) - 1].datetime == datetime:
            self.data.pop()
        self.data.append(bar)

    def remove(self):
        self.data.pop()
