import pandas as pd
from typing import Dict, Any

BASE_STYLE = "_base_style"


def from_dfs(dfs: Dict[Any, pd.DataFrame]):
    style_layers = {}

    default_style = None
    if BASE_STYLE in dfs:
        default_style = dfs.pop(BASE_STYLE).to_dict("index")[0]

    for sheet_name, df in dfs.items():
        df = df.set_index(df.columns[0])
        style_layers[sheet_name] = df.to_dict("index")

    if default_style:
        return {BASE_STYLE: default_style, "style_layers": style_layers}
    else:
        return {"style_layers": style_layers}
