import pygraphutils.representation.dictionary as d

from tests.pygraphutils.conftest import *


def test_from_graph(G_small, dict_small):
    gd = d.from_graph(G_small)
    assert dict_small == gd
