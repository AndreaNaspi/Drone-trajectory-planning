import networkx as nx
from random import uniform
from data_structure import Depot, PointOfInterest
from algorithms import KruskalAlgorithm
from utility import DrawGraph


class RootedTreeCoverAlgorithm:

    def generateContractingGraph(self):
        contractingGraph = nx.Graph()

        """Add the single depot root at random location with delay 0 (no interest on location and delay data)"""
        singleDepotRoot = Depot.Depot(uniform(-90.000000000, 90.000000000), uniform(-180.000000000, 180.000000000), 0)
        contractingGraph.add_node(singleDepotRoot, label="r")

        """Insert point of interest nodes (no change prom previous graph)"""
        pointOfInterestNodes = [(node, data) for node, data in self.originalGraph.nodes(data=True) if type(node) == PointOfInterest.PointOfInterest]
        contractingGraph.add_nodes_from(pointOfInterestNodes)

        """Add edges from point of interest to point of interest (no change from previous graph)"""
        pointOfInterestEdges = [(v, u) for v, u in self.originalGraph.edges if ((type(v) == PointOfInterest.PointOfInterest)
                                                                    & (type(u) == PointOfInterest.PointOfInterest))]
        contractingGraph.add_edges_from(pointOfInterestEdges)

        """For each edge from point of interest to a depot induces a new edge to the single depot root"""
        """Iterate over each edge to a depot in previous graph"""
        for v, u, data in self.originalGraph.edges(data=True):
            if (type(v) == PointOfInterest.PointOfInterest) & (type(u) == Depot.Depot):
                """Find min edge cost from v to a generic depot"""
                edgesToDepot = [edge for edge in self.originalGraph.edges(data=True) if ((edge[0] == v) & (type(edge[1]) == Depot.Depot))]
                minEdge = min(edgesToDepot, key=lambda edge: edge[-1]['weight'])

                """Finally add edge from v to single depot root with this min weight"""
                contractingGraph.add_edge(v, singleDepotRoot, weight=minEdge[-1]['weight'])
            else:
                continue

        return contractingGraph

    def generateUncontractingGraph(self, contractingGraph):
        """Compute uncontracting graph (uncontract single depot root to multiple depot) from MST of contracting graph"""

        """Back to directed graph"""
        uncontractingGraph = nx.DiGraph()

        """Add all point of interest nodes"""
        pointOfInterestNodes = [(node, data) for node, data in contractingGraph.nodes(data=True) if type(node) == PointOfInterest.PointOfInterest]
        uncontractingGraph.add_nodes_from(pointOfInterestNodes)

        """Add all depot nodes from original graph"""
        depotNodes = [(node, data) for node, data in self.originalGraph.nodes(data=True) if type(node) == Depot.Depot]
        uncontractingGraph.add_nodes_from(depotNodes)

        """Add all edges (if exist) from point of interest to point of interest"""
        pointOfInterestEdges = [(v, u) for v, u in contractingGraph.edges if ((type(v) == PointOfInterest.PointOfInterest) & (type(u) == PointOfInterest.PointOfInterest))]
        uncontractingGraph.add_edges_from(pointOfInterestEdges)

        """Map the edges to single depot root into multiple depot"""
        for u, v, data in [edge for edge in contractingGraph.edges(data=True) if ((type(edge[0]) == Depot.Depot) & (type(edge[1]) == PointOfInterest.PointOfInterest))]:
            """Search in original graph the edge with this weight and map this edge to that depot 
               (only one edge have this property!)"""
            matchingEdgeWeight = [edge for edge in self.originalGraph.edges(data=True) if edge[-1]['weight'] == data['weight']][0]
            uncontractingGraph.add_edge(matchingEdgeWeight[1], matchingEdgeWeight[0], weight=data['weight'])

        return uncontractingGraph

    def computeRootedTreeCover(self):
        """Compute the RTCP (Rooted Tree Cover Problem) 4+epsilon approximation algorithm with edge upper bound B"""

        """Remove edge greater than B"""
        removeEdge = []
        for edge in self.originalGraph.edges(data=True):
            if edge[-1]['weight'] >= self.b:
                removeEdge.append(edge[:2])
        self.originalGraph.remove_edges_from(removeEdge)

        """Instantiate plot object"""
        plot = DrawGraph.DrawGraph()

        """Compute contracting graph with single depot root"""
        contractingGraph = self.generateContractingGraph()
        plot.drawGraphKamada(contractingGraph, False, 'g', 'b')

        """Compute MST of contracting graph with Kruskal Algorithm"""
        kruskal = KruskalAlgorithm.KruskalAlgorithm(contractingGraph)
        mstContractingGraph = kruskal.computeKruskal()
        plot.drawGraphKamada(mstContractingGraph, True, 'g', 'b')

        """Uncontracting the contracting graph after the Kruskal application"""
        uncontractingGraph = self.generateUncontractingGraph(mstContractingGraph)
        plot.drawGraphKamada(uncontractingGraph, True, 'r', 'b')

        """Generate single tree for each depot"""
        depotRoot = []
        for root in [root for root in uncontractingGraph.nodes if type(root) == Depot.Depot]:
            depotRoot.append(nx.DiGraph(uncontractingGraph.edge_subgraph(list(nx.dfs_edges(uncontractingGraph, root)))))

        return depotRoot

    def __init__(self, graph, b):
        self.originalGraph = graph
        self.b = b