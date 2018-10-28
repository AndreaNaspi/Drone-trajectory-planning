from math import pi, sqrt, cos, sin
from random import seed, random, uniform


from utility import WriteToJson


class GenerateLatLong:

    @staticmethod
    def generatePoint(radius, x0, y0):
        """Generate a single point with latitude and longitude in a certain radius (meters) around a location (x0,y0)"""

        "Generate two random variables in [0,1)"
        u = random()
        v = random()

        "Convert radius in degrees from meters"
        radiusInDegrees = radius / 111300

        "Generate points"
        w = radiusInDegrees * sqrt(u)
        t = 2 * pi * v
        x = w * cos(t)
        y = w * sin(t)

        "Adjust the x-coordinate for the shrinking of the east-west distances"
        new_x = x / cos(y0)

        "Return the random point"
        return new_x + x0, y + y0

    def __init__(self, radius, numberOfDepot, numberOfPoint, file):
        """"Generate a certain number of depot and a certain number of points in a certain radius (meters). After the execution
        write the data in the file data.json"""
        self.radius = radius
        self.numberOfDepot = numberOfDepot
        self.numberOfPoints = numberOfPoint

        "Set random seed"
        seed(600)

        "Generate start point latitude, longitude"
        startLatitude = uniform(-90.000000000, 90.000000000)
        startLongitude = uniform(-180.000000000, 180.000000000)

        "Generate the depots"
        self.listDepot = []
        for i in range(numberOfDepot):
            x, y = self.generatePoint(radius, startLatitude, startLongitude)
            self.listDepot.append((x, y))

        "Generate the points of interest"
        self.listPoints = []
        for j in range(numberOfPoint):
            x, y = self.generatePoint(radius, startLatitude, startLongitude)
            self.listPoints.append((x, y))

        "Write the lists in data.json file"
        writer = WriteToJson.WriteToJson(file, self.listDepot, self.listPoints)
        writer.writeLists()
