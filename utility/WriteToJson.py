import json
from random import seed, randint


class WriteToJson:

    def writeLists(self):
        """Convert lists to dict and write it to file jsonFile"""
        with open(self.jsonFile, 'w') as outFile:
            """Create a new dict with two empty list"""
            newDict = {'depot': [], 'pointOfInterest': []}

            """Fill the depot list with the elements in listDepot"""
            for depot in self.listDepot:
                newDict['depot'].append({'latitude': depot[0], 'longitude': depot[1], 'delay': randint(1, 11)})

            """Fill the pointOfInterest list with the elements in listPoints"""
            for point in self.listPoints:
                newDict['pointOfInterest'].append({'latitude': point[0], 'longitude': point[1]})

            """Write dict to json"""
            self.writeDict(newDict, outFile)

    @staticmethod
    def writeDict(actualDict, outFile):
        """Write a dict to file outFile"""
        json.dump(actualDict, outFile)

    def __init__(self, jsonFile, listDepot, listPoints):
        """Write the generated depot and points of interest to the file jsonFile"""
        self.jsonFile = jsonFile
        self.listDepot = listDepot
        self.listPoints = listPoints

        """Set seed"""
        seed(600)
