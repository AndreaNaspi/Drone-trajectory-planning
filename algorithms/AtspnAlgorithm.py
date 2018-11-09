from algorithms import RootedTreeCoverAlgorithm, ChristofidesAlgorithm
from utility import DrawGraph


class AtspnAlgorithm:

    def computeAtspn(self):
        """Execute RTCP (Rooted Tree Cover Problem) approximation algorithm
           with a upper bound B at max edge cost (ignore upper bound)"""

        """Compute max edge cost"""
        maxEdge = max([data['weight'] for u, v, data in self.graph.edges(data=True)])

        """Execute RTCP"""
        rtcp = RootedTreeCoverAlgorithm.RootedTreeCoverAlgorithm(self.graph, maxEdge)
        rootedTrees = rtcp.computeRootedTreeCover()

        """For each rooted tree back to complete graph"""
        for tree in rootedTrees:
            """Iterate over the original graph and add missing edges"""
            for u, v, data in self.graph.edges(data=True):
                if (not tree.has_edge(u, v)) and (tree.has_node(u) and tree.has_node(v)):
                    tree.add_edge(u, v, weight=data['weight'])

            """Compute christofides and plot the paths"""
            christofides = ChristofidesAlgorithm.ChristofidesAlgorithm(tree)
            tour = christofides.computeChristofides()

            """Insert label in the tour graph from the original tree"""
            for node, data in tree.nodes(data=True):
                    tour.add_node(node, label=data['label'])

            """Plot the tour"""
            plot = DrawGraph.DrawGraph()
            plot.drawGraphKamada(tour, True, 'r', 'b')

    def __init__(self, graph):
        self.graph = graph