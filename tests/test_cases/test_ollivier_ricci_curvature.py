import pytest
import numpy as np
from graph_ricci_curvature._graph_metric import _GraphMetric
from graph_ricci_curvature.ollivier_ricci_curvature import OllivierRicciCurvature


def test_uniform_mass_distribution(simple_graph):
    """
    Test that mass distribution among neighborhoods works with unweighted edges

    """
    obj = OllivierRicciCurvature(simple_graph)
    nodes, distributions = obj._neighborhood_mass_distribution(
        1, alpha=0.5, dist_type="uniform"
    )
    assert np.allclose(distributions, np.array([0.25, 0.25, 0.5]))


def test_linear_mass_distribution(simple_graph):
    """
    Test that mass distribution among neighborhoods works with unweighted edges

    """
    obj = OllivierRicciCurvature(simple_graph)
    nodes, distributions = obj._neighborhood_mass_distribution(
        1, alpha=0.5, dist_type="linear"
    )
    assert np.allclose(distributions, np.array([0.25, 0.25, 0.5]))


def test_inverselinear_mass_distribution(simple_graph):
    """
    Test that mass distribution among neighborhoods works with unweighted edges

    """
    obj = OllivierRicciCurvature(simple_graph)
    nodes, distributions = obj._neighborhood_mass_distribution(
        1, alpha=0.5, dist_type="inverse-linear"
    )
    assert np.allclose(distributions, np.array([0.25, 0.25, 0.5]))


def test_gaussian_mass_distribution(simple_graph):
    """
    Test that mass distribution among neighborhoods works with unweighted edges

    """
    obj = OllivierRicciCurvature(simple_graph)
    nodes, distributions = obj._neighborhood_mass_distribution(
        1, alpha=0.5, dist_type="gaussian"
    )
    assert np.allclose(distributions, np.array([0.25, 0.25, 0.5]))


def test_uniform_weighted_mass_distribution(simple_weighted_graph):
    """
    Test that mass distribution among neighborhoods works with unweighted edges

    """
    obj = OllivierRicciCurvature(simple_weighted_graph)
    nodes, distributions = obj._neighborhood_mass_distribution(1, alpha=0.5, dist_type="uniform")
    assert np.allclose(distributions, np.array([0.25, 0.25, 0.5]))


def test_linear_weighted_mass_distribution(simple_weighted_graph):
    """
    Test that mass distribution among neighborhoods works with weighted edges

    """
    obj = OllivierRicciCurvature(simple_weighted_graph)
    nodes, distributions = obj._neighborhood_mass_distribution(
        1, alpha=0.5, dist_type="linear"
    )
    assert np.allclose(distributions, np.array([0.1, 0.4, 0.5]))


def test_inverselinear_weighted_mass_distribution(simple_weighted_graph):
    """
    Test that mass distribution among neighborhoods works with weighted edges

    """
    obj = OllivierRicciCurvature(simple_weighted_graph)
    nodes, distributions = obj._neighborhood_mass_distribution(
        1, alpha=0.5, dist_type="inverse-linear"
    )
    assert np.allclose(distributions, np.array([0.4, 0.1, 0.5]))


def test_gaussian_weighted_mass_distribution(simple_weighted_graph):
    """
    Test that mass distribution among neighborhoods works with weighted edges

    """
    obj = OllivierRicciCurvature(simple_weighted_graph)
    nodes, distributions = obj._neighborhood_mass_distribution(
        1, alpha=0.5, dist_type="gaussian"
    )
    assert np.allclose(distributions, np.array([0.48851132, 0.01148868, 0.5]))


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
    assert obj.calculate_edge_curvature(1, 2, method="sinkhorn") == pytest.approx(
        0.5, 0.001
    )


def test_tensor_symmetry(simple_graph):
    """
    Test the Ollivier Ricci Curvature of an edge is the same if source and target nodes
    are swapped

    """
    obj = OllivierRicciCurvature(simple_graph)
    assert obj.calculate_edge_curvature(1, 2) == obj.calculate_edge_curvature(2, 1)


def test_ricci_tensor(simple_graph):
    """
    Test Ricci curvature tensor calculation for simple graph

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
        (1, {"weight": 1.0, "ricci_curvature": 0.5}),
        (2, {"weight": 1.0, "ricci_curvature": 0.5}),
        (3, {"weight": 1.0, "ricci_curvature": 0.5}),
    ]


def test_unnormed_node_curvature(simple_graph):
    """
    Test calculation of unnormalized nodal scalar curvature from the Ricci
    Curvature tensor

    """
    obj = OllivierRicciCurvature(simple_graph)
    obj.calculate_ricci_curvature(norm=False)
    assert list(obj.G.nodes.data()) == [
        (1, {"weight": 1.0, "ricci_curvature": 1.0}),
        (2, {"weight": 1.0, "ricci_curvature": 0.5}),
        (3, {"weight": 1.0, "ricci_curvature": 0.5}),
    ]


def test_uniform_weighted_ricci_curvature(simple_weighted_graph):
    """
    Test calculation of ricci curvature tensor for weighted graph

    """
    obj = OllivierRicciCurvature(simple_weighted_graph)
    obj.calculate_ricci_curvature()
    assert list(obj.G.edges.data()) == [
        (1, 2, {"weight": 0.5, "ricci_curvature": pytest.approx(0)}),
        (1, 3, {"weight": 2, "ricci_curvature": pytest.approx(0.75)}),
    ]


def test_inverselinear_weighted_ricci_curvature(simple_weighted_graph):
    """
    Test calculation of ricci curvature tensor for weighted graph

    """
    obj = OllivierRicciCurvature(simple_weighted_graph)
    obj.calculate_ricci_curvature(dist_type="inverse-linear")
    assert list(obj.G.edges.data()) == [
        (1, 2, {"weight": 0.5, "ricci_curvature": pytest.approx(0.6)}),
        (1, 3, {"weight": 2, "ricci_curvature": pytest.approx(0.6)}),
    ]


def test_inverselinear_weighted_pathmatrix_ricci_curvature(simple_weighted_graph):
    """
    Test calculation of ricci curvature tensor for weighted graph

    """
    obj = OllivierRicciCurvature(simple_weighted_graph)
    obj.calculate_ricci_curvature(dist_type="inverse-linear", weight_path_matrix=True)
    assert list(obj.G.edges.data()) == [
        (1, 2, {"weight": 0.5, "ricci_curvature": pytest.approx(0.5)}),
        (1, 3, {"weight": 2, "ricci_curvature": pytest.approx(0.5)}),
    ]


def test_grid_graph(grid_graph):
    """
    Test the result of a calculation of graph curvature of a grid graph is zero

    """
    obj = OllivierRicciCurvature(grid_graph)
    obj.calculate_ricci_curvature()
    for edge in obj.G.edges():
        assert obj.G[edge[0]][edge[1]]["ricci_curvature"] == 0


def test_complete_graph(complete_graph):
    """
    Test the result of a calculation of graph curvature of a grid graph is positive

    """
    obj = OllivierRicciCurvature(complete_graph)
    obj.calculate_ricci_curvature()
    for edge in obj.G.edges():
        assert obj.G[edge[0]][edge[1]]["ricci_curvature"] == 0.625
