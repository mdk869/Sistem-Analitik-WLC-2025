import pandas as pd
import streamlit as st

from app.helper_gsheet import (
    load_worksheet_to_df,
    save_df_to_worksheet,
    append_row_to_worksheet,
    update_baris_dalam_worksheet,
    padam_baris_dari_worksheet
)

# =============================
# ✅ Setup Spreadsheet & Sheet
# =============================
SPREADSHEET_PESERTA = st.secrets["gsheet"]["data_peserta_id"]
SPREADSHEET_REKOD = st.secrets["gsheet"]["rekod_ranking"]

SHEET_PESERTA = "peserta"       # Betulkan dari 'data_peserta'
SHEET_REKOD = "rekod_berat_"


# =============================
# ✅ Load Data Peserta
# =============================
def load_data_peserta():
    df = load_worksheet_to_df(SPREADSHEET_PESERTA, SHEET_PESERTA)
    return df


# =============================
# ✅ Load Rekod Berat
# =============================
def load_rekod_berat_semua():
    df = load_worksheet_to_df(SPREADSHEET_PESERTA, SHEET_PESERTA)
    return df



# =============================
# ✅ Simpan Data Peserta
# =============================
def save_data_peserta(df):
    return save_df_to_worksheet(SPREADSHEET_PESERTA, SHEET_PESERTA, df)


# =============================
# ✅ Simpan Data Rekod Berat
# =============================
def save_rekod_berat(df):
    return save_df_to_worksheet(SPREADSHEET_REKOD, SHEET_REKOD, df)


# =============================
# ✅ Tambah Peserta
# =============================
def tambah_peserta_google_sheet(data_dict):
    return append_row_to_worksheet(SPREADSHEET_PESERTA, SHEET_PESERTA, data_dict)


# =============================
# ✅ Simpan Rekod Berat
# =============================
def simpan_rekod_berat(data_dict):
    return append_row_to_worksheet(SPREADSHEET_REKOD, SHEET_REKOD, data_dict)


# =============================
# ✅ Update Data Peserta
# =============================
def update_data_peserta(no_staf, update_dict):
    return update_baris_dalam_worksheet(
        SPREADSHEET_PESERTA, SHEET_PESERTA, "NoStaf", no_staf, update_dict
    )


# =============================
# ✅ Padam Peserta
# =============================
def padam_peserta_dari_sheet(no_staf):
    return padam_baris_dari_worksheet(
        SPREADSHEET_PESERTA, SHEET_PESERTA, "NoStaf", no_staf
    )
