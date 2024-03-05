from abc import ABC, abstractmethod
import networkx as nx
import numpy as np
import sys
from src.exceptions.exceptions import NotImplementedError


class RicciCurvature(ABC):
    def __init__(self, G: nx.Graph, weight_key):
        self.G = G.copy()
        self.weight_key = weight_key
        self._validate()

    def _validate(self):
        self._check_edge_weights()
        self._check_directed()

    def _check_edge_weights(self):
        if not nx.get_edge_attributes(self.G, self.weight_key):
            sys.stderr.write(
                "No edge weights detected, setting edge weights to one with weight_key = weight\n"
            )
            self._set_edge_weights()

    def _set_edge_weights(self):
        for i, j in self.G.edges():
            self.G[i][j][self.weight_key] = 1.0

    def _check_directed(self):
        if self.G.is_directed():
            raise NotImplementedError(
                "Directed Graphs are not implemented. Set your graph to undirected with self.G.to_undirected()."
            )
