import networkx as nx
import numpy as np
import ot

def get_neighbors_and_distributions(graph, node, alpha):
    neighbors = list(graph.neighbors(node))
    distributions = [(1 - alpha)/len(neighbors)] * len(neighbors)
    neighbors = neighbors + [node]
    distributions = distributions + [alpha]
    return np.array(neighbors), np.array(distributions)

def get_shortest_path_matrix(graph, source_neighborhood, target_neighborhood):
    #find shortest distance between every node in source neighborhood (attached to source node by one edge) and every node in target neighborhood
    d = []
    for source in source_neighborhood:
        tmp = []
        for target in target_neighborhood:
            tmp.append(nx.shortest_path_length(graph, source, target))
        d.append(tmp)
    return np.array(d)

def example():
    #define graph
    G = nx.Graph()
    G.add_nodes_from([1, 2, 3])
    G.add_edges_from([(1,2), (1,3)])

    #get keys for nodes/edges
    edge_keys = list(G.edges.keys())
    node_keys = list(G.nodes.keys())

    #hyperparameter for mass distribution
    alpha = 0.5

    #calculate Ricci Curvature for one edge, source & target node neighborhood distributions and shortest path matrix between nodes in neighborhoods
    source_neighborhood, source_distribution = get_neighbors_and_distributions(G, edge_keys[0][1], alpha)
    target_neighborhood, target_distribution = get_neighbors_and_distributions(G, edge_keys[0][0], alpha)
    short_path_matrix = get_shortest_path_matrix(G, source_neighborhood, target_neighborhood)

    #inputs to the earth mover's distance function in POT class
    print(source_distribution, target_distribution, short_path_matrix)

    #calculate earth mover's distance
    m = ot.emd2(source_distribution, target_distribution, short_path_matrix)

    #calculate Ricci curvature of edge, no division in second term because weight is 1
    k = 1 - m
    print("Curvature: ", k)
