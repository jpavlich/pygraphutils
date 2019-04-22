import pandas as pd
from pygraphutils.representation.adjacency_list import AdjacencyList
import pytest


@pytest.fixture
def adj_list():
    df = pd.read_excel("test_data/adj_list/topic/3. Construcción de software.xlsx")
    al = AdjacencyList(df, adj_cols={1: "default", 3: "def2"})
    return al


def test_get_adjacents(adj_list):
    assert set(["Use Case"]) == set(
        adj_list.get_adjacents("Use Case Diagram", "default")
    )


def test_get_adjacents2(adj_list):
    assert set(
        [
            "Test Case",
            "Actor (Uml)",
            "User Interface Design Process",
            "User Requirements Document",
            "Software Requirements",
        ]
    ) == set(adj_list.get_adjacents("Use Case Diagram", "def2"))
