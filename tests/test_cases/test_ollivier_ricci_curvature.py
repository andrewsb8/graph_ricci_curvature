import pytest
import numpy as np
from graph_ricci_curvature._graph_metric import GraphMetric
from graph_ricci_curvature.ollivier_ricci_curvature import OllivierRicciCurvature


def test_mass_distribution(simple_graph):
    """
    Test that mass distribution among neighborhoods works with unweighted edges

    """
    obj = OllivierRicciCurvature(simple_graph)
    nodes, distributions = obj._neighborhood_mass_distribution(1)
    assert np.allclose(distributions, np.array([0.25, 0.25, 0.5]))


def test_calculate_edge_curvature(simple_graph):
    """
    Test for correct value of Ricci Curvature of an edge in a simple graph

    """
    obj = OllivierRicciCurvature(simple_graph)
    assert obj.calculate_edge_curvature(1, 2) == 0.5


def test_calculate_edge_curvature_sinkhorn(simple_graph):
    """
    Test for correct value of Ricci Curvature of an edge in a simple graph using
    sinkhorn divergence

    """
    obj = OllivierRicciCurvature(simple_graph)
    assert obj.calculate_edge_curvature(1, 2, method="sinkhorn") == pytest.approx(0.5, 0.001)


def test_tensor_symmetry(simple_graph):
    """
    Test the Ricci Curvature of an edge is the same if source and target nodes
    are swapped

    """
    obj = OllivierRicciCurvature(simple_graph)
    assert obj.calculate_edge_curvature(1, 2) == obj.calculate_edge_curvature(2, 1)


def test_ricci_tensor(simple_graph):
    """
    Test Ricci curvature calculation for multiple edges in bulk and addition
    to graph object

    """
    obj = OllivierRicciCurvature(simple_graph)
    obj.calculate_ricci_curvature()
    assert list(obj.G.edges.data()) == [
        (1, 2, {"weight": 1.0, "ricci_curvature": 0.5}),
        (1, 3, {"weight": 1.0, "ricci_curvature": 0.5}),
    ]


def test_node_curvature(simple_graph):
    """
    Test calculation of normalized nodal scalar curvature from the Ricci
    Curvature tensor

    """
    obj = OllivierRicciCurvature(simple_graph)
    obj.calculate_ricci_curvature()
    assert list(obj.G.nodes.data()) == [
        (1, {"ricci_curvature": 0.5}),
        (2, {"ricci_curvature": 0.5}),
        (3, {"ricci_curvature": 0.5}),
    ]


def test_unnormed_node_curvature(simple_graph):
    """
    Test calculation of unnormalized nodal scalar curvature from the Ricci
    Curvature tensor

    """
    obj = OllivierRicciCurvature(simple_graph)
    obj.calculate_ricci_curvature(norm=False)
    assert list(obj.G.nodes.data()) == [
        (1, {"ricci_curvature": 1.0}),
        (2, {"ricci_curvature": 0.5}),
        (3, {"ricci_curvature": 0.5}),
    ]


def test_weighted_mass_distribution(simple_weighted_graph):
    """
    Test that mass distribution among neighborhoods works with weighted edges

    """
    obj = OllivierRicciCurvature(simple_weighted_graph)
    nodes, distributions = obj._neighborhood_mass_distribution(1)
    assert np.allclose(distributions, np.array([0.4, 0.1, 0.5]))


def test_weighted_ricci_curvature(simple_weighted_graph):
    """
    Test calculation of ricci curvature tensor for weighted graph

    """
    obj = OllivierRicciCurvature(simple_weighted_graph)
    obj.calculate_ricci_curvature()
    assert list(obj.G.edges.data()) == [
        (1, 2, {"weight": 0.5, "ricci_curvature": pytest.approx(0.5)}),
        (1, 3, {"weight": 2, "ricci_curvature": pytest.approx(0.5)}),
    ]
