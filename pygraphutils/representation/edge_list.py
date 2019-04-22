import math
from collections import OrderedDict, defaultdict
from copy import copy

import networkx as nx
import pandas as pd

from pygraphutils.util.sheet import get_col_number, is_valid


def to_df(G: nx.Graph) -> pd.DataFrame:
    """Converts a {nx.Graph} to a Pandas DataFrame as an edge list
    
    Arguments:
        G {nx.Graph} -- The adjacency list
    
    Returns:
        pd.DataFrame -- A pandas DataFrame with two sheets: 'nodes' that contains the list of nodes and 'edges' with all edges
    """
    pass
