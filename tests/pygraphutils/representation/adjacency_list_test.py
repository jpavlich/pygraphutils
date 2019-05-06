import pandas as pd
import pygraphutils.representation.adjacency_list as al
import pytest
from random import randint
from tests.pygraphutils.conftest import *


def test_get_adjacents(adj_list_df):
    for num_edge_types in range(1, MAX_COLS):
        adj_list = create_adj_list1(adj_list_df, num_edge_types)

        for i in range(0, MAX_ROWS):
            node = adj_list.get_nodes()[i]
            for edge_type, col_range in adj_list.edge_type_cols.items():
                assert set(adj_list.get_adjacents(node, edge_type)) == set(
                    adj_list_df.iloc[i, col_range[0] : col_range[1]]
                )


def test_to_df_equivalence(adj_list_df):
    for num_edge_types in range(1, MAX_COLS):
        adj_list1 = create_adj_list1(adj_list_df, num_edge_types)
        adj_list2 = create_adj_list2(adj_list1)
        adj_list_df.to_excel("tmp/adj_list1.xlsx")
        al.to_df(adj_list2).to_excel("tmp/adj_list2.xlsx")
        assert set(adj_list1.edge_type_cols) == set(adj_list2.edge_type_cols)
        assert set(adj_list1.get_nodes()) == set(adj_list2.get_nodes())

        for node in adj_list1.get_nodes():
            for edge_type in adj_list1.get_edge_types():
                assert adj_list1.get_adjacents(
                    node, edge_type
                ) == adj_list2.get_adjacents(node, edge_type)


def test_graph_equivalence(adj_list_df):
    for num_edge_types in range(1, MAX_COLS):
        adj_list1 = create_adj_list1(adj_list_df, num_edge_types)
        G = graph(adj_list_df, num_edge_types)
        assert set(G.nodes) == set(adj_list1.get_nodes())
        for n in adj_list1.get_nodes():
            for edge_type in adj_list1.edge_type_cols.keys():
                assert set(adj_list1.get_adjacents(n, edge_type)) == set(
                    [
                        adj
                        for _, adj in G.out_edges(n)
                        if G.edges[n, adj]["edge_type"] == edge_type
                    ]
                )
