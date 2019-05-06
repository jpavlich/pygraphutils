import uuid
import pytest
import pandas as pd
import pygraphutils.representation.adjacency_list as al
import networkx as nx

MAX_COLS = 10
MAX_ROWS = 10


@pytest.fixture
def adj_list_df():
    rows = []
    for i in range(0, MAX_ROWS):
        row = []
        for j in range(0, MAX_COLS):
            row.append(cell_name(i, j))
        rows.append(row)

    df = pd.DataFrame(rows, columns=range(0, MAX_COLS))
    # df.to_excel("tmp/test.xlsx")
    return df


@pytest.fixture
def G(adj_list_df):
    G = graph(adj_list_df, 5)
    for n in G.nodes:
        for d in range(0, 10):
            G.nodes[n]["d%d" % d] = str(uuid.uuid1())

    for e in G.edges:
        for d in range(0, 10):
            G.edges[e]["d%d" % d] = str(uuid.uuid1())
    return G


@pytest.fixture
def G_small():
    G = nx.DiGraph()
    G.add_edge("a", "b")
    G.add_edge("a", "c")
    G.add_edge("b", "c")
    return G


@pytest.fixture
def dict_small():
    return {
        "nodes": [{"id": "a"}, {"id": "b"}, {"id": "c"}],
        "edges": [
            {"source": "a", "target": "b", "id": 0},
            {"source": "a", "target": "c", "id": 1},
            {"source": "b", "target": "c", "id": 2},
        ],
    }


@pytest.fixture
def json_small():
    return """{"nodes": [{"id": "a"}, {"id": "b"}, {"id": "c"}], "edges": [{"source": "a", "target": "b", "id": 0}, {"source": "a", "target": "c", "id": 1}, {"source": "b", "target": "c", "id": 2}]}"""


def cell_name(i, j):
    return "cell_%d_%d" % (i, j)


def edge_type_name(i):
    return "edge_type_%d" % i


def edge_type_cols(num_edge_types=4):
    ac = {}
    for i in range(1, MAX_COLS, MAX_COLS // num_edge_types):
        ac[edge_type_name(i)] = (i, i + MAX_COLS // num_edge_types)
    return ac


def create_adj_list1(adj_list_df, num_edge_types):
    adj_list1 = al.from_df(adj_list_df, edge_type_cols=edge_type_cols(num_edge_types))
    # adj_list_df.to_excel("tmp/adj_list_df.xlsx")
    # al.to_df(adj_list1).to_excel("tmp/adj_list1.xlsx")
    return adj_list1


def create_adj_list2(adj_list1):
    df2 = al.to_df(adj_list1)
    adj_list2 = al.from_df(df2, edge_type_cols=adj_list1.edge_type_cols)
    return adj_list2


def graph(adj_list_df, num_edge_types):
    return al.to_graph(create_adj_list1(adj_list_df, num_edge_types))
