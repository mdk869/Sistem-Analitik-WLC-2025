import pandas as pd
import streamlit as st
import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from google.oauth2.service_account import Credentials

# =========================================
# ✅ Connection Google Sheets
# =========================================
def connect_gsheet(spreadsheet_id):
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scopes
    )
    client = gspread.authorize(credentials)
    sh = client.open_by_key(spreadsheet_id)
    return sh

# =========================================
# ✅ Load Sheet ke DataFrame
# =========================================
def load_worksheet_to_df(spreadsheet_id, sheet_name):
    try:
        sh = connect_gsheet(spreadsheet_id)
        worksheet = sh.worksheet(sheet_name)
        df = get_as_dataframe(worksheet).dropna(how="all")
        df = df.dropna(axis=1, how="all")
        df = df.fillna("")
        return df
    except Exception:
        return pd.DataFrame()

# =========================================
# ✅ Save DataFrame ke Sheet
# =========================================
def save_df_to_worksheet(spreadsheet_id, sheet_name, df):
    sh = connect_gsheet(spreadsheet_id)
    try:
        worksheet = sh.worksheet(sheet_name)
        worksheet.clear()
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sh.add_worksheet(title=sheet_name, rows=1000, cols=26)

    set_with_dataframe(worksheet, df)

# =========================================
# ✅ Append Row ke Sheet
# =========================================
def append_row_to_worksheet(spreadsheet_id, sheet_name, data_dict):
    df_existing = load_worksheet_to_df(spreadsheet_id, sheet_name)

    df_new = pd.DataFrame([data_dict])

    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    save_df_to_worksheet(spreadsheet_id, sheet_name, df_combined)

# =========================================
# ✅ Update Row Berdasarkan Key
# =========================================
def update_baris_dalam_worksheet(spreadsheet_id, sheet_name, key_column, key_value, update_dict):
    df = load_worksheet_to_df(spreadsheet_id, sheet_name)
    if df.empty:
        return False

    index = df[df[key_column] == key_value].index
    if not index.empty:
        idx = index[0]
        for col, value in update_dict.items():
            if col in df.columns:
                df.at[idx, col] = value
        save_df_to_worksheet(spreadsheet_id, sheet_name, df)
        return True
    return False

# =========================================
# ✅ Delete Row Berdasarkan Key
# =========================================
def delete_baris_dalam_worksheet(spreadsheet_id, sheet_name, key_column, key_value):
    df = load_worksheet_to_df(spreadsheet_id, sheet_name)
    df = df[df[key_column] != key_value]
    save_df_to_worksheet(spreadsheet_id, sheet_name, df)
