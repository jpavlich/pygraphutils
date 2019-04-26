import pandas as pd
from typing import List
import math
import pygraphutils.util.file as f
import os


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


def to_excel(filename, sheet_names, dfs, formats=None, save=True, col_width=40):
    if not f.mkdir(os.path.dirname(filename)):
        return None

    # https://stackoverflow.com/a/44289401
    import pandas.io.formats.excel

    pandas.io.formats.excel.header_style = None
    writer = pd.ExcelWriter(filename, engine="xlsxwriter")
    for i, (df, sheet_name) in enumerate(zip(dfs, sheet_names)):
        df.to_excel(writer, sheet_name=sheet_name)
        worksheet = writer.sheets[sheet_name]
        if isinstance(df, pd.DataFrame):
            worksheet.autofilter(0, 1, 30000, len(df.columns))
        # worksheet.set_column("B:Z", 32)
        if formats and i < len(formats):
            for col, fmt in enumerate(formats[i]):
                if fmt:
                    fmt = writer.book.add_format(fmt)
                    worksheet.set_column(col + 1, col + 1, col_width, fmt)
                else:
                    worksheet.set_column(col + 1, col + 1, col_width)
        else:
            for col, _ in enumerate(df.columns):
                worksheet.set_column(col + 1, col + 1, col_width)

        header_fmt = writer.book.add_format({"text_wrap": True})
        worksheet.set_row(0, 30, header_fmt)
        worksheet.freeze_panes(1, 1)
    if save:
        writer.save()
        print("Saved %s" % filename)
    return writer
