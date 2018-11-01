import sys
import networkx as nx


class KruskalAlgorithm:

    @staticmethod
    def getMin(graph, mstFlag):
        """Utility function that return the smallest unprocessed edge"""

        """Assign largest numeric value to min"""
        node_min = sys.maxsize
        """Compute the min"""
        min_edge = None
        for i in [(u, v, data['weight']) for u, v, data in graph.edges(data=True) if 'weight' in data]:
            if mstFlag[i] == False and i[2] < node_min:
                node_min = i[2]
                min_edge = i
        return min_edge

    def findRoot(self, parent, i):
        """Utility function to find root or origin of the i-node in MST"""
        if parent[i] == i:
            return i
        return self.findRoot(parent, parent[i])

    def union(self, parent, order, x, y):
        """A function that does union of set x and y based on the order"""
        xRoot = self.findRoot(parent, x)
        yRoot = self.findRoot(parent, y)

        """Attach smaller order tree under root of high order tree
           if order are the same, then make any one as root and increment its order by one"""
        if order[xRoot] < order[yRoot]:
            parent[xRoot] = yRoot
        elif order[xRoot] > order[yRoot]:
            parent[yRoot] = xRoot
        else:
            parent[yRoot] = xRoot
            order[xRoot] += 1

    def computeKruskal(self):
        """Function that performs Kruskal algorithm on the graph 'graph'
           vLen denotes the number of vertices in G
           mst_graph contains the MST graph
           mst contains the MST edges
           mstFLag[i] will hold true if the edge i has ben processed for MST"""
        mst_graph = nx.Graph()
        vLen = len(self.graph.nodes())
        mst = []
        mstFlag = {}
        """Initialize the flags to False"""
        for i in [(u, v, data['weight']) for u, v, data in self.graph.edges(data=True) if 'weight' in data]:
            mstFlag[i] = False

        """parent[i] will hold the vertex connected to i in the MST
           order[i] will hold the order of appearance of the node in the MST"""
        parent = [0] * vLen
        order = [0] * vLen

        for v in range(vLen):
            parent[v] = v
            order[v] = 0
        while len(mst) < vLen - 1:
            """Pick the smallest edge from the set of edges"""
            curr_edge = self.getMin(self.graph, mstFlag)
            """Update the flag for the current edge"""
            mstFlag[curr_edge] = True
            y = self.findRoot(parent, list(self.graph.nodes).index(curr_edge[1]))
            x = self.findRoot(parent, list(self.graph.nodes).index(curr_edge[0]))
            """Adds the edge to MST, if including it doesn't form a cycle"""
            if x != y:
                mst.append(curr_edge)
                self.union(parent, order, x, y)

        for x in mst:
            if (x[0], x[1]) in self.graph.edges():
                mst_graph.add_edge(x[0], x[1], weight=self.graph[x[0]][x[1]]['weight'])

        return mst_graph

    def __init__(self, graph):
        self.graph = graph
