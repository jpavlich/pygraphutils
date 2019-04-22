import pandas as pd
import pygraphutils.representation.adjacency_list as al

if __name__ == "__main__":
    df = pd.read_excel("test_data/adj_list/topic/3. Construcción de software.xlsx")
    adj_list1 = al.from_df(df, adj_cols={1: "default", 4: "def2"})
    df2 = al.to_df(adj_list1)
    print(df2)

    df2.to_excel("tmp/out.xlsx")

