import uuid

import networkx as nx
import pandas as pd
import pytest

import pygraphutils.representation.adjacency_list as al
import pygraphutils.representation.edge_list as el


@pytest.fixture
def adj_list1():
    df = pd.read_excel("test_data/adj_list/topic/3. Construcción de software.xlsx")
    adj_list1 = al.from_df(df, adj_cols={1: "default", 4: "def2"})
    return adj_list1


@pytest.fixture
def G(adj_list1):
    G = al.to_graph(adj_list1)
    for n in G.nodes:
        for d in range(0, 10):
            G.nodes[n]["d%d" % d] = str(uuid.uuid1())

    for e in G.edges:
        for d in range(0, 10):
            G.edges[e]["d%d" % d] = str(uuid.uuid1())
    return G


def test_graph_equivalence(G):
    n_df, e_df = el.to_df(G)
    G2 = el.from_df(n_df, e_df)
    assert nx.is_isomorphic(G, G2)
