import json
import uuid
from collections import OrderedDict
from random import random

import networkx as nx
from networkx.drawing.layout import spring_layout
import pandas as pd

import pygraphutils.representation.adjacency_list as al
import pygraphutils.representation.json_string as j
from pygraphutils.util.template import template_function
from pygraphutils.util.serialization import GenericJSONEncoder
from pygraphutils.util.html import include_tags_in_html

template_path = "pygraphutils/visualization/templates"
apply_template = template_function(template_path=template_path)


if __name__ == "__main__":
    df = pd.read_excel("test_data/adj_list/topic/3. Construcción de software.xlsx")
    adj_list = al.from_df(df)
    G = al.to_graph(adj_list, reverse_edges=True)
    G = nx.convert_node_labels_to_integers(G, label_attribute="label")
    json_graph = j.from_graph(G)
    json_layout = json.dumps(spring_layout(G), cls=GenericJSONEncoder)

    html_str = apply_template("sigma_vis.j2", g=json_graph, layout=json_layout)

    with open("tmp/g.html", "w") as out_file:
        out_file.write(
            include_tags_in_html(in_html_str=html_str, base_path=template_path)
        )
