import networkx as nx
from . import KruskalAlgorithm


class ChristofidesAlgorithm:

    @staticmethod
    def minimumWeightedMatching(mst, graph, odd_vert):
        """Utility function that adds minimum weight matching edges to MST"""
        while odd_vert:
            v = odd_vert.pop()
            weight = float("inf")
            closest = 0
            for u in odd_vert:
                if graph[v][u]['weight'] < weight:
                    weight = graph[v][u]['weight']
                    closest = u
            mst.add_edge(v, closest, weight=weight)
            odd_vert.remove(closest)

    """Function that perform Christofides approximation algorithm"""
    def computeChristofides(self):

        opGraph = nx.DiGraph()

        """Generate minimum spanning tree of graph G with Kruskal Algorithm"""
        kruskalAlgorithm = KruskalAlgorithm.KruskalAlgorithm(self.graph)
        MST = kruskalAlgorithm.computeKruskal()

        """List containing the vertices with odd degree"""
        odd_vert = []
        for i in MST.nodes():
            """If the degree of the vertex is odd, then append it to odd vertex list"""
            if MST.degree(i) % 2 != 0:
                odd_vert.append(i)

        """Adds minimum weight matching edges to MST"""
        self.minimumWeightedMatching(MST, self.graph, odd_vert)

        """Now MST has the Eulerian circuit"""
        start = list(MST.nodes())[0]
        visited = [False] * len(MST.nodes())

        """Finds the hamiltonian circuit"""
        curr = start
        nextNode = None
        visited[list(MST.nodes).index(curr)] = True
        for nd in MST.neighbors(curr):
            if visited[list(MST.nodes).index(nd)] == False or nd == start:
                nextNode = nd
                break
        while nextNode != start:
            visited[list(MST.nodes).index(nextNode)] = True
            opGraph.add_edge(curr, nextNode, weight=self.graph[curr][nextNode]['weight'])

            """Finding the shortest Eulerian path from MST"""
            curr = nextNode
            for nd in MST.neighbors(curr):
                if not visited[list(MST.nodes).index(nd)]:
                    nextNode = nd
                    break
            if nextNode == curr:
                for nd in self.graph.neighbors(curr):
                    if not visited[list(MST.nodes).index(nd)]:
                        nextNode = nd
                        break
            if nextNode == curr:
                nextNode = start
        opGraph.add_edge(curr, nextNode, weight=self.graph[curr][nextNode]['weight'])

        """return optimal_dist"""
        return opGraph

    def __init__(self, graph):
        self.graph = graph
