from abc import ABC, abstractmethod
import networkx as nx
import numpy as np
import sys


class _GraphMetric(ABC):
    """
    Parent class for classes calculating properties of a graph

    Parameters
    ----------
    G : networkx graph
        Input graph
    weight_key : str
        key to specify edge weights in networkx dictionary

    """

    def __init__(self, G: nx.Graph, edge_weight_key, node_weight_key):
        self.G = G.copy()
        self.edge_weight_key = edge_weight_key
        self.node_weight_key = node_weight_key
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

        if not nx.get_edge_attributes(self.G, self.edge_weight_key):
            sys.stderr.write(
                "No edge weights detected, setting edge weights to one with edge_weight_key = weight\n"
            )
            self._set_edge_weights(self.edge_weight_key)

        if not nx.get_node_attributes(self.G, self.node_weight_key):
            sys.stderr.write(
                "No node weights detected, setting edge weights to one with node_weight_key = weight\n"
            )
            self._set_node_weights(self.node_weight_key)

    def _set_edge_weights(self, key):
        for i, j in self.G.edges():
            self.G[i][j][key] = 1.0

    def _set_node_weights(self, key):
        nx.set_node_attributes(self.G, {node: 1.0 for node in self.G.nodes()}, key)

    def _get_neighbors(self, node):
        return list(self.G.neighbors(node))

    def _calculate_weight_sum(self, node, neighbors):
        """
        Calculate sum of weights of edges connected to a given node.

        """
        return sum(
            [self.G[node][neighbor][self.edge_weight_key] for neighbor in neighbors]
        )

    def _get_shortest_path_matrix(self, source_neighborhood, target_neighborhood, weight_path_matrix):
        """
        Find shortest distance between every node in source neighborhood
        (attached to source node by one edge) and every node in target
        neighborhood

        Parameters
        ----------
        source_neighborhood : list
            list of node index values (ints or tuples) of a source node and its neighbors
        target_neighborhood : list
            list of node index values (ints or tuples) of a source node and its neighbors
        weight_path_matrix : bool
            When True, use edge weights when calculating shortest distance matrix. Default: False.

        Returns
        -------
        numpy array of shape len(source_neighbors) x len(target_neighborhood) including
        shortest path matrices between nodes in source neighborhood and nodes in target
        neighborhood

        """
        if weight_path_matrix:
            key = self.edge_weight_key
        else:
            key = None
        return np.array(
            [
                [
                    nx.shortest_path_length(
                        self.G, source, target, weight=key
                    )
                    for target in target_neighborhood
                ]
                for source in source_neighborhood
            ]
        )

    def _check_directed(self):
        # this function will be removed when support for directed graphs is added
        if self.G.is_directed():
            raise NotImplementedError(
                "Directed Graphs are not implemented. Set your graph to undirected with G.to_undirected()."
            )
