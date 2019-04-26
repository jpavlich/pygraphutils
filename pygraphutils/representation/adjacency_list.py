import math
from collections import OrderedDict, defaultdict
from copy import copy

import networkx as nx
import pandas as pd


from pygraphutils.util.sheet import get_col_number, is_valid


class AdjacencyList(object):
    def __init__(self):
        self.adjacents = OrderedDict()
        self.adj_cols = {}
        self.max_cols = 0
        self.edge_types = set({})

    def add_node(self, node):
        self.adjacents[node] = OrderedDict()
        for edge_type in self.edge_types:
            self.adjacents[node][edge_type] = set()

    def get_adjacents(self, node, edge_type="default"):
        """Returns adjacent nodes for the given edge_type
        
        Arguments:
            node {str} -- The node
        
        Keyword Arguments:
            edge_type {str} -- The edge type to filter adjacents (default: {'default'})
        """
        return self.adjacents[node][edge_type]

    def get_nodes(self):
        return list(self.adjacents.keys())

    def __repr__(self):
        return str(self.adjacents)


def from_df(df: pd.DataFrame, node_col=0, adj_cols={1: "default"}) -> AdjacencyList:
    """Creates adjacency list from a Pandas DataFrame
    
    Arguments:
        df {pd.DataFrame} -- The Pandas DataFrame that contains the adjacency list.
        Each row must have a node and its adjacents. Different column ranges
        can be specified in the constructor to denote specific edge types.
    
    Keyword Arguments:
        node_col {int} -- The column in df that contains the nodes (default: {0})
        adj_cols {dict} -- Each key in the dict contains the start column of adjacent nodes. 
                            The value is the edge type name.  (default: {{1: 'default'}})
    """

    adj_list = AdjacencyList()
    node_col = get_col_number(df, node_col)
    # df.set_index(df.columns[node_col], inplace=True)
    adj_cols_sorted = sorted(
        [(get_col_number(df, col), edge_type) for col, edge_type in adj_cols.items()]
    )
    edge_types = {}
    for i in range(0, len(adj_cols_sorted) - 1):
        start_col = adj_cols_sorted[i][0]
        end_col = adj_cols_sorted[i + 1][0]
        edge_type = adj_cols_sorted[i][1]
        edge_types[edge_type] = slice(start_col, end_col)

    last = len(adj_cols_sorted) - 1
    start_col = adj_cols_sorted[last][0]
    edge_type = adj_cols_sorted[last][1]
    edge_types[edge_type] = slice(start_col, None)

    for _, row in df.iterrows():
        node = row[df.columns[node_col]]
        if is_valid(node):
            adj_list.max_cols = max(len(row), adj_list.max_cols)
            adj_dict = OrderedDict()
            for edge_type, adj_slice in edge_types.items():
                adj_dict[edge_type] = set(
                    [val for val in row.values[adj_slice] if is_valid(val)]
                )

            adj_list.adjacents[node] = adj_dict

    adj_list.adj_cols = copy(adj_cols)
    adj_list.edge_types = adj_cols.values()

    # Find nodes that are only defined as adjacents
    orphans = set()
    for node, adjacents in adj_list.adjacents.items():
        if is_valid(node):
            for edge_type in adj_list.edge_types:
                for adj in adjacents[edge_type]:
                    if not adj in adj_list.adjacents:
                        orphans.add(adj)
    for n in orphans:
        adj_list.add_node(n)

    return adj_list


def to_df(adj_list: AdjacencyList) -> pd.DataFrame:
    """Converts an {AdjacencyList} to a Pandas DataFrame
    
    Arguments:
        adj_list {AdjacencyList} -- The adjacency list
    
    Returns:
        pd.DataFrame -- The equivalent DataFrame. It has the same format as the one used as input in {from_df}
    """

    rows = []
    for node, adjacents in adj_list.adjacents.items():
        row = [math.nan] * adj_list.max_cols
        row[0] = node
        # print(adj_list.adj_cols)
        for start_col, edge_type in adj_list.adj_cols.items():
            for i, adj in enumerate(adjacents[edge_type]):
                row[start_col + i] = adj
        rows.append(row)

    cols = list(range(0, adj_list.max_cols))
    for start_col, edge_type in adj_list.adj_cols.items():
        cols[start_col] = edge_type

    return pd.DataFrame(rows, columns=cols)


def to_graph(adj_list: AdjacencyList, G=nx.DiGraph(), reverse_edges=False) -> nx.Graph:
    """Converts an {AdjacencyList} to a {nx.Graph}
    
    Arguments:
        adj_list {AdjacencyList} --  The adj. list
    
    Keyword Arguments:
        G {[type]} -- The graph to populate. (default: {nx.DiGraph()})
    
    Returns:
        nx.Graph -- The equivalent graph
    """
    for node, adjacents in adj_list.adjacents.items():
        G.add_node(node)
        for edge_type in adj_list.edge_types:
            for adj in adjacents[edge_type]:
                if reverse_edges:
                    G.add_edge(adj, node, edge_type=edge_type)
                else:
                    G.add_edge(node, adj, edge_type=edge_type)

    return G
