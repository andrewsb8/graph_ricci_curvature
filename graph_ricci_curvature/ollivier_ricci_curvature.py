"""
References:
    - Ollivier, Y. 2009. "Ricci curvature of Markov chains on metric spaces". Journal of Functional Analysis, 256(3), 810-864.
    - Sandhu et al. 2015. "Graph Curvature for Differentiating Cancer Networks". Scientific Reports. DOi: 10.1038/srep12323
"""

import networkx as nx
import numpy as np
import ot
from graph_ricci_curvature._ricci_curvature import RicciCurvature


class OllivierRicciCurvature(RicciCurvature):
    """
    Class for calculating Ollivier Ricci Curvature

    Parameters
    ----------
    G : networkx graph
        Input graph
    weight_key : str
        Key to specify edge weights in networkx dictionary. Default = weight

    """

    def __init__(self, G: nx.Graph, weight_key="weight"):
        super().__init__(G, weight_key)

    def calculate_ricci_curvature(self, alpha=0.5, norm=True, dist_type="uniform", method="otd", numThreads=1, reg=0.1):
        """
        Calculate nonzero values of Ricci curvature tensor for all edges in
        graph self.G

        Parameters
        ----------
        alpha : float
            Hyperparameter (0 <= alpha <=1) determining how much mass to move
            from node.
        norm : bool
            If True, normalize nodal scalar curvature.
        dist_type : str
            Distribution type for mass distribution in source or target node neighborhood. Default: uniform. Options: uniform, inverse-linear.
        method : str
            Method for calculating optimal transport plan. Options: otd (optimal transport distance), sinkhorn.
        numThreads : int
            Specify number of threads for optimal transport plan. Only for "otd" method.
        reg : float
            Regularization term to be used with "sinkhorn" method.

        Returns
        -------
        self.G : networkx graph
            Returns graph with ricci_curvature as graph, node, and edge attributes

        """

        if alpha >= 1 or alpha <= 0:
            raise ValueError("alpha must be set between 0 and 1")

        if method != "otd" and method != "sinkhorn":
            raise NotImplementedError(
                "Specified method not available. Available options: otd, sinkhorn."
            )

        ricci_tensor = {
            edge: self.calculate_edge_curvature(edge[0], edge[1], alpha=alpha, dist_type=dist_type, method=method, numThreads=numThreads, reg=reg)
            for edge in self.G.edges()
        }
        nx.set_edge_attributes(self.G, ricci_tensor, "ricci_curvature")

        node_curvature = {
            node: self._calculate_node_curvature(node, norm) for node in self.G.nodes()
        }
        nx.set_node_attributes(self.G, node_curvature, "ricci_curvature")
        (
            self.G.graph["graph_ricci_curvature"],
            self.G.graph["norm_graph_ricci_curvature"],
        ) = self._calculate_graph_curvature()

    def calculate_edge_curvature(self, source_node, target_node, alpha=0.5, dist_type="uniform", method="otd", numThreads=1, reg=0.1):
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
        dist_type : str
            Distribution type for mass distribution in source or target node neighborhood. Default: uniform. Options: uniform, inverse-linear.
        method : str
            Method for calculating optimal transport plan. Options: otd (optimal transport distance), sinkhorn
        numThreads : int
            Specify number of threads for optimal transport plan. Only for "otd" method.
        reg : float
            Regularization term to be used with "sinkhorn" method

        Returns
        -------
        curvature : float
            value of curvature tensor

        """
        source_neighbors, source_dist = self._neighborhood_mass_distribution(
            source_node, alpha, dist_type
        )
        target_neighbors, target_dist = self._neighborhood_mass_distribution(
            target_node, alpha, dist_type
        )
        short_path_matrix = self._get_shortest_path_matrix(
            source_neighbors, target_neighbors
        )
        if method == "otd":
            opt_transport = ot.emd2(
                source_dist, target_dist, short_path_matrix, numThreads=numThreads
            )
        elif method == "sinkhorn":
            opt_transport = ot.sinkhorn2(
                source_dist, target_dist, short_path_matrix, reg=reg
            )
        edge_weight = self.G.edges[source_node, target_node][self.weight_key]
        curvature = 1 - (opt_transport / edge_weight)
        return curvature

    def _neighborhood_mass_distribution(self, node, alpha, dist_type):
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
        dist_type : str
            Distribution type for mass distribution in source or target node neighborhood. Options: uniform, inverse-linear.

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
            if dist_type == "uniform":
                distribution = [(1 - alpha)/(num_neighbors) for i in range(num_neighbors)]
            elif dist_type == "inverse-linear":
                weight_sum = self._calculate_weight_sum(node, neighbors)
                distribution = [
                    (
                        (1 - alpha)
                        * (
                            (1 - (self.G[node][neighbor][self.weight_key] / weight_sum))
                            / (num_neighbors - 1)
                        )
                    )
                    for neighbor in neighbors
                ]
            else:
                raise NotImplementedError("Specified dist_type is not available. Options: uniform, inverse-linear.")
        return neighbors + [node], np.array(
            distribution + [alpha]
        )  # return neighbors as list for nx.shortest_path_length
