import json
import uuid
from collections import OrderedDict
from random import random

import networkx as nx
import pandas as pd
from networkx.drawing.layout import spring_layout

import pygraphutils.representation.adjacency_list as al
import pygraphutils.representation.json_string as j
import pygraphutils.visualization.style as s
from pygraphutils.representation.adjacency_list import AdjacencyList
from pygraphutils.util.html import include_tags_in_html
from pygraphutils.util.serialization import GenericJSONEncoder
from pygraphutils.util.template import template_function
from pygraphutils.visualization.layout import sfdp

template_path = "pygraphutils/visualization/templates"
apply_template = template_function(template_path=template_path)


if __name__ == "__main__":
    dfs = pd.read_excel("tmp/MC.xlsx", sheet_name=None)

    adj_list = AdjacencyList()
    # for sheet_name, df in dfs.items():
    adj_list = al.from_df(
        dfs["Tópicos"], edge_type_cols={"requisito": (2, 9), "es parte de": (9, None)}
    )

    G = al.to_graph(adj_list, reverse_edges=True)

    G = nx.convert_node_labels_to_integers(G, label_attribute="label")
    graph_json = j.from_graph(G)

    layout = sfdp(G, a=len(G))
    layout_json = json.dumps(layout, cls=GenericJSONEncoder)

    node_style = s.from_dfs(
        pd.read_excel("test_data/style/topic_node.xlsx", sheet_name=None)
    )
    node_style_json = json.dumps(node_style, cls=GenericJSONEncoder)

    edge_style = s.from_dfs(
        pd.read_excel("test_data/style/topic_edge.xlsx", sheet_name=None)
    )
    edge_style_json = json.dumps(edge_style, cls=GenericJSONEncoder)

    html_str = apply_template(
        "sigma_vis.j2",
        g=graph_json,
        layout=layout_json,
        node_style=node_style_json,
        edge_style=edge_style_json,
    )

    with open("tmp/sec.html", "w") as out_file:
        out_file.write(
            include_tags_in_html(in_html_str=html_str, base_path=template_path)
        )
