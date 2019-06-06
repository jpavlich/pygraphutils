import networkx as nx
import sys


def remove_unreachable(G, start_nodes=None):
    G = G.copy()
    if not start_nodes:
        start_nodes = [
            n for n in G.nodes if G.in_degree(n) == 0 and G.out_degree(n) > 0
        ]
    unreachable = set()
    for node in start_nodes:
        unreachable.update(nx.descendants(G, node))
    G.remove_nodes_from(unreachable)
    return G


def remove_cycles(G, start_nodes=None, orientation="original", inplace=False):
    if not start_nodes:
        start_nodes = [n for n in G.nodes if G.in_degree(n) == 0]

    if not inplace:
        G = G.copy()
    for node in start_nodes:
        remove_cycles_from_node(G, node, orientation=orientation)

    # remove_simple_cycles(G)
    return G


def remove_simple_cycles(G):
    G = G.copy()
    for cycle in nx.simple_cycles(G):
        try:
            edge = cycle[-1]
            if G.has_edge(*edge):
                G.remove_edge(*edge)
                # print(edge)
        except:
            return
    return G


def remove_cycles_from_node(G, node, orientation="original"):
    while True:
        try:

            cycle = nx.find_cycle(G, node, orientation=orientation)

            # Find weakest edge
            min_w = sys.float_info.max
            edge = (cycle[-1][0], cycle[-1][1])

            for e in cycle:
                if (
                    "weight" in G.edges[(e[0], e[1])]
                    and G.edges[(e[0], e[1])]["weight"] < min_w
                ):
                    min_w = G.edges[(e[0], e[1])]["weight"]
                    edge = (e[0], e[1])

            if G.has_edge(*edge):
                G.remove_edge(*edge)

        except nx.NetworkXNoCycle:
            return


def transitive_reduction(G):

    G_tr = nx.transitive_reduction(G)
    G_final = nx.DiGraph()
    G_final.add_nodes_from(G.nodes(data=True))
    G_final.add_edges_from(G_tr.edges)
    return G_final
