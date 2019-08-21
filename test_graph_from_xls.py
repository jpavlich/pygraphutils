import json
import uuid
from collections import OrderedDict
from random import random

import networkx as nx
import pandas as pd
from networkx.drawing.layout import spring_layout

import pygraphutils.representation.edge_list as edge_list
import pygraphutils.representation.json_string as j
import pygraphutils.visualization.style as s
from pygraphutils.representation.adjacency_list import AdjacencyList
from pygraphutils.util.html import include_tags_in_html
from pygraphutils.util.serialization import GenericJSONEncoder
from pygraphutils.util.template import template_function
from pygraphutils.visualization.layout import sfdp
import pygraphutils.visualization.report as report


if __name__ == "__main__":
    dfs = pd.read_excel("test_data/edge_list/topic_graph.xlsx", sheet_name=None)
    nodes_df = dfs["nodes"]
    edges_df = dfs["edges"]

    G = edge_list.to_graph(nodes_df, edges_df)

    # n, e = edge_list.from_graph(G)
    # n.to_excel("tmp/nodes.xlsx")
    # e.to_excel("tmp/edges.xlsx")

    G = nx.convert_node_labels_to_integers(G, label_attribute="label")
    nodes = [n for n in G.nodes if G.nodes[n]["area"] == "Sistemas Operativos"]
    print(nodes)
    H = G.subgraph(nodes)

    layout = sfdp(H)

    node_style = s.from_dfs(
        pd.read_excel("test_data/style/topic_node.xlsx", sheet_name=None)
    )

    edge_style = s.from_dfs(
        pd.read_excel("test_data/style/topic_edge.xlsx", sheet_name=None)
    )

    with open("tmp/index.html", "w") as out_file:
        out_file.write(report.from_graph(H, layout, node_style, edge_style))
