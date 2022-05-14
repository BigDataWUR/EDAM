class Measurement(object):
    def __init__(self, value, timestamp=None, observable=None,
                 uom=None, station=None, junction=None):
        self.value = value
        self.timestamp = timestamp
        self.observable = observable
        self.uom = uom
        self.station = station
        self.junction = junction

    def __repr__(self):
        return f"{self.value}"
