import pytest
import networkx as nx
from src.graph_ricci_curvature.ricci_curvature import RicciCurvature
from src.graph_ricci_curvature.ollivier_ricci_curvature import OllivierRicciCurvature


def test_calculate_edge_curvature():
    G = nx.Graph()
    G.add_nodes_from([1, 2, 3])
    G.add_edges_from([(1, 2), (1, 3)])

    obj = OllivierRicciCurvature(G)
    assert obj._calculate_edge_curvature(1, 2) == 0.5

def test_tensor_symmetry():
    G = nx.Graph()
    G.add_nodes_from([1, 2, 3])
    G.add_edges_from([(1, 2), (1, 3)])

    obj = OllivierRicciCurvature(G)
    assert obj._calculate_edge_curvature(1, 2) == obj._calculate_edge_curvature(2, 1)
