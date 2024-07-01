"""
References:
    - [1] R P Sreejith et al J. Stat. Mech. (2016) 063206. DOI: 10.1088/1742-5468/2016/06/063206. arXiv: https://arxiv.org/pdf/1603.00386.
"""

import networkx as nx
import numpy as np
import ot
import math
from graph_ricci_curvature._ricci_curvature import _RicciCurvature


class FormanRicciCurvature(_RicciCurvature):
    """
    Class for calculating Forman Ricci Curvature for a connected graph. Edge and
    node weights are set to 1.0 unless values are specified by the user in the input
    networkx graph object.

    Parameters
    ----------
    G : networkx graph
        Input graph
    edge_weight_key : str
        Key to specify edge weights in networkx graph. Default = weight.
    node_weight_key : str
        Key to specify node weights in networkx graph. Default = weight.
    """

    def __init__(self, G: nx.Graph, edge_weight_key="weight", node_weight_key="weight"):
        super().__init__(G, edge_weight_key, node_weight_key)

    def calculate_ricci_curvature(self, norm=True):
        """
        Calculate nonzero values of Ricci curvature tensor for all edges in
        graph self.G

        Parameters
        ----------
        norm : bool
            If True, normalize nodal scalar curvature.

        Returns
        -------
        self.G : networkx graph
            Returns graph with ricci_curvature as graph, node, and edge attributes

        """

        ricci_tensor = {
            edge: self.calculate_edge_curvature(
                edge[0],
                edge[1],
            )
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

    def calculate_edge_curvature(self, source_node, target_node):
        """
        Calculate value of Forman Ricci Curvature tensor associated with an edge
        between a source and target node defined as in References.

        Parameters
        ----------
        source_node : int or tuple
            index of source_node in graph self.G
        target_node : int or tuple
            index of target node in graph self.G

        """
        # define some variables to make equation more readable
        source_neighbors = self._get_neighbors(source_node)
        target_neighbors = self._get_neighbors(target_node)
        edge_weight = self.G[source_node][target_node][self.edge_weight_key]
        source_node_w = self.G.nodes[source_node][self.node_weight_key]
        target_node_w = self.G.nodes[target_node][self.node_weight_key]

        # equation for curvature (see Ref [1])
        curvature = edge_weight * (
            (source_node_w / edge_weight)
            + (target_node_w / edge_weight)
            - (
                sum(
                    [
                        (
                            source_node_w
                            / math.sqrt(
                                edge_weight
                                * self.G[source_node][sn_neigh][self.edge_weight_key]
                            )
                        )
                        for sn_neigh in source_neighbors
                        if sn_neigh != target_node
                    ]
                )
                + sum(
                    [
                        (
                            target_node_w
                            / math.sqrt(
                                edge_weight
                                * self.G[target_node][tn_neigh][self.edge_weight_key]
                            )
                        )
                        for tn_neigh in target_neighbors
                        if tn_neigh != source_node
                    ]
                )
            )
        )
        return curvature
