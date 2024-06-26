import pytest
import networkx as nx


@pytest.fixture
def simple_graph():
    """Mock optimizer"""
    G = nx.Graph()
    G.add_nodes_from([1, 2, 3])
    G.add_edges_from([(1, 2), (1, 3)])
    return G


@pytest.fixture
def simple_weighted_graph():
    """Mock optimizer"""
    G = nx.Graph()
    G.add_nodes_from([1, 2, 3])
    G.add_edges_from([(1, 2), (1, 3)])
    G.edges[1, 2]["weight"] = 0.5
    G.edges[1, 3]["weight"] = 2
    return G


@pytest.fixture
def complete_graph():
    """Mock optimizer"""
    G = nx.complete_graph(5)
    return G


@pytest.fixture
def grid_graph():
    """Mock optimizer"""
    G = nx.grid_2d_graph(10, 10, periodic=True)
    return G
