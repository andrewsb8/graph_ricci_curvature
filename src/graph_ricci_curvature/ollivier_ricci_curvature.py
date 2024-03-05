import networkx as nx
import numpy as np
import ot
from src.graph_ricci_curvature.ricci_curvature import RicciCurvature

class OllivierRicciCurvature(RicciCurvature):
    def __init__(self, G: nx.Graph, weight_key="weight"):
        super().__init__(G, weight_key)

    def _calculate_edge_curvature(self, source_node, target_node):
        source_neighbors = self._get_neighbors(source_node)
        source_dist = self._neighborhood_mass_distribution(len(source_neighbors))
        target_neighbors = self._get_neighbors(target_node)
        target_dist = self._neighborhood_mass_distribution(len(target_neighbors))
        short_path_matrix = self._get_shortest_path_matrix(source_neighbors, target_neighbors)
        return 1 - (ot.emd2(source_dist, target_dist, short_path_matrix)/self.G.edges[source_node, target_node][self.weight_key])

    def _get_neighbors(self, node):
        return list(self.G.neighbors(node)).append(node)

    def _neighborhood_mass_distribution(self, num_neighbors, alpha=0.5):
        #TO DO: add case for node with no neighbors
        #TO DO: make sure neighbors is not zero somewhere
        distribution = [((1 - alpha)/num_neighbors) for neighbor in num_neighbors]
        distribution = np.array(distributions.append(alpha))
        return distribution

    def _get_shortest_path_matrix(self, source_neighborhood, target_neighborhood):
        #find shortest distance between every node in source neighborhood (attached to source node by one edge) and every node in target neighborhood
        """d = []
        for source in source_neighborhood:
            tmp = []
            for target in target_neighborhood:
                tmp.append(nx.shortest_path_length(graph, source, target))
            d.append(tmp)
        return np.array(d)"""

        return np.array([ [nx.shortest_path_length(graph, source, target) for target in target_neighborhood] for source in source_neighborhood ])
