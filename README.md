# graph_ricci_curvature
Calculate Ricci Curvature for a networkx graph

# Installation

## From Source
- Clone the repository and ```cd``` into it
- Install python's ```build```: ```python -m pip install build```
- Build the project: ```python -m build```
- Install the package: ```python -m pip install dist/[file name].whl```

## Download the .whl from Releases

Not done yet

## From PyPi

Not done yet

# Usage

After installation:

```
from graph_ricci_curvature.ollivier_ricci_curvature import OllivierRicciCurvature
import networkx as nx
G = nx.Graph()
G.add_nodes_from([1, 2, 3])
G.add_edges_from([(1, 2), (1, 3)])
g = OllivierRicciCurvature(G)
g.calculate_ricci_curvature()
print(list(g.G.edges.data()))
print(list(g.G.nodes.data()))
print(g.G.graph["graph_ricci_curvature"], g.G.graph["norm_graph_ricci_curvature"])
```

Output:

```
[
(1, 2, {"weight": 1.0, "ricci_curvature": 0.5}),
(1, 3, {"weight": 1.0, "ricci_curvature": 0.5}),
]
[
(1, {'ricci_curvature': 0.5}),
(2, {'ricci_curvature': 0.5}),
(3, {'ricci_curvature': 0.5})
]
1.5 0.5
```

# References
- [1] https://www.nature.com/articles/s41598-018-27001-3
