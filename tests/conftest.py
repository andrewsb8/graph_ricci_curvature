import pytest
import networkx as nx


@pytest.fixture
def simple_graph():
    """Mock optimizer"""
    G = nx.Graph()
    G.add_nodes_from([1, 2, 3])
    G.add_edges_from([(1, 2), (1, 3)])
    return G
