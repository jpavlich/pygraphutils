import math
from collections import OrderedDict, defaultdict
from copy import copy

import networkx as nx
import pandas as pd

from pygraphutils.util.sheet import get_col_number, is_valid


def from_graph(G: nx.Graph) -> pd.DataFrame:
    """Converts a {nx.Graph} to a Pandas DataFrame as an edge list
    
    Arguments:
        G {nx.Graph} -- The adjacency list
    
    Returns:
        pd.DataFrame -- A pandas DataFrame with two sheets: 'nodes' that contains the list of nodes and 'edges' with all edges
    """
    node_columns = sorted(list(set([k for n in G.nodes for k in G.nodes[n].keys()])))
    edge_columns = sorted(list(set([k for e in G.edges for k in G.edges[e].keys()])))

    nodes = []
    for n, d in G.nodes(data=True):
        row = [n]
        for col in node_columns:
            if col in d:
                row.append(d[col])
            else:
                row.append(math.nan)
        nodes.append(row)

    edges = []
    for s, t, d in G.edges(data=True):
        row = [s, t]
        for col in edge_columns:
            if col in d:
                row.append(d[col])
            else:
                row.append(math.nan)
        edges.append(row)

    nodes_df = pd.DataFrame(nodes, columns=["id"] + node_columns)
    edges_df = pd.DataFrame(edges, columns=["source", "target"] + edge_columns)
    return nodes_df, edges_df


def to_graph(
    nodes_df: pd.DataFrame, edges_df: pd.DataFrame, G=nx.DiGraph()
) -> nx.Graph:
    for _, row in nodes_df.iterrows():
        node = row[nodes_df.columns[0]]
        attrs = row.to_dict()
        del attrs["id"]
        G.add_node(node, **attrs)

    for _, row in edges_df.iterrows():
        attrs = row.to_dict()
        del attrs["source"]
        del attrs["target"]
        G.add_edge(row[edges_df.columns[0]], row[edges_df.columns[1]], **attrs)

    return G
