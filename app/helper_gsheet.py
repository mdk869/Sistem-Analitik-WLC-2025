import gspread
import pandas as pd
import streamlit as st


# ✅ Sambungan ke Google Sheet
def connect_gsheet():
    gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
    return gc


# ✅ Buka worksheet
def open_worksheet(spreadsheet_id, worksheet_name):
    try:
        gc = connect_gsheet()
        sh = gc.open_by_key(spreadsheet_id)
        worksheet = sh.worksheet(worksheet_name)
        return worksheet
    except Exception as e:
        st.error(f"❌ Gagal buka sheet '{worksheet_name}': {e}")
        return None


# ✅ Load worksheet ke DataFrame
def load_worksheet_to_df(spreadsheet_id, worksheet_name):
    ws = open_worksheet(spreadsheet_id, worksheet_name)
    if ws:
        data = ws.get_all_records()
        df = pd.DataFrame(data)
        return df
    return pd.DataFrame()


# ✅ Simpan DataFrame ke worksheet (overwrite)
def save_df_to_worksheet(spreadsheet_id, worksheet_name, df):
    ws = open_worksheet(spreadsheet_id, worksheet_name)
    if ws is None:
        return False

    ws.clear()
    if df.empty:
        return True

    ws.update([df.columns.values.tolist()] + df.values.tolist())
    return True


# ✅ Append satu row ke worksheet
def append_row_to_worksheet(spreadsheet_id, worksheet_name, data_dict):
    ws = open_worksheet(spreadsheet_id, worksheet_name)
    if ws is None:
        return False

    existing_data = ws.get_all_values()

    if not existing_data:
        headers = list(data_dict.keys())
        ws.append_row(headers)

    row = list(data_dict.values())
    ws.append_row(row)

    return True


# ✅ Padam baris berdasarkan column_key dan value
def padam_baris_dari_worksheet(spreadsheet_id, worksheet_name, column_key, value):
    ws = open_worksheet(spreadsheet_id, worksheet_name)
    if ws is None:
        return False

    data = ws.get_all_records()

    if not data:
        return False

    df = pd.DataFrame(data)

    if column_key not in df.columns:
        st.warning(f"⚠️ Column '{column_key}' tidak wujud dalam sheet '{worksheet_name}'")
        return False

    if value not in df[column_key].values:
        return False

    df = df[df[column_key] != value]

    ws.clear()
    if not df.empty:
        ws.update([df.columns.values.tolist()] + df.values.tolist())

    return True


# ✅ Update baris berdasarkan key_column dan key_value
def update_baris_dalam_worksheet(spreadsheet_id, worksheet_name, key_column, key_value, update_dict):
    ws = open_worksheet(spreadsheet_id, worksheet_name)
    if ws is None:
        return False

    data = ws.get_all_records()

    if not data:
        return False

    df = pd.DataFrame(data)

    if key_column not in df.columns:
        st.warning(f"⚠️ Column '{key_column}' tidak wujud dalam sheet '{worksheet_name}'")
        return False

    if key_value not in df[key_column].values:
        return False

    for col, val in update_dict.items():
        if col in df.columns:
            df.loc[df[key_column] == key_value, col] = val
        else:
            st.warning(f"⚠️ Column '{col}' tidak wujud dalam sheet '{worksheet_name}'")

    ws.clear()
    if not df.empty:
        ws.update([df.columns.values.tolist()] + df.values.tolist())

    return True
