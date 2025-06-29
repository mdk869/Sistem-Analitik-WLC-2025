import pandas as pd
import streamlit as st
from app.helper_logic import kira_bmi, kategori_bmi_asia
from app.helper_gsheet import (
    load_worksheet_to_df,
    save_df_to_worksheet,
    append_row_to_worksheet,
    update_baris_dalam_worksheet,
    padam_baris_dari_worksheet
)

# ===============================
# ✅ Setup Spreadsheet
# ===============================
SPREADSHEET_PESERTA = st.secrets["gsheet"]["data_peserta_id"]
SPREADSHEET_REKOD = st.secrets["gsheet"]["rekod_ranking"]

SHEET_PESERTA = "peserta"
SHEET_REKOD = "rekod_berat"

# ===============================
# ✅ Load Data
# ===============================
def load_data_peserta():
    return load_worksheet_to_df(SPREADSHEET_PESERTA, SHEET_PESERTA)

def load_rekod_berat_semua():
    return load_worksheet_to_df(SPREADSHEET_REKOD, SHEET_REKOD)

# ===============================
# ✅ Simpan Data
# ===============================
def save_data_peserta(df):
    return save_df_to_worksheet(SPREADSHEET_PESERTA, SHEET_PESERTA, df)

def save_rekod_berat(df):
    return save_df_to_worksheet(SPREADSHEET_REKOD, SHEET_REKOD, df)

# ===============================
# ✅ Tambah Peserta
# ===============================
def daftar_peserta(nama, nostaf, umur, jantina, jabatan, tinggi, berat_awal, tarikh):
    bmi = kira_bmi(berat_awal, tinggi)
    kategori = kategori_bmi_asia(bmi)

    data = {
        "Nama": nama,
        "NoStaf": nostaf,
        "Umur": umur,
        "Jantina": jantina,
        "Jabatan": jabatan,
        "Tinggi": tinggi,
        "BeratAwal": berat_awal,
        "TarikhDaftar": str(tarikh),
        "BeratTerkini": berat_awal,
        "TarikhTimbang": str(tarikh),
        "BMI": bmi,
        "Kategori": kategori
    }
    return append_row_to_worksheet(SPREADSHEET_PESERTA, SHEET_PESERTA, data)

# ===============================
# ✅ Rekod Berat
# ===============================
def simpan_rekod_berat(data):
    """
    Simpan rekod timbang dan update data peserta.
    Parameter data:
    {
        "Nama": str,
        "NoStaf": str,
        "Tarikh": str (yyyy-mm-dd),
        "Berat": float,
        "SesiBulan": str (yyyy-mm)
    }
    """
    append_row_to_worksheet(SPREADSHEET_REKOD, SHEET_REKOD, data)

    df = load_data_peserta()
    idx = df[df["Nama"].str.lower() == data["Nama"].lower()].index

    if not idx.empty:
        tinggi = df.loc[idx[0], "Tinggi"]
        bmi = kira_bmi(data["Berat"], tinggi)
        kategori = kategori_bmi_asia(bmi)

        update = {
            "BeratTerkini": data["Berat"],
            "TarikhTimbang": data["Tarikh"],
            "BMI": bmi,
            "Kategori": kategori
        }
        update_baris_dalam_worksheet(SPREADSHEET_PESERTA, SHEET_PESERTA, "Nama", data["Nama"], update)
        return True
    return False


# ===============================
# ✅ Update Data Peserta
# ===============================
def update_data_peserta(nama, nostaf, umur, jantina, jabatan, tinggi, berat_terkini, tarikh_timbang, bmi, kategori):
    update = {
        "Nama": nama,
        "NoStaf": nostaf,
        "Umur": umur,
        "Jantina": jantina,
        "Jabatan": jabatan,
        "Tinggi": tinggi,
        "BeratTerkini": berat_terkini,
        "TarikhTimbang": str(tarikh_timbang),
        "BMI": bmi,
        "Kategori": kategori
    }
    return update_baris_dalam_worksheet(SPREADSHEET_PESERTA, SHEET_PESERTA, "Nama", nama, update)

# ===============================
# ✅ Padam Peserta
# ===============================
def padam_peserta_dari_sheet(nama):
    return padam_baris_dari_worksheet(SPREADSHEET_PESERTA, SHEET_PESERTA, "Nama", nama)
