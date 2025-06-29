import pandas as pd
import streamlit as st
from datetime import datetime

from app.helper_logic import kira_bmi, kategori_bmi_asia
from app.helper_gsheet import (
    load_worksheet_to_df,
    save_df_to_worksheet,
    append_row_to_worksheet,
    update_baris_dalam_worksheet,
    padam_baris_dari_worksheet
)

# =========================================
# ✅ Setup Spreadsheet & Sheet
# =========================================
SPREADSHEET_PESERTA = st.secrets["gsheet"]["data_peserta_id"]
SPREADSHEET_REKOD = st.secrets["gsheet"]["rekod_ranking"]

SHEET_PESERTA = "peserta"
SHEET_REKOD = "rekod_berat"

# =========================================
# ✅ Load Data Peserta
# =========================================
def load_data_peserta():
    try:
        df = load_worksheet_to_df(SPREADSHEET_PESERTA, SHEET_PESERTA)
        return df
    except Exception as e:
        st.error(f"❌ Gagal buka sheet 'peserta': {e}")
        return pd.DataFrame()

# =========================================
# ✅ Load Data Rekod Berat
# =========================================
def load_rekod_berat_semua():
    try:
        df = load_worksheet_to_df(SPREADSHEET_REKOD, SHEET_REKOD)
        return df
    except Exception as e:
        st.error(f"❌ Gagal buka sheet 'rekod_berat': {e}")
        return pd.DataFrame()

# =========================================
# ✅ Simpan Data Penuh ke Sheet
# =========================================
def save_data_peserta(df):
    return save_df_to_worksheet(SPREADSHEET_PESERTA, SHEET_PESERTA, df)

def save_rekod_berat(df):
    return save_df_to_worksheet(SPREADSHEET_REKOD, SHEET_REKOD, df)

# =========================================
# ✅ Tambah Peserta Baru
# =========================================
def tambah_peserta_google_sheet(data_dict):
    return append_row_to_worksheet(SPREADSHEET_PESERTA, SHEET_PESERTA, data_dict)

def daftar_peserta(
    nama, nostaf, umur, jantina, jabatan,
    tinggi, berat_awal, tarikh
):
    bmi = kira_bmi(berat_awal, tinggi)
    kategori = kategori_bmi_asia(bmi)

    data = {
        "Nama": str(nama),
        "NoStaf": str(nostaf),
        "Umur": int(umur),
        "Jantina": str(jantina),
        "Jabatan": str(jabatan),
        "Tinggi": int(tinggi),
        "BeratAwal": float(berat_awal),
        "TarikhDaftar": tarikh.strftime("%Y-%m-%d") if isinstance(tarikh, (datetime, pd.Timestamp)) else str(tarikh),
        "BeratTerkini": float(berat_awal),
        "TarikhTimbang": tarikh.strftime("%Y-%m-%d") if isinstance(tarikh, (datetime, pd.Timestamp)) else str(tarikh),
        "BMI": round(float(bmi), 2),
        "Kategori": kategori
    }

    return tambah_peserta_google_sheet(data)

# =========================================
# ✅ Simpan Rekod Timbang
# =========================================
def simpan_rekod_berat(nama, tarikh, berat):
    data = {
        "Nama": str(nama),
        "Tarikh": tarikh.strftime("%Y-%m-%d") if isinstance(tarikh, (datetime, pd.Timestamp)) else str(tarikh),
        "Berat": float(berat),
        "SesiBulan": tarikh.strftime("%Y-%m") if isinstance(tarikh, (datetime, pd.Timestamp)) else str(tarikh)[:7]
    }

    try:
        # Simpan ke sheet rekod_berat
        rekod_status = append_row_to_worksheet(SPREADSHEET_REKOD, SHEET_REKOD, data)

        # Update berat terkini peserta
        update_status = update_data_peserta(
            nama,
            {
                "BeratTerkini": float(berat),
                "TarikhTimbang": data["Tarikh"],
                "BMI": round(kira_bmi(berat,  float(load_data_peserta().query("Nama == @nama")["Tinggi"].values[0])), 2),
                "Kategori": kategori_bmi_asia(
                    kira_bmi(berat, float(load_data_peserta().query("Nama == @nama")["Tinggi"].values[0]))
                )
            }
        )

        return {"rekod_berat": rekod_status, "update_peserta": update_status}

    except Exception as e:
        st.error(f"❌ Gagal simpan rekod berat: {e}")
        return {"rekod_berat": False, "update_peserta": False}

# =========================================
# ✅ Update Data Peserta
# =========================================
def update_data_peserta(no_staf, update_dict):
    return update_baris_dalam_worksheet(
        SPREADSHEET_PESERTA, SHEET_PESERTA, "NoStaf", no_staf, update_dict
    )

# =========================================
# ✅ Padam Peserta
# =========================================
def padam_peserta_dari_sheet(no_staf):
    return padam_baris_dari_worksheet(
        SPREADSHEET_PESERTA, SHEET_PESERTA, "NoStaf", no_staf
    )
