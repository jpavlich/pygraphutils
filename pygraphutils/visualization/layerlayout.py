import graph_tool.all as gt
from collections import deque
import random as r
from collections import OrderedDict
import networkx as nx
import sys


def _next(G, node):
    return G.predecessors(node)


def position_layers(g, layers, x_sep=150, y_sep=30):
    if not g.nodes:
        return {}
    sizes = list(map(len, layers))
    largest_layer_size = max(sizes)
    height = largest_layer_size * y_sep

    pos = {
        n: [r.randint(-x_sep / 2, x_sep / 2), -x_sep + r.randint(-x_sep / 2, x_sep / 2)]
        for n in g.nodes
    }
    for i, layer in enumerate(reversed(layers)):
        if len(layer) == 1:
            pos[int(layer[0])] = [i * x_sep, height * 0.2 * r.random() + height * 0.4]
        else:
            noise = r.random() + 0.5
            separation = height * noise / len(layer)
            y0 = height / 2 - height * noise / 2
            for j, node in enumerate(layer):
                pos[int(node)] = [i * x_sep, y0 + j * separation + separation / 2]

    return pos


def bf_layers(g, start_nodes):
    bfs_queue = deque(start_nodes)
    node_layer = {}
    visited = {}
    layers = []

    for node in start_nodes:
        node_layer[node] = 0

    while len(bfs_queue) > 0:
        current = bfs_queue.popleft()
        layer = node_layer[current]
        if layer >= len(layers):
            layers.append([])
        layers[layer].append(current)

        for n in _next(g, current):
            if not n in visited and not n in node_layer:
                node_layer[n] = layer + 1
                bfs_queue.append(n)

        visited[current] = True

    return layers


def df_layers(g, start_nodes):
    layers = []
    visited = {}
    for node in start_nodes:
        df_layer_rec(g, node, 0, layers, visited)
    return layers


def df_layer_rec(g, current, layer, layers, visited):
    if current in visited:
        return

    visited[current] = True

    if layer >= len(layers):
        layers.append([])
    layers[layer].append(current)

    for n in _next(g, current):
        df_layer_rec(g, n, layer + 1, layers, visited)


def bf_layout(g, start_nodes=[0]):
    layers = bf_layers(g, start_nodes)
    return position_layers(g, layers)


def df_layout(g, start_nodes=[0]):
    layers = df_layers(g, start_nodes)
    return position_layers(g, layers)


def convert_mapping_to_layers(node_to_layer):
    layers_dict = {}
    for node, layer in node_to_layer.items():
        if not layer in layers_dict:
            layers_dict[layer] = []
        layers_dict[layer].append(node)
    layers = [[]] * len(layers_dict.keys())
    for layer, nodes in layers_dict.items():
        layers[layer] = nodes
    return layers


def layered_layout(G, start_nodes=[0]):  # G must be acyclic

    node_to_layer = OrderedDict()

    for node in start_nodes:
        assign_to_layers(G, node, 0, node_to_layer)
    layers = convert_mapping_to_layers(node_to_layer)
    return position_layers(G, layers)


def assign_to_layers(G, current, layer, node_to_layer):
    if current in node_to_layer:
        if layer > node_to_layer[current]:
            node_to_layer[current] = layer
        else:
            return
    else:
        node_to_layer[current] = layer

    for n in _next(G, current):
        assign_to_layers(G, n, layer + 1, node_to_layer)
