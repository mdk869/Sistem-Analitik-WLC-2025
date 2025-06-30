import streamlit as st
import pandas as pd
import gspread
from gspread.exceptions import WorksheetNotFound
from google.oauth2.service_account import Credentials


# =========================================
# ✅ Connect ke Google Spreadsheet
# =========================================
def connect_gsheet(spreadsheet_id):
    """
    Connect ke Google Spreadsheet menggunakan credentials dari st.secrets.
    """
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scope
    )
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(spreadsheet_id)
    return spreadsheet


# =========================================
# ✅ Load Sheet ke DataFrame
# =========================================
def load_worksheet_to_df(spreadsheet_id, sheet_name):
    try:
        spreadsheet = connect_gsheet(spreadsheet_id)
        worksheet = spreadsheet.worksheet(sheet_name)
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)
        return df
    except WorksheetNotFound:
        return pd.DataFrame()


# =========================================
# ✅ Save DataFrame ke Sheet (Replace)
# =========================================
def save_df_to_worksheet(spreadsheet_id, sheet_name, df):
    spreadsheet = connect_gsheet(spreadsheet_id)
    try:
        worksheet = spreadsheet.worksheet(sheet_name)
    except WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title=sheet_name, rows="1000", cols="50")

    worksheet.clear()
    if not df.empty:
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())


# =========================================
# ✅ Append Baris Baru ke Sheet
# =========================================
def append_row_to_worksheet(spreadsheet_id, sheet_name, data_dict):
    df = load_worksheet_to_df(spreadsheet_id, sheet_name)
    df = pd.concat([df, pd.DataFrame([data_dict])], ignore_index=True)
    save_df_to_worksheet(spreadsheet_id, sheet_name, df)


# =========================================
# ✅ Update Baris Berdasarkan Key
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
# ✅ Semak & Cipta Sheet Jika Tiada
# =========================================
def check_or_create_sheet(spreadsheet_id, sheet_name, header_list):
    spreadsheet = connect_gsheet(spreadsheet_id)
    try:
        spreadsheet.worksheet(sheet_name)
    except WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title=sheet_name, rows="1000", cols="50")
        worksheet.append_row(header_list)


# =========================================
# ✅ Load Banyak Sheet Ikut Prefix (Contoh rekod_berat_*)
# =========================================
def load_multiple_sheets_by_prefix(spreadsheet_id, prefix):
    spreadsheet = connect_gsheet(spreadsheet_id)
    sheet_list = [ws.title for ws in spreadsheet.worksheets() if ws.title.startswith(prefix)]

    df_list = []
    for sheet in sheet_list:
        df = load_worksheet_to_df(spreadsheet_id, sheet)
        if not df.empty:
            df["Sheet"] = sheet  # Tambah info sheet
            df_list.append(df)

    if df_list:
        return pd.concat(df_list, ignore_index=True)
    else:
        return pd.DataFrame()


# =========================================
# ✅ Padam Baris Berdasarkan Key
# =========================================
def delete_baris_dalam_worksheet(spreadsheet_id, sheet_name, key_column, key_value):
    df = load_worksheet_to_df(spreadsheet_id, sheet_name)
    if df.empty:
        return False

    new_df = df[df[key_column] != key_value]

    if len(new_df) == len(df):
        # Tidak jumpa key
        return False

    save_df_to_worksheet(spreadsheet_id, sheet_name, new_df)
    return True
