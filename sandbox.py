import json
import uuid

import networkx as nx
import pandas as pd

import pygraphutils.representation.adjacency_list as al
import pygraphutils.representation.edge_list as el

if __name__ == "__main__":

    print(
        json.dumps(
            {
                "nodes": [{"id": "a"}, {"id": "b"}, {"id": "c"}],
                "edges": [
                    {"source": "a", "target": "b", "id": 0},
                    {"source": "a", "target": "c", "id": 1},
                    {"source": "b", "target": "c", "id": 2},
                ],
            }
        )
    )

    json.loads(
        """
        {"nodes": [{"id": "a"}, {"id": "b"}, {"id": "c"}], "edges": [{"source": "a", "target": "b", "id": 0}, {"source": "a", "target": "c", "id": 1}, {"source": "b", "target": "c", "id": 2}]}
    """
    )
