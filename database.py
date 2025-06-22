# database.py

import streamlit as st
import gspread
import pandas as pd
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from google.oauth2.service_account import Credentials

# ========== CREDENTIALS DARI st.secrets ==========

SERVICE_ACCOUNT_INFO = st.secrets["google_service_account"]

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO, scopes=SCOPE)
client = gspread.authorize(creds)

# ========== MAKLUMAT SPREADSHEET DAN FOLDER GOOGLE DRIVE ==========

SPREADSHEET_ID = st.secrets["google_service_account"]["spreadsheet_id"]
DRIVE_FOLDER_ID = st.secrets["google_service_account"]["drive_folder_id"]

# ========== UTAMA: Fungsi Worksheet ==========

def get_worksheet(sheet_name: str):
    """Dapatkan worksheet berdasarkan nama"""
    sh = client.open_by_key(SPREADSHEET_ID)
    return sh.worksheet(sheet_name)


# ========== BACA DATA ==========

def baca_data(sheet_name: str):
    """Pulangkan semua data dari sheet sebagai DataFrame"""
    ws = get_worksheet(sheet_name)
    df = get_as_dataframe(ws, evaluate_formulas=True).dropna(how="all")
    return df


# ========== TAMBAH DATA (append) ==========

def tambah_baris(sheet_name: str, data_dict: dict):
    """Tambah baris baharu ke dalam sheet"""
    ws = get_worksheet(sheet_name)
    headers = ws.row_values(1)
    values = [data_dict.get(col, "") for col in headers]
    ws.append_row(values)


# ========== SIMPAN DATA (replace all) ==========

def simpan_semula(sheet_name: str, df: pd.DataFrame):
    """Gantikan semua isi sheet dengan DataFrame baharu"""
    ws = get_worksheet(sheet_name)
    ws.clear()
    set_with_dataframe(ws, df)


# ========== KEMASKINI BARIS BERDASARKAN ID ==========

def kemaskini_baris(sheet_name: str, id_column: str, id_value, updated_data: dict):
    df = get_as_dataframe(get_worksheet(sheet_name)).fillna("")
    idx_match = df[df[id_column] == id_value].index
    if not idx_match.empty:
        for key, val in updated_data.items():
            if key in df.columns:
                df.at[idx_match[0], key] = val
        simpan_semula(sheet_name, df)
        return True
    return False


# ========== PADAM BARIS ==========

def padam_baris(sheet_name: str, id_column: str, id_value):
    df = baca_data(sheet_name)
    df = df[df[id_column] != id_value]
    simpan_semula(sheet_name, df)
