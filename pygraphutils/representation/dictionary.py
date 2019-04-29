import networkx as nx
from typing import Dict


def from_graph(G: nx.Graph) -> Dict:
    json_graph = nx.node_link_data(G, {"key": "id"})
    edges = [{**e, "id": i} for i, e in enumerate(json_graph["links"])]
    return {"nodes": json_graph["nodes"], "edges": edges}


def to_graph(graph_dict) -> nx.Graph:
    return nx.node_link_graph(
        {"nodes": graph_dict["nodes"], "links": graph_dict["edges"]},
        directed=True,
        attrs={"key": "id"},
    )
