from abc import ABC, abstractmethod

class RicciCurvature(ABC):
    def __init__(self):
        pass

    def _get_neighbors_and_distributions(graph, node, alpha):
        neighbors = list(graph.neighbors(node))
        distributions = [(1 - alpha)/len(neighbors)] * len(neighbors)
        neighbors = neighbors + [node]
        distributions = distributions + [alpha]
        return np.array(neighbors), np.array(distributions)

    def _get_shortest_path_matrix(graph, source_neighborhood, target_neighborhood):
        #find shortest distance between every node in source neighborhood (attached to source node by one edge) and every node in target neighborhood
        d = []
        for source in source_neighborhood:
            tmp = []
            for target in target_neighborhood:
                tmp.append(nx.shortest_path_length(graph, source, target))
            d.append(tmp)
        return np.array(d)
