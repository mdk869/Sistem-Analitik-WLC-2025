import pandas as pd
from app.helper_connection import connect_gspread

# ===============================
# ✅ Fungsi Load Worksheet
# ===============================
def load_worksheet_to_df(spreadsheet_id, sheet_name):
    gc = connect_gspread()
    sh = gc.open_by_key(spreadsheet_id)
    try:
        ws = sh.worksheet(sheet_name)
        data = ws.get_all_records()
        df = pd.DataFrame(data)
        return df
    except Exception:
        return pd.DataFrame()

# ===============================
# ✅ Fungsi Save DataFrame ke Sheet
# ===============================
def save_df_to_worksheet(spreadsheet_id, sheet_name, df):
    gc = connect_gspread()
    sh = gc.open_by_key(spreadsheet_id)

    try:
        try:
            sh.worksheet(sheet_name).clear()
        except:
            sh.add_worksheet(title=sheet_name, rows=1000, cols=20)

        ws = sh.worksheet(sheet_name)
        ws.update([df.columns.values.tolist()] + df.values.tolist())
        return True
    except Exception:
        return False

# ===============================
# ✅ Append Row
# ===============================
def append_row_to_worksheet(spreadsheet_id, sheet_name, row_dict):
    gc = connect_gspread()
    sh = gc.open_by_key(spreadsheet_id)

    ws = None
    try:
        ws = sh.worksheet(sheet_name)
    except:
        ws = sh.add_worksheet(title=sheet_name, rows=1000, cols=20)

    header = ws.row_values(1)
    row = [row_dict.get(col, "") for col in header]
    ws.append_row(row)
    return True

# ===============================
# ✅ Update Baris Berdasarkan Key
# ===============================
def update_baris_dalam_worksheet(spreadsheet_id, sheet_name, key_col, key_value, update_dict):
    df = load_worksheet_to_df(spreadsheet_id, sheet_name)
    if df.empty:
        return False

    index = df[df[key_col] == key_value].index
    if not index.empty:
        idx = index[0]
        for col, value in update_dict.items():
            if col in df.columns:
                df.at[idx, col] = value
        save_df_to_worksheet(spreadsheet_id, sheet_name, df)
        return True
    return False

# ===============================
# ✅ Padam Baris Berdasarkan Key
# ===============================
def padam_baris_dari_worksheet(spreadsheet_id, sheet_name, key_col, key_value):
    df = load_worksheet_to_df(spreadsheet_id, sheet_name)
    if df.empty:
        return False

    df = df[df[key_col] != key_value]
    save_df_to_worksheet(spreadsheet_id, sheet_name, df)
    return True
