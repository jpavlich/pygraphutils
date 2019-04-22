import pandas as pd
import pygraphutils.representation.adjacency_list as al
import pygraphutils.representation.edge_list as el
import uuid

if __name__ == "__main__":
    df = pd.read_excel("test_data/adj_list/topic/3. Construcción de software.xlsx")
    adj_list1 = al.from_df(df, adj_cols={1: "default", 4: "def2"})
    G = al.to_graph(adj_list1)
    for n in G.nodes:
        for d in range(0, 10):
            G.nodes[n]["d%d" % d] = str(uuid.uuid1())

    for e in G.edges:
        for d in range(0, 10):
            G.edges[e]["d%d" % d] = str(uuid.uuid1())
    nodes_df, edges_df = el.to_df(G)
    # edges_df.to_excel("tmp/out.xlsx")

    G2 = el.from_df(nodes_df, edges_df)
    print(G2.nodes)
    print(G2.edges)
    n2, e2 = el.to_df(G2)
    n2.to_excel("tmp/out.xlsx")

