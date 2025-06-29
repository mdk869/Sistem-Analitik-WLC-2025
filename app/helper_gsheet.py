import pandas as pd
from app.helper_connection import connect_gspread


def load_worksheet_to_df(spreadsheet_id, sheet_name):
    client = connect_gspread()
    sheet = client.open_by_key(spreadsheet_id)
    ws = sheet.worksheet(sheet_name)
    data = ws.get_all_records()
    df = pd.DataFrame(data)
    return df


def save_df_to_worksheet(spreadsheet_id, sheet_name, df):
    client = connect_gspread()
    sheet = client.open_by_key(spreadsheet_id)
    try:
        ws = sheet.worksheet(sheet_name)
    except:
        ws = sheet.add_worksheet(title=sheet_name, rows="1000", cols="20")
    ws.clear()
    ws.update([df.columns.values.tolist()] + df.values.tolist())
    return True


def append_row_to_worksheet(spreadsheet_id, sheet_name, data_dict):
    client = connect_gspread()
    sheet = client.open_by_key(spreadsheet_id)
    ws = sheet.worksheet(sheet_name)
    row = [data_dict.get(col, "") for col in ws.row_values(1)]
    ws.append_row(row)
    return True


def update_baris_dalam_worksheet(spreadsheet_id, sheet_name, key_col, key_value, update_dict):
    df = load_worksheet_to_df(spreadsheet_id, sheet_name)
    if key_col not in df.columns:
        return False
    idx = df[df[key_col] == key_value].index
    if idx.empty:
        return False
    for k, v in update_dict.items():
        if k in df.columns:
            df.loc[idx, k] = v
    save_df_to_worksheet(spreadsheet_id, sheet_name, df)
    return True


def padam_baris_dari_worksheet(spreadsheet_id, sheet_name, key_col, key_value):
    df = load_worksheet_to_df(spreadsheet_id, sheet_name)
    df = df[df[key_col] != key_value]
    save_df_to_worksheet(spreadsheet_id, sheet_name, df)
    return True
