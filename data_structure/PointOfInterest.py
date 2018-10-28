from data_structure import NetworkPoint


class PointOfInterest(NetworkPoint.NetworkPoint):

    def __init__(self, latitude, longitude):
        super().__init__(latitude, longitude)
        self.latitude = latitude
        self.longitude = longitude
