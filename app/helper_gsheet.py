import pandas as pd
from app.helper_connection import client


def get_worksheet(spreadsheet, sheet_name):
    return spreadsheet.worksheet(sheet_name)


def load_worksheet_to_df(spreadsheet, sheet_name):
    ws = spreadsheet.worksheet(sheet_name)
    data = ws.get_all_records()
    df = pd.DataFrame(data)
    return df


def save_df_to_worksheet(spreadsheet, sheet_name, df):
    ws = spreadsheet.worksheet(sheet_name)
    ws.clear()
    ws.update([df.columns.values.tolist()] + df.values.tolist())
