import json
import networkx as nx
from data_structure import NetworkPoint, Depot, PointOfInterest
from utility import GenerateLatLong, DrawGraph
from algorithms import AtspnAlgorithm
from string import ascii_lowercase


class Main:

    def importFromFile(self, file):
        """Load data from a json file in the path 'file' """
        with open(file, 'r') as readFile:
            data = json.load(readFile)
            listDepot = data["depot"]
            listPointOfInterest = data["pointOfInterest"]

            """Generate depot nodes"""
            self.numberOfDepot = len(listDepot)
            for index, depot in enumerate(listDepot):
                newNode = Depot.Depot(depot["latitude"], depot["longitude"], depot["delay"])
                self.listDepot.append(newNode)
                self.graph.add_node(newNode, label=ascii_lowercase[index])

            """Generate point of interest nodes"""
            self.numberOfPoints = len(listPointOfInterest)
            for index, point in enumerate(listPointOfInterest):
                newNode = PointOfInterest.PointOfInterest(point["latitude"], point["longitude"])
                self.listPoints.append(newNode)
                self.graph.add_node(newNode, label=index+1)

    def setEdges(self):
        """Generate edges from depot to other nodes"""
        for depot in self.listDepot:
            for otherNode in self.graph.nodes:
                if depot != otherNode:
                    weight = NetworkPoint.NetworkPoint.getDistance(depot, otherNode)
                    if type(otherNode) == PointOfInterest.PointOfInterest:
                        weight += (self.uniqueSpeed * depot.getDelay())
                    self.graph.add_edge(depot, otherNode, weight=weight)

        """Generate edges from point fo interest to other nodes"""
        for point in self.listPoints:
            for otherNode in self.graph.nodes:
                if point != otherNode:
                    weight = NetworkPoint.NetworkPoint.getDistance(point, otherNode)
                    self.graph.add_edge(point, otherNode, weight=weight)

    def __init__(self, uniqueSpeed, numberOfDepot=None, numberOfPoints=None, fromFile=""):
        """Generate the graph from a json file or generate random values for depot and point of interest
           (size based on the numbers in input) in the file data.json """
        self.numberOfDepot = numberOfDepot
        self.listDepot = []
        self.numberOfPoints = numberOfPoints
        self.listPoints = []
        self.uniqueSpeed = uniqueSpeed
        self.graph = nx.DiGraph()

        if fromFile != "":
            self.importFromFile(fromFile)
        else:
            GenerateLatLong.GenerateLatLong(2000, numberOfDepot, numberOfPoints, "data.json")
            self.importFromFile("data.json")

        """After import the nodes set the weight of the edges (complete graph!)"""
        self.setEdges()

        """Plot the initial graph in kamada layout"""
        plot = DrawGraph.DrawGraph()
        plot.drawGraphKamada(self.graph, highlightEdge=False, depot_color='r', point_color='b')

        """Compute ATSPN algorithm"""
        atspn = AtspnAlgorithm.AtspnAlgorithm(self.graph)
        atspn.computeAtspn()


"""Testing"""
instance = Main(uniqueSpeed=1.5, fromFile='data.json')
