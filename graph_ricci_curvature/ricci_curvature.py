import networkx as nx
from graph_ricci_curvature.graph_metric import GraphMetric

class RicciCurvature(GraphMetric):
    """
    Class for storing information about the Ricci Curvature Tensor

    Parameters
    ----------
    G : networkx graph
        Input graph
    weight_key : str
        key to specify edge weights in networkx dictionary. Default = weight

    """

    def __init__(self, G: nx.Graph, weight_key):
        super().__init__(G, weight_key)

    def _calculate_graph_curvature(self):
        """
        Calculate both normalized and unnormalized sums of scalar nodal ricci
        curvature for a graph

        """

        graph_curvature = 0
        for node in self.G.nodes.data():
            graph_curvature += node[1]["ricci_curvature"]
        graph_curvature_norm = graph_curvature / self.G.number_of_nodes()
        return graph_curvature, graph_curvature_norm

    def _calculate_node_curvature(self, node, norm=True):
        """
        Calculates normalized, or unnormalized, nodal scalar Ricci Curvature
        (i.e. contracting the curvature tensor) as described in Sandhu et al.,
        Scientific Reports, 2015, DOi: 10.1038/srep12323

        Parameters
        ----------
        node : int or tuple
            index of node in graph self.G
        norm : bool
            if True, normalize scalar curvature by edge weights

        Returns
        -------
        Sum of edge curvatures of node and its neighbors. If norm == True,
        sums are normalized by edge weights of node

        """
        neighbors = self._get_neighbors(node)
        if norm:
            weight_sum = self._calculate_weight_sum(node, neighbors)
            return sum(
                [
                    self.G[node][neighbor]["ricci_curvature"]
                    * (self.G[node][neighbor][self.weight_key] / weight_sum)
                    for neighbor in neighbors
                ]
            )
        else:
            return sum(
                [self.G[node][neighbor]["ricci_curvature"] for neighbor in neighbors]
            )
