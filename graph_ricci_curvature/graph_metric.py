from abc import ABC, abstractmethod
import networkx as nx
import numpy as np
import sys


class GraphMetric(ABC):
    """
    Parent class for classes calculating properties of a graph

    Parameters
    ----------
    G : networkx graph
        Input graph
    weight_key : str
        key to specify edge weights in networkx dictionary

    """

    def __init__(self, G: nx.Graph, weight_key):
        self.G = G.copy()
        self.weight_key = weight_key
        self._validate()

    def _validate(self):
        """
        Validate user input by checking the graph has appropriate properties
        for calculating curvature

        """
        self._check_directed()

        if len(self.G.nodes()) == 0:
            raise ValueError("Graph has no nodes!")

        if len(self.G.edges()) == 0:
            raise ValueError("Graph has no edges!")

        if not nx.get_edge_attributes(self.G, self.weight_key):
            sys.stderr.write(
                "No edge weights detected, setting edge weights to one with weight_key = weight\n"
            )
            self._set_edge_weights()

    def _set_edge_weights(self):
        for i, j in self.G.edges():
            self.G[i][j][self.weight_key] = 1.0

    def _check_directed(self):
        # this function will be removed when support for directed graphs is added
        if self.G.is_directed():
            raise NotImplementedError(
                "Directed Graphs are not implemented. Set your graph to undirected with G.to_undirected()."
            )
