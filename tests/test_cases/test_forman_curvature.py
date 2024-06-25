import pytest
import numpy as np
from graph_ricci_curvature.forman_ricci_curvature import FormanRicciCurvature


def test_tensor_symmetry(simple_graph):
    """
    Test the Forman Ricci Curvature of an edge is the same if source and target nodes
    are swapped

    """
    obj = FormanRicciCurvature(simple_graph)
    assert obj.calculate_edge_curvature(1, 2) == obj.calculate_edge_curvature(2, 1)


def test_ricci_tensor(simple_graph):
    """
    Test Ricci curvature tensor calculation for simple graph

    """
    obj = FormanRicciCurvature(simple_graph)
    obj.calculate_ricci_curvature()
    assert list(obj.G.edges.data()) == [
        (1, 2, {"weight": 1.0, "ricci_curvature": 1.0}),
        (1, 3, {"weight": 1.0, "ricci_curvature": 1.0}),
    ]


def test_grid_graph(grid_graph):
    """
    Test the result of a calculation of graph curvature of a grid graph
    For Forman curvature, it is trivial to show each edge curvature value is -4
    rather than 0 expected from Ollivier curvature

    """
    obj = FormanRicciCurvature(grid_graph)
    obj.calculate_ricci_curvature()
    for edge in obj.G.edges():
        assert obj.G[edge[0]][edge[1]]["ricci_curvature"] == -4


def test_complete_graph(complete_graph):
    """
    Test the result of a calculation of graph curvature of a grid graph

    """
    obj = FormanRicciCurvature(complete_graph)
    obj.calculate_ricci_curvature()
    for edge in obj.G.edges():
        assert obj.G[edge[0]][edge[1]]["ricci_curvature"] == -4
