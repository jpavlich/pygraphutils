import pandas as pd
from typing import Dict, Any


def from_dfs(dfs: Dict[Any, pd.DataFrame]):
    style = {}
    for sheet_name, df in dfs.items():
        df = df.set_index(df.columns[0])
        style[sheet_name] = df.to_dict("index")
    return style
