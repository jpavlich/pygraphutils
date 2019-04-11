import pandas as pd
from typing import List
import math


def get_sheets_from_xls(url, sheet_names) -> List[pd.DataFrame]:
    xls = pd.ExcelFile(url)
    return [xls.parse(sheet_name) for sheet_name in sheet_names]


def is_valid(value):
    return isinstance(value, str) or not math.isnan(value)


def get_col_number(df, col):
    if isinstance(col, int):
        return col
    elif isinstance(col, str):
        return df.columns.get_loc(col)
    else:
        raise Exception("column %s does not exist" % col)
