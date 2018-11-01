import json
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from data_structure import NetworkPoint, Depot, PointOfInterest
from utility import GenerateLatLong
from algorithms import RootedTreeCoverAlgorithm


class Main:

    def importFromFile(self, file):
        """Load data from a json file in the path 'file' """
        with open(file, 'r') as readFile:
            data = json.load(readFile)
            listDepot = data["depot"]
            listPointOfInterest = data["pointOfInterest"]

            """Generate depot nodes"""
            self.numberOfDepot = len(listDepot)
            for depot in listDepot:
                newNode = Depot.Depot(depot["latitude"], depot["longitude"], depot["delay"])
                self.listDepot.append(newNode)
                self.graph.add_node(newNode)

            """Generate point of interest nodes"""
            self.numberOfPoints = len(listPointOfInterest)
            for point in listPointOfInterest:
                newNode = PointOfInterest.PointOfInterest(point["latitude"], point["longitude"])
                self.listPoints.append(newNode)
                self.graph.add_node(newNode)

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

    def drawGraphKamada(self):
        """Plot graph in kamada layout"""

        """Create a dictionary with latitude/longitude values for each nodes"""
        dictPos = {}
        for node in self.graph.nodes:
            dictPos[node] = (node.getLatitude(), node.getLongitude())

        """Plot the graph"""
        pos = nx.kamada_kawai_layout(self.graph, dictPos)
        nx.draw_networkx_nodes(self.graph, pos, nodelist=self.listDepot, node_color='r')
        nx.draw_networkx_nodes(self.graph, pos, nodelist=self.listPoints, node_color='b')
        nx.draw_networkx_edges(self.graph, pos,
                               edgelist=[edge for edge in self.graph.edges if type(edge[0]) == Depot.Depot])
        plt.axis('off')
        plt.draw()
        plt.show()

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
        self.adjMatrix = np.zeros((self.numberOfDepot + self.numberOfPoints, self.numberOfDepot + self.numberOfPoints))
        self.setEdges()

        """Plot the initial graph in kamada layout"""
        self.drawGraphKamada()

        """Execute RTCP (Rooted Tree Cover Problem) approximation algorithm 
           with a upper bound B at max edge cost (ignore upper bound)"""

        """Compute max edge cost"""
        maxEdge = max([data['weight'] for u, v, data in self.graph.edges(data=True)])
        """Execute RTCP"""
        rtcp = RootedTreeCoverAlgorithm.RootedTreeCoverAlgorithm(self.graph, maxEdge)
        rootedGraphs = rtcp.computeRootedTreeCover()


"""Testing"""
instance = Main(uniqueSpeed=1.5, fromFile="data.json")
