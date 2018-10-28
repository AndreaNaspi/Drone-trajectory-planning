from math import sin, cos, sqrt, atan2, radians


class NetworkPoint:

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def getLatitude(self):
        return self.latitude

    def setLatitude(self, newLatitude):
        self.latitude = newLatitude

    def getLongitude(self):
        return self.longitude

    def setLongitude(self, newLongitude):
        self.longitude = newLongitude

    @staticmethod
    def getDistance(point1, point2):
        """Haversine formula to calculate the distance between two points"""

        """Convert in radians"""
        lat1 = radians(point1.getLatitude())
        lon1 = radians(point1.getLongitude())
        lat2 = radians(point2.getLatitude())
        lon2 = radians(point2.getLongitude())
        d_lon = lon2 - lon1
        d_lat = lat2 - lat1

        """Approximate radius of earth in km"""
        R = 6373.0

        """Apply the formula"""
        a = sin(d_lat / 2)**2 + cos(lat1) * cos(lat2) * sin(d_lon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        """Get the distance between point1 and point2"""
        distance = R * c

        return distance