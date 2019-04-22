import pandas as pd
import pygraphutils.representation.adjacency_list as al
import pytest


@pytest.fixture
def adj_list1():
    df = pd.read_excel("test_data/adj_list/topic/3. Construcción de software.xlsx")
    adj_list1 = al.from_df(df, adj_cols={1: "default", 4: "def2"})
    return adj_list1


@pytest.fixture
def adj_list2():
    df = pd.read_excel("test_data/adj_list/topic/3. Construcción de software.xlsx")
    adj_list1 = al.from_df(df, adj_cols={1: "default", 4: "def2"})
    df2 = al.to_df(adj_list1)
    adj_list2 = al.from_df(df2, adj_cols={1: "default", 4: "def2"})
    return adj_list2


def test_to_df(adj_list1, adj_list2):
    assert adj_list1.adj_cols == adj_list2.adj_cols
    assert set(adj_list1.edge_types) == set(adj_list2.edge_types)

    for n in adj_list1.get_nodes():
        for edge_type in adj_list1.edge_types:
            assert adj_list1.get_adjacents(n, edge_type) == adj_list2.get_adjacents(
                n, edge_type
            )


def test_get_adjacents(adj_list1):
    assert set(adj_list1.get_adjacents("Use Case Diagram", "default")) == set(
        ["Use Case", "Actor (Uml)"]
    )


def test_get_adjacents2(adj_list1):
    assert set(adj_list1.get_adjacents("Use Case Diagram", "def2")) == set(
        [
            "Test Case",
            "User Interface Design Process",
            "User Requirements Document",
            "Software Requirements",
        ]
    )


def test_get_adjacents3(adj_list1):
    assert set(adj_list1.get_adjacents("Unified Modeling Language", "default")) == set(
        ["Use Case Diagram", "Class Diagram"]
    )


def test_get_adjacents4(adj_list1):
    assert set(adj_list1.get_adjacents("Unified Modeling Language", "def2")) == set(
        [
            "Activity Diagram",
            "Sequence Diagram",
            "Component Diagram",
            "Package Diagram",
            "Object Diagram",
            "Deployment Diagram",
            "Uml State Machine",
        ]
    )
