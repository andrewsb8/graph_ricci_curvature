import networkx as nx
import numpy as np
import ot
from src.graph_ricci_curvature.ricci_curvature import RicciCurvature

class OllivierRicciCurvature(RicciCurvature):
    def __init__(self):
        super().__init__()
        print("did it!")

    def _get_num_neighbors(self, graph, node):
        return len(list(graph.neighbors(node)))

    def _neighborhood_mass_distributions(node, num_neighbors, alpha):
        distributions = [(1 - alpha)/num_neighbors] * num_neighbors
        distributions = np.array(distributions.append(alpha))
        return distributions

    def _get_shortest_path_matrix(graph, source_neighborhood, target_neighborhood):
        #find shortest distance between every node in source neighborhood (attached to source node by one edge) and every node in target neighborhood
        d = []
        for source in source_neighborhood:
            tmp = []
            for target in target_neighborhood:
                tmp.append(nx.shortest_path_length(graph, source, target))
            d.append(tmp)
        return np.array(d)
