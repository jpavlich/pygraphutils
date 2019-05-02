import graph_tool.all as gt
import networkx as nx


def from_nx(G: nx.Graph) -> gt.Graph():
    g = gt.Graph()
    g.add_vertex(len(G.nodes))
    for e in G.edges:
        g.add_edge(e[0], e[1])
    return g

