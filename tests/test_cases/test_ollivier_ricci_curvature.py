import pytest
from src.graph_ricci_curvature.ricci_curvature import RicciCurvature
from src.graph_ricci_curvature.ollivier_ricci_curvature import OllivierRicciCurvature


def test_calculate_edge_curvature(simple_graph):
    obj = OllivierRicciCurvature(simple_graph)
    assert obj._calculate_edge_curvature(1, 2) == 0.5

def test_tensor_symmetry(simple_graph):
    obj = OllivierRicciCurvature(simple_graph)
    assert obj._calculate_edge_curvature(1, 2) == obj._calculate_edge_curvature(2, 1)
