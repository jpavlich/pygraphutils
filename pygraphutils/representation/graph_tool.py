import graph_tool.all as gt
import networkx as nx


def from_nx(G: nx.Graph) -> gt.Graph():
    g = gt.Graph()
    g.add_vertex(len(G.nodes))
    node_dict = {n: i for i, n in enumerate(G.nodes)}

    for e in G.edges:
        g.add_edge(node_dict[e[0]], node_dict[e[1]])
    return g

