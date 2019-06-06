from pygraphutils.util.template import template_function
from pygraphutils.visualization.layout import sfdp
from pygraphutils.util.serialization import GenericJSONEncoder
import pygraphutils.representation.json_string as j
from pygraphutils.util.html import include_tags_in_html
import json
import os


def from_graph(G, layout, node_style, edge_style) -> str:
    template_path = f"{os.path.dirname(__file__)}/templates"
    apply_template = template_function(template_path=template_path)

    graph_json = j.from_graph(G)
    layout_json = json.dumps(layout, cls=GenericJSONEncoder)
    node_style_json = json.dumps(node_style, cls=GenericJSONEncoder)
    edge_style_json = json.dumps(edge_style, cls=GenericJSONEncoder)

    html_str = apply_template(
        "sigma_vis.j2",
        g=graph_json,
        layout=layout_json,
        node_style=node_style_json,
        edge_style=edge_style_json,
    )

    return include_tags_in_html(in_html_str=html_str, base_path=template_path)
