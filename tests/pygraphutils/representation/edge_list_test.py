import networkx as nx
import pandas as pd
import pytest

import pygraphutils.representation.adjacency_list as al
import pygraphutils.representation.edge_list as el

from tests.pygraphutils.conftest import *


def test_graph_equivalence(G):
    n_df, e_df = el.from_graph(G)
    G2 = el.to_graph(n_df, e_df)
    assert nx.is_isomorphic(G, G2)
