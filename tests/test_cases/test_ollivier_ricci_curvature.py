import pytest
import numpy as np
from src.graph_ricci_curvature.ricci_curvature import RicciCurvature
from src.graph_ricci_curvature.ollivier_ricci_curvature import OllivierRicciCurvature


def test_calculate_edge_curvature(simple_graph):
    obj = OllivierRicciCurvature(simple_graph)
    assert obj._calculate_edge_curvature(1, 2) == 0.5


def test_tensor_symmetry(simple_graph):
    obj = OllivierRicciCurvature(simple_graph)
    assert obj._calculate_edge_curvature(1, 2) == obj._calculate_edge_curvature(2, 1)


def test_ricci_tensor(simple_graph):
    obj = OllivierRicciCurvature(simple_graph)
    obj._calculate_ricci_curvature()
    assert list(obj.G.edges.data()) == [
        (1, 2, {"weight": 1.0, "ricci_curvature": 0.5}),
        (1, 3, {"weight": 1.0, "ricci_curvature": 0.5}),
    ]


def test_weighted_mass_distribution(simple_weighted_graph):
    obj = OllivierRicciCurvature(simple_weighted_graph)
    nodes, distributions = obj._neighborhood_mass_distribution(1)
    assert np.allclose(distributions, np.array([0.4, 0.1, 0.5]))


def test_weighted_ricci_curvature(simple_weighted_graph):
    obj = OllivierRicciCurvature(simple_weighted_graph)
    obj._calculate_ricci_curvature()
    assert list(obj.G.edges.data()) == [
        (1, 2, {"weight": 0.5, "ricci_curvature": 0.6000000000000001}),
        (1, 3, {"weight": 2, "ricci_curvature": 0.6}),
    ]
