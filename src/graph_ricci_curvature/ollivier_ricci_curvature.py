import networkx as nx
import numpy as np
import ot
from src.exceptions.exceptions import NotImplementedError
from src.graph_ricci_curvature.ricci_curvature import RicciCurvature


class OllivierRicciCurvature(RicciCurvature):
    def __init__(self, G: nx.Graph, weight_key="weight"):
        super().__init__(G, weight_key)

    def _calculate_ricci_curvature(self, alpha=0.5):
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
        source_neighbors, source_dist = self._neighborhood_mass_distribution(
            source_node, alpha
        )
        target_neighbors, target_dist = self._neighborhood_mass_distribution(
            target_node, alpha
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

    def _calculate_weight_sum(self, node, neighbors):
        return sum([self.G[node][neighbor][self.weight_key] for neighbor in neighbors])

    def _neighborhood_mass_distribution(self, node, alpha=0.5):
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
        return np.array(neighbors + [node]), np.array(distribution + [alpha])

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
