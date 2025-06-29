from app.helper_gsheet import(
    load_worksheet_to_df,
    tambah_data_peserta,
    append_data_to_worksheet,
    padam_baris_dari_worksheet
    
)
import pandas as pd
import streamlit as st


SPREADSHEET_PESERTA = st.secrets["gsheet"]["data_peserta_id"]
SPREADSHEET_REKOD = st.secrets["gsheet"]["rekod_ranking"]


def load_data_peserta():
    df = load_worksheet_to_df(SPREADSHEET_PESERTA, "peserta")
    return df


def load_rekod_berat_semua():
    df = load_worksheet_to_df(SPREADSHEET_REKOD, "rekod_berat")

    expected_header = ['Nama', 'NoStaf', 'Tarikh', 'Berat', 'SesiBulan']
    if not set(expected_header).issubset(df.columns):
        st.warning(f"⚠️ Header pada sheet 'rekod_berat' tidak lengkap. Jumpa: {df.columns.tolist()}")
        return pd.DataFrame()

    return df


def tambah_peserta_google_sheet(data_dict):
    SPREADSHEET_ID = st.secrets["gsheet"]["data_peserta_id"]
    SHEET_NAME = "data_peserta"

    return tambah_data_peserta(SPREADSHEET_ID, SHEET_NAME, data_dict)


def simpan_rekod_berat(data):
    """
    Simpan rekod berat baru ke sheet 'rekod_berat'.
    Data dalam bentuk dictionary.
    """
    spreadsheet_id = st.secrets["gsheet"]["rekod_ranking"]
    worksheet_name = "rekod_berat"

    status = append_data_to_worksheet(spreadsheet_id, worksheet_name, data)

    return status


def padam_peserta_dari_sheet(nama):
    """
    Padam peserta berdasarkan Nama dari sheet data_peserta.
    """
    spreadsheet_id = st.secrets["gsheet"]["data_peserta_id"]
    worksheet_name = "data_peserta"

    return padam_baris_dari_worksheet(spreadsheet_id, worksheet_name, "Nama", nama)