import pandas as pd
import pygraphutils.representation.adjacency_list as al
import pytest
from random import randint

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


def cell_name(i, j):
    return "cell_%d_%d" % (i, j)


def edge_type_name(i):
    return "edge_type_%d" % i


def adj_cols(num_edge_types=4):
    ac = {}
    for i in range(1, MAX_COLS, MAX_COLS // num_edge_types):
        ac[i] = edge_type_name(i)
    return ac


def create_adj_list1(adj_list_df, num_edge_types):
    adj_list1 = al.from_df(adj_list_df, adj_cols=adj_cols(num_edge_types))
    return adj_list1


def create_adj_list2(adj_list1):
    df2 = al.to_df(adj_list1)
    adj_list2 = al.from_df(df2, adj_cols=adj_list1.adj_cols)
    return adj_list2


def graph(adj_list_df, num_edge_types):
    return al.to_graph(create_adj_list1(adj_list_df, num_edge_types))


def test_get_adjacents(adj_list_df):
    for num_edge_types in range(1, MAX_COLS):
        adj_list = create_adj_list1(adj_list_df, num_edge_types)
        for i in range(0, MAX_ROWS):
            node = adj_list.get_nodes()[i]
            for j, edge_type in adj_cols(num_edge_types).items():
                assert set(adj_list.get_adjacents(node, edge_type)) == set(
                    adj_list_df.iloc[i, j : j + MAX_COLS // num_edge_types]
                )


def test_to_df_equivalence(adj_list_df):
    for num_edge_types in range(1, MAX_COLS):
        adj_list1 = create_adj_list1(adj_list_df, num_edge_types)
        adj_list2 = create_adj_list2(adj_list1)
        adj_list_df.to_excel("tmp/adj_list1.xlsx")
        al.to_df(adj_list2).to_excel("tmp/adj_list2.xlsx")
        assert adj_list1.adj_cols == adj_list2.adj_cols
        assert set(adj_list1.edge_types) == set(adj_list2.edge_types)

        for n in adj_list1.get_nodes():
            for edge_type in adj_list1.edge_types:
                assert adj_list1.get_adjacents(n, edge_type) == adj_list2.get_adjacents(
                    n, edge_type
                )


def test_graph_equivalence(adj_list_df):
    for num_edge_types in range(1, MAX_COLS):
        adj_list1 = create_adj_list1(adj_list_df, num_edge_types)
        G = graph(adj_list_df, num_edge_types)
        assert set(G.nodes) == set(adj_list1.get_nodes())
        for n in adj_list1.get_nodes():
            for edge_type in adj_list1.edge_types:
                assert set(adj_list1.get_adjacents(n, edge_type)) == set(
                    [
                        adj
                        for _, adj in G.out_edges(n)
                        if G.edges[n, adj]["edge_type"] == edge_type
                    ]
                )
