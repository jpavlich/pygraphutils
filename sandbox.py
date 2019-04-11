import pandas as pd
from pygraphutils.representation.adjacency_list import AdjacencyList

if __name__ == "__main__":
    df = pd.read_excel("test_data/adj_list/topic/3. Construcción de software.xlsx")
    al = AdjacencyList(df, adj_cols={1: "default", 3: "def2"})
    print(al.get_adjacents("Use Case Diagram", "default"))
    print(al.get_adjacents("Use Case Diagram", "def2"))

