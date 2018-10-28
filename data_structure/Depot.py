from data_structure import NetworkPoint


class Depot(NetworkPoint.NetworkPoint):

    def __init__(self, latitude, longitude, delay=0):
        super().__init__(latitude, longitude)
        self.latitude = latitude
        self.longitude = longitude
        self.delay = delay

    def getDelay(self):
        return self.delay

    def setDelay(self, newDelay):
        self.delay = newDelay
