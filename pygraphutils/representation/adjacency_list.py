import math
from collections import defaultdict
from copy import copy

import networkx as nx
import pandas as pd
from typing import List


from pygraphutils.util.sheet import get_col_number, is_valid
from pygraphutils.util.text import standardize_string


class AdjacencyList(object):
    def __init__(self):
        self._nodes = defaultdict(dict)
        self._adjacents_by_edge_type = defaultdict(lambda: defaultdict(set))
        self.max_cols = 0
        self.attr_cols = dict({})
        self.edge_type_cols = dict({})

    def add_node(self, node, **attrs):
        self._nodes[node].update(attrs)
        if not node in self._adjacents_by_edge_type:
            self._adjacents_by_edge_type[node] = defaultdict(set)
            return True
        else:
            return False

    def set_adjacents(self, node, adjacents, edge_type="default"):
        # self._adjacents_by_edge_type[node][edge_type].update(adjacents)
        self._adjacents_by_edge_type[node][edge_type] = set(adjacents)

    def add_adjacents(self, node, adjacents, edge_type="default"):
        # self._adjacents_by_edge_type[node][edge_type].update(adjacents)
        self._adjacents_by_edge_type[node][edge_type].update(adjacents)

    def get_adjacents(self, node, edge_type="default"):
        """Returns adjacent nodes for the given edge_type
        
        Arguments:
            node {str} -- The node
        
        Keyword Arguments:
            edge_type {str} -- The edge type to filter adjacents (default: {'default'})
        """
        return self._adjacents_by_edge_type[node][edge_type]

    def get_nodes(self):
        return list(self._nodes.keys())

    def get_attrs(self, node):
        return self._nodes[node]

    def get_edge_types(self):
        return self.edge_type_cols.keys()

    def __repr__(self):
        return str(self._adjacents_by_edge_type)


def from_dfs(
    dfs: List[pd.DataFrame],
    node_col=0,
    attr_cols={"node_type": 1},
    default_attr_values={"node_type": None},
    edge_type_cols={"default_edge_type": (2, None)},
):
    adj_list = AdjacencyList()
    for df in dfs:
        from_df(df, node_col, attr_cols, default_attr_values, edge_type_cols, adj_list)
    return adj_list


def from_df(
    df: pd.DataFrame,
    node_col=0,
    attr_cols={"node_type": 1},
    default_attr_values={"node_type": None},
    edge_type_cols={"default_edge_type": (2, None)},
    adj_list=AdjacencyList(),
) -> AdjacencyList:
    """Creates adjacency list from a Pandas DataFrame
    
    Arguments:
        df {pd.DataFrame} -- The Pandas DataFrame that contains the adjacency list.
        Each row must have a node and its adjacents. Different column ranges
        can be specified in the constructor to denote specific edge types.
    
    Keyword Arguments:
        node_col {int} -- The column in df that contains the node attributes (default: 0)
        attr_cols {dict} -- Each key in the dict contains name of the attribute and maps to the column that has that attribute. 
        edge_type_cols {dict} -- Each key in the dict contains the name of the edge type and the value contains the range of columns with
                            the adjacent nodes with that edge_type. (default: {"default_edge_type": (2, None)}})
    """

    node_col = get_col_number(df, node_col)
    adj_list.attr_cols = attr_cols
    adj_list.edge_type_cols = edge_type_cols

    for _, row in df.iterrows():
        node = standardize_string(row[df.columns[node_col]])
        if is_valid(node):
            attrs = {}
            for attr, col in attr_cols.items():
                if col < len(df.columns) and is_valid(row[df.columns[col]]):
                    attrs[attr] = row[df.columns[col]]
                    # print(node, attrs[attr], is_valid(row[df.columns[col]]))
                else:
                    attrs[attr] = default_attr_values.get(attr, None)
                    # print(node, attrs[attr], list(df.columns))

            adj_list.add_node(node, **attrs)
            adj_list.max_cols = max(len(row), adj_list.max_cols)

            for edge_type, col_range in adj_list.edge_type_cols.items():
                adjs = [
                    standardize_string(val)
                    for val in row.values[slice(*col_range)]
                    if is_valid(val)
                ]
                adj_list.add_adjacents(node, adjs, edge_type)

    # Find nodes that are only defined as adjacents
    for node in adj_list.get_nodes():
        for edge_type in adj_list.get_edge_types():
            for adj in adj_list.get_adjacents(node, edge_type):
                attrs = {
                    attr: default_attr_values.get(attr, None)
                    for attr in attr_cols.keys()
                }
                adj_list.add_node(adj, **attrs)

    return adj_list


def to_df(adj_list: AdjacencyList) -> pd.DataFrame:
    """Converts an {AdjacencyList} to a Pandas DataFrame
    
    Arguments:
        adj_list {AdjacencyList} -- The adjacency list
    
    Returns:
        pd.DataFrame -- The equivalent DataFrame. It has the same format as the one used as input in {from_df}
    """

    rows = []
    for node in adj_list.get_nodes():
        row = [math.nan] * adj_list.max_cols
        row[0] = node
        for attr, col in adj_list.attr_cols.items():
            row[col] = adj_list.get_attrs(node)[attr]

        for edge_type, col_range in adj_list.edge_type_cols.items():
            adjs = adj_list.get_adjacents(node, edge_type)
            row[col_range[0] : col_range[1] + len(adjs)] = sorted(adjs)

        rows.append(row)

    cols = list(range(0, adj_list.max_cols))
    for edge_type, col_range in adj_list.edge_type_cols.items():
        cols[col_range[0]] = edge_type

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
    # for node, adjacents in adj_list.adjacents_by_edge_type.items():
    for node in adj_list.get_nodes():
        G.add_node(node, **adj_list.get_attrs(node))
        for edge_type in adj_list.get_edge_types():
            for adj in adj_list.get_adjacents(node, edge_type):
                if reverse_edges:
                    G.add_edge(adj, node, edge_type=edge_type)
                else:
                    G.add_edge(node, adj, edge_type=edge_type)

    return G
