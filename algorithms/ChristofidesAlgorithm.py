import networkx as nx
import matplotlib.pyplot as plt
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

    """Function that perform Christofides algorithm"""
    def christofides(self, pos):

        opGraph = nx.DiGraph()

        """Generate minimum spanning tree of graph G with Kruskal Algorithm"""
        kruskalAlgorithm = KruskalAlgorithm.KruskalAlgorithm(self.graph)
        MST = kruskalAlgorithm.kruskal()

        """List containing the vertices with odd degree"""
        odd_vert = []
        for i in MST.nodes():
            """If the degree of the vertex is odd, then append it to odd vertex list"""
            if MST.degree(i) % 2 != 0:
                odd_vert.append(i)

        """Adds minimum weight matching edges to MST"""
        self.minimumWeightedMatching(MST, self.graph, odd_vert)
        """Now MST has the Eulerian circuit"""
        start = MST.nodes()[0]
        visited = [False] * len(MST.nodes())

        """Finds the hamiltonian circuit"""
        curr = start
        nextNode = None
        visited[curr] = True
        for nd in MST.neighbors(curr):
            if visited[nd] == False or nd == start:
                nextNode = nd
                break
        while nextNode != start:
            visited[nextNode] = True
            opGraph.add_edge(curr, nextNode, length=self.graph[curr][nextNode]['weight'])
            nx.draw_networkx_edges(self.graph, pos, arrows=True, edgelist=[(curr, nextNode)],
                                   width=2.5, alpha=0.6, edge_color='g')
            """Finding the shortest Eulerian path from MST"""
            curr = nextNode
            for nd in MST.neighbors(curr):
                if not visited[nd]:
                    nextNode = nd
                    break
            if nextNode == curr:
                for nd in self.graph.neighbors(curr):
                    if not visited[nd]:
                        nextNode = nd
                        break
            if nextNode == curr:
                nextNode = start
        opGraph.add_edge(curr, nextNode, length=self.graph[curr][nextNode]['weight'])
        nx.draw_networkx_edges(self.graph, pos, edgelist=[(curr, nextNode)], width=2.5, alpha=0.6, edge_color='g')

        """return optimal_dist"""
        return opGraph

    @staticmethod
    def drawGraph(graph, color):
        """Generate the pos for plot the graph"""
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True, edge_color=color)
        edge_labels = nx.get_edge_attributes(graph, 'weight')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=11)
        return pos

    def __init__(self, graph):
        self.graph = graph
        pos = self.drawGraph(self.graph, 'black')
        self.christofides(pos)
        plt.show()
