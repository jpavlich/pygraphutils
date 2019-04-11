import pandas as pd
from pygraphutils.util.sheet import get_col_number, is_valid
from collections import OrderedDict, defaultdict
import math


class AdjacencyList(object):
    def __init__(self, df: pd.DataFrame, node_col=0, adj_cols={1: "default"}):
        """Initializes adjacency list from a sheet
        
        Arguments:
            df {pd.DataFrame} -- The pandas sheet that contains the adjacency list.
            Each row must have a node and its adjacents. Different column ranges
            can be specified in the constructor to denote specific edge types.
        
        Keyword Arguments:
            node_col {int} -- The column in df that contains the nodes (default: {0})
            adj_cols {dict} -- Each key in the dict contains the start column of adjacent nodes. 
                               The value is the edge type name.  (default: {{1: 'default'}})
        """

        self.df = df
        node_col = get_col_number(df, node_col)
        # df.set_index(df.columns[node_col], inplace=True)
        adj_cols_sorted = sorted(
            [
                (get_col_number(df, col), edge_type)
                for col, edge_type in adj_cols.items()
            ]
        )
        self.edge_types = {}
        for i in range(0, len(adj_cols_sorted) - 1):
            start_col = adj_cols_sorted[i][0]
            end_col = adj_cols_sorted[i + 1][0]
            edge_type = adj_cols_sorted[i][1]
            self.edge_types[edge_type] = slice(start_col, end_col)

        last = len(adj_cols_sorted) - 1
        start_col = adj_cols_sorted[last][0]
        edge_type = adj_cols_sorted[last][1]
        self.edge_types[edge_type] = slice(start_col, None)

        self.adjacents = OrderedDict()
        for _, row in df.iterrows():
            node = row[df.columns[node_col]]
            adj_dict = OrderedDict()
            for edge_type, adj_slice in self.edge_types.items():
                adj_dict[edge_type] = set(
                    [val for val in row.values[adj_slice] if is_valid(val)]
                )

            self.adjacents[node] = adj_dict

    def get_adjacents(self, node, edge_type="default"):
        """Returns adjacent nodes for the given edge_type
        
        Arguments:
            node {str} -- The node
        
        Keyword Arguments:
            edge_type {str} -- The edge type to filter adjacents (default: {'default'})
        """
        # print(self.adjacents)
        return self.adjacents[node][edge_type]

