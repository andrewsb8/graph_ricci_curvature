# graph_ricci_curvature

Calculate the Ricci curvature tensor for a networkx graph. Both Ollivier [1] and Forman [3] discretizations of Ricci curvature are implemented (see [4] for comparison of methods).

## Installation

### From Source
- Clone the repository and ```cd``` into the top level directory
- Install python's ```build```: ```python -m pip install build```
- Build the project: ```python -m build```
- Install the project with pip: ```python -m pip install dist/[file name].whl```

For testing the installation, you need ```pytest```. Run ```pytest``` in the top level directory to run the full test suite.

### Download the .whl from Releases

After download, install the wheel via pip: ```python -m pip install [file name].whl```

### From PyPi

Not done yet

## Usage

After installation:

```
from graph_ricci_curvature.ollivier_ricci_curvature import OllivierRicciCurvature
import networkx as nx

#setting up a simple graph
G = nx.Graph()
G.add_nodes_from([1, 2, 3])
G.add_edges_from([(1, 2), (1, 3)])

#create an object and calculate the values of the tensor and its contractions
g = OllivierRicciCurvature(G)
g.calculate_ricci_curvature()

#print results of calculation
print(list(g.G.edges.data()))
print(list(g.G.nodes.data()))
print(g.G.graph["graph_ricci_curvature"], g.G.graph["norm_graph_ricci_curvature"])
```

Output:

```
#edge curvature data
[
(1, 2, {"weight": 1.0, "ricci_curvature": 0.5}),
(1, 3, {"weight": 1.0, "ricci_curvature": 0.5}),
]

#node curvature data
[
(1, {"weight": 1.0, "ricci_curvature": 0.5}),
(2, {"weight": 1.0, "ricci_curvature": 0.5}),
(3, {"weight": 1.0, "ricci_curvature": 0.5})
]

#graph curvature data
1.5 0.5
```

## Manual

You can see the manual [here](https://github.com/andrewsb8/graph_ricci_curvature/blob/docs/docs/_build/latex/graph_ricci_curvature.pdf) which is in ```docs/_build/latex```. Or, after installation, can run the following with python

```
import graph_ricci_curvature as grc
grc.__manual__
```

to obtain the link to the pdf in the github repository.

# References
- [1] Ollivier, Y. 2009. "Ricci curvature of Markov chains on metric spaces". Journal of Functional Analysis, 256(3), 810-864. DOI: https://doi.org/10.1016/j.jfa.2008.11.001, arXiv: https://arxiv.org/abs/math/0701886
- [2] Sandhu et al. 2015. "Graph Curvature for Differentiating Cancer Networks". Scientific Reports. DOi: 10.1038/srep12323. DOI: https://doi.org/10.1038/srep12323.
- [3] R P Sreejith et al. "Forman curvature for complex networks" J. Stat. Mech. (2016) 063206. DOI: 10.1088/1742-5468/2016/06/063206. arXiv: https://arxiv.org/pdf/1603.00386.
- [4] Samal et al. "Comparative analysis of two discretizations of Ricci curvature for complex networks". Nature Scientific Reports, 2018. https://www.nature.com/articles/s41598-018-27001-3.
