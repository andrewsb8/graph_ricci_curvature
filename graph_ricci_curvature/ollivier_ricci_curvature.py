"""
References:
    - Ollivier, Y. 2009. "Ricci curvature of Markov chains on metric spaces". Journal of Functional Analysis, 256(3), 810-864.
    - Sandhu et al. 2015. "Graph Curvature for Differentiating Cancer Networks". Scientific Reports. DOi: 10.1038/srep12323
"""

import networkx as nx
import numpy as np
import ot
from graph_ricci_curvature.graph_metric import GraphMetric


class OllivierRicciCurvature(GraphMetric):
    """
    Class for calculating Ollivier Ricci Curvature

    Parameters
    ----------
    G : networkx graph
        Input graph
    weight_key : str
        key to specify edge weights in networkx dictionary. Default = weight

    """

    def __init__(self, G: nx.Graph, weight_key="weight"):
        super().__init__(G, weight_key)

    def _calculate_ricci_curvature(self, alpha=0.5):
        """
        Calculate nonzero values of Ricci curvature tensor for all edges in
        graph self.G

        Parameters
        ----------
        alpha : float
            hyperparameter (0 <= alpha <=1) determining how much mass to move
            from node

        Returns
        -------
        self.G : networkx graph
            Returns graph with ricci_curvature as node and edge attributes

        """

        if alpha >= 1 or alpha <= 0:
            raise ValueError("alpha must be set between 0 and 1")

        ricci_tensor = {
            edge: self._calculate_edge_curvature(edge[0], edge[1], alpha)
            for edge in self.G.edges()
        }
        nx.set_edge_attributes(self.G, ricci_tensor, "ricci_curvature")

        node_curvature = {
            node: self._calculate_node_curvature(node) for node in self.G.nodes()
        }
        nx.set_node_attributes(self.G, node_curvature, "ricci_curvature")

    def _calculate_node_curvature(self, node):
        """
        Calculates normalized nodal scalar Ricci Curvature (i.e. contracting
        the curvature tensor) as described in Sandhu et al., Scientific Reports,
        2015, DOi: 10.1038/srep12323

        Parameters
        ----------
        node : int or tuple
            index of node in graph self.G

        Returns
        -------
        Normalized sum of edge curvatures of node and its neighbors. Normalized
        by edge weights

        """
        neighbors = self._get_neighbors(node)
        weight_sum = self._calculate_weight_sum(node, neighbors)
        return sum(
            [
                self.G[node][neighbor]["ricci_curvature"]
                * (self.G[node][neighbor][self.weight_key] / weight_sum)
                for neighbor in neighbors
            ]
        )

    def _calculate_edge_curvature(self, source_node, target_node, alpha=0.5):
        """
        Calculate value of Ricci Curvature tensor associated with an edge
        between a source and target node defined as

        1 - ( Wasserstein 1 Distance / Edge Weight )

        Parameters
        ----------
        source_node : int or tuple
            index of source_node in graph self.G
        target_node : int or tuple
            index of target node in graph self.G
        alpha : float
            hyperparameter (0 <= alpha <=1) determining how much mass to move
            from node

        Returns
        -------
        curvature : float
            value of curvature tensor

        """
        source_neighbors, source_dist = self._neighborhood_mass_distribution(
            source_node, alpha
        )
        target_neighbors, target_dist = self._neighborhood_mass_distribution(
            target_node, alpha
        )
        short_path_matrix = self._get_shortest_path_matrix(
            source_neighbors, target_neighbors
        )
        print(source_neighbors, target_neighbors, source_dist, target_dist, short_path_matrix)
        wasserstein_one = ot.emd2(source_dist, target_dist, short_path_matrix)
        edge_weight = self.G.edges[source_node, target_node][self.weight_key]
        curvature = 1 - (wasserstein_one / edge_weight)
        return curvature

    def _get_neighbors(self, node):
        return list(self.G.neighbors(node))

    def _calculate_weight_sum(self, node, neighbors):
        """
        Calculate sum of weights of edges connected to a given node

        """
        return sum([self.G[node][neighbor][self.weight_key] for neighbor in neighbors])

    def _neighborhood_mass_distribution(self, node, alpha=0.5):
        """
        Alpha is a hyperparameter such that 1 - alpha mass is distributed from
        a node to its nearest neighbors according to edge weights. Default is
        0.5 but can be changed by producing it as an argument to
        _calculate_ricci_curvature

        Parameters
        ----------
        node : int or tuple
            index of node of graph self.G
        alpha : float
            hyperparameter (0 <= alpha <=1) determining how much mass to move
            from node

        Returns
        -------
        neighbors : list
            list of indices or tuples of nearest neighbor nodes of input node
        distribution : numpy array
            array of mass at each node in array neighbors

        """
        neighbors = self._get_neighbors(node)
        num_neighbors = len(neighbors)
        if num_neighbors == 0:
            return [node], [1]
        elif num_neighbors == 1:
            distribution = [1 - alpha]
        else:
            weight_sum = self._calculate_weight_sum(node, neighbors)
            distribution = [
                (
                    (1 - alpha)
                    * (1 - (self.G[node][neighbor][self.weight_key] / weight_sum))
                )
                for neighbor in neighbors
            ]
        return neighbors + [node], np.array(distribution + [alpha]) #return neighbors as list for nx.shortest_path_length

    def _get_shortest_path_matrix(self, source_neighborhood, target_neighborhood):
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

        Returns
        -------
        numpy array of shape len(source_neighbors) x len(target_neighborhood) including
        shortest path matrices between nodes in source neighborhood and nodes in target
        neighborhood

        """
        return np.array(
            [
                [
                    nx.shortest_path_length(self.G, source, target, weight=self.weight_key)
                    for target in target_neighborhood
                ]
                for source in source_neighborhood
            ]
        )
