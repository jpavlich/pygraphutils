import json
import networkx as nx

import pygraphutils.representation.dictionary as d


def from_graph(G: nx.Graph) -> str:
    graph_dict = d.from_graph(G)
    return json.dumps(graph_dict)


def to_graph(json_str: str) -> nx.Graph:
    graph_dict = json.loads(json_str)
    return d.to_graph(graph_dict)
