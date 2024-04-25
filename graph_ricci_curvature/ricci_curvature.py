import networkx as nx
from graph_ricci_curvature.graph_metric import GraphMetric

class RicciCurvature(GraphMetric):
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
