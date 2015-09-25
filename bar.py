class Bar:


    def __init__(self, datetime, op, lo, hi, cl, vl):
        self.datetime = datetime
        self.open = op
        self.low = lo
        self.high = hi
        self.close = cl
        self.volume = vl

    def shift(self, value):
        self.open += value
        self.low += value
        self.high += value
        self.close += value
        self.volume += value

    def multiply(self, value):
        self.open *= value
        self.low *= value
        self.high *= value
        self.close *= value
        self.volume *= value

    def volumeMultiply(self, value):
        self.volume *= value

    def white(self):
        return self.close > self.open
