import pygraphutils.representation.json_string as j
import json
from tests.pygraphutils.conftest import *


def test_from_graph(G_small, json_small):
    gd = j.from_graph(G_small)
    print(gd)

    assert json.loads(json_small) == json.loads(gd)
