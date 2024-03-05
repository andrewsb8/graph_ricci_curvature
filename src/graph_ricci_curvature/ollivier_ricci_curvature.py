import networkx as nx
import numpy as np
import ot
from src.graph_ricci_curvature.ricci_curvature import RicciCurvature


class OllivierRicciCurvature(RicciCurvature):
    def __init__(self, G: nx.Graph, weight_key="weight"):
        super().__init__(G, weight_key)

    def _calculate_edge_curvature(self, source_node, target_node):
        source_neighbors, source_dist = self._neighborhood_mass_distribution(
            source_node
        )
        target_neighbors, target_dist = self._neighborhood_mass_distribution(
            target_node
        )
        short_path_matrix = self._get_shortest_path_matrix(
            source_neighbors, target_neighbors
        )
        return 1 - (
            ot.emd2(source_dist, target_dist, short_path_matrix)
            / self.G.edges[source_node, target_node][self.weight_key]
        )

    def _get_neighbors(self, node):
        return list(self.G.neighbors(node))

    def _neighborhood_mass_distribution(self, node, alpha=0.5):
        # TO DO: add case for node with no neighbors
        # TO DO: make sure neighbors is not zero somewhere
        node_neighbors = self._get_neighbors(node)
        distribution = [
            ((1 - alpha) / len(node_neighbors)) for neighbor in node_neighbors
        ]
        node_neighbors = np.array(node_neighbors + [node])
        distribution = np.array(distribution + [alpha])
        return node_neighbors, distribution

    def _get_shortest_path_matrix(self, source_neighborhood, target_neighborhood):
        # find shortest distance between every node in source neighborhood (attached to source node by one edge) and every node in target neighborhood
        return np.array(
            [
                [
                    nx.shortest_path_length(self.G, source, target)
                    for target in target_neighborhood
                ]
                for source in source_neighborhood
            ]
        )
