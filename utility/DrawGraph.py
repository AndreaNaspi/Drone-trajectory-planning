import networkx as nx
import matplotlib.pyplot as plt
from data_structure import Depot, PointOfInterest


class DrawGraph:

    @staticmethod
    def drawGraphKamada(graph, highlightEdge, depot_color, point_color):
        """Plot graph in kamada layout"""

        """Create a dictionary with latitude/longitude values for each nodes"""
        dictPos = {}
        for node in graph.nodes:
            dictPos[node] = (node.getLatitude(), node.getLongitude())

        """Plot the graph"""
        pos = nx.kamada_kawai_layout(graph, dictPos)
        nx.draw_networkx_nodes(graph, pos, nodelist=[node for node in graph.nodes if type(node) == Depot.Depot], with_labels=True, node_color=depot_color)
        nx.draw_networkx_nodes(graph, pos, nodelist=[node for node in graph.nodes if type(node) == PointOfInterest.PointOfInterest], with_labels=True, node_color=point_color)
        if highlightEdge:
            nx.draw_networkx_edges(graph, pos, edgelist=graph.edges, width=2.5, alpha=0.6)
        else:
            nx.draw_networkx_edges(graph, pos, edgelist=graph.edges)
        """Plot labels"""
        if nx.get_node_attributes(graph, 'label') != {}:
            labels = {}
            for node, data in graph.nodes(data=True):
                labels[node] = data['label']
            nx.draw_networkx_labels(graph, pos, labels, font_size=15)

        plt.axis('off')
        plt.draw()
        plt.show()
