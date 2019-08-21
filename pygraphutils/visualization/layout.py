import pygraphutils.representation.graph_tool as gt
from graph_tool.draw import sfdp_layout
import pandas as pd
import numpy as np
import math
import json
from random import shuffle, random
import networkx.drawing.nx_agraph as nxa
import networkx as nx


def sfdp(G: nx.DiGraph, weight_attr=None, **params):
    g = gt.from_nx(G)
    coords = []
    if weight_attr:
        weights = g.new_edge_property("float")
        for i, j, d in G.edges(data=True):
            weights[(i, j)] = d[weight_attr]
        coords = sfdp_layout(g, eweight=weights, **params)
    else:
        coords = sfdp_layout(g)

    nodes = list(G.nodes)
    print(list(coords))
    return {nodes[i]: [pos[0], pos[1]] for i, pos in enumerate(coords)}
