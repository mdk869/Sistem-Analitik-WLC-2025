# app/helper_data.py

import streamlit as st
import pandas as pd
from datetime import datetime

from app.helper_connection import SPREADSHEET_PESERTA, SPREADSHEET_RANKING
from app.helper_gsheet import load_worksheet_to_df, save_df_to_worksheet
from app.helper_gsheet_utils import check_and_create_worksheet
from app.helper_utils import proses_data_peserta, kategori_bmi_asia
from app.helper_log import log_dev, log_error


# ==============================================
# ✅ Header Template
# ==============================================
HEADER_PESERTA = [
    "Nama", "NoStaf", "Umur", "Jantina", "Jabatan",
    "Tinggi", "BeratAwal", "TarikhDaftar",
    "BeratTerkini", "TarikhTimbang", "BMI", "Kategori"
]

HEADER_REKOD_BERAT = ["Nama", "NoStaf", "Tarikh", "Berat", "BMI", "Kategori"]


# ==============================================
# ✅ Load Data Peserta
# ==============================================
def load_data_peserta() -> pd.DataFrame:
    try:
        check_and_create_worksheet(SPREADSHEET_PESERTA, "data_peserta", HEADER_PESERTA)
        df = load_worksheet_to_df(SPREADSHEET_PESERTA, "data_peserta")
        if df.empty:
            return pd.DataFrame(columns=HEADER_PESERTA)
        df = proses_data_peserta(df)
        return df
    except Exception as e:
        log_error(f"Gagal load data peserta: {e}")
        st.error(f"❌ Error load data peserta: {e}")
        return pd.DataFrame(columns=HEADER_PESERTA)


# ==============================================
# ✅ Simpan Data Peserta
# ==============================================
def save_data_peserta(df: pd.DataFrame) -> bool:
    try:
        return save_df_to_worksheet(SPREADSHEET_PESERTA, "data_peserta", df)
    except Exception as e:
        log_error(f"Gagal simpan data peserta: {e}")
        st.error(f"❌ Error save data peserta: {e}")
        return False


# ==============================================
# ✅ Tambah Peserta Baru
# ==============================================
def tambah_peserta(new_data: dict) -> bool:
    try:
        df = load_data_peserta()

        tinggi = new_data.get("Tinggi")
        berat = new_data.get("BeratAwal")

        bmi = round(berat / ((tinggi / 100) ** 2), 2) if tinggi and berat else None
        kategori = kategori_bmi_asia(bmi)

        peserta = {
            **new_data,
            "BeratTerkini": berat,
            "TarikhTimbang": new_data.get("TarikhDaftar"),
            "BMI": bmi,
            "Kategori": kategori
        }

        df = pd.concat([df, pd.DataFrame([peserta])], ignore_index=True)
        save_data_peserta(df)
        log_dev("Tambah Peserta", f"{peserta['Nama']}")
        return True

    except Exception as e:
        log_error(f"Gagal tambah peserta: {e}")
        return False


# ==============================================
# ✅ Update Data Peserta
# ==============================================
def update_data_peserta(nama: str, data: dict) -> bool:
    try:
        df = load_data_peserta()
        if nama not in df["Nama"].values:
            st.warning(f"Nama {nama} tidak ditemui.")
            return False

        idx = df[df["Nama"] == nama].index[0]

        for k, v in data.items():
            if k in df.columns:
                df.at[idx, k] = v

        save_data_peserta(df)
        log_dev("Update Peserta", f"{nama}")
        return True

    except Exception as e:
        log_error(f"Gagal update peserta: {e}")
        return False


# ==============================================
# ✅ Padam Peserta
# ==============================================
def padam_peserta(nama: str) -> bool:
    try:
        df = load_data_peserta()
        if nama not in df["Nama"].values:
            st.warning(f"Nama {nama} tidak ditemui.")
            return False

        df = df[df["Nama"] != nama]
        save_data_peserta(df)
        log_dev("Padam Peserta", f"{nama}")
        return True

    except Exception as e:
        log_error(f"Gagal padam peserta: {e}")
        return False


# ==============================================
# ✅ Load Rekod Berat Semua
# ==============================================
def load_rekod_berat_semua() -> pd.DataFrame:
    try:
        check_and_create_worksheet(SPREADSHEET_RANKING, "rekod_berat", HEADER_REKOD_BERAT)
        df = load_worksheet_to_df(SPREADSHEET_RANKING, "rekod_berat")
        if df.empty:
            return pd.DataFrame(columns=HEADER_REKOD_BERAT)
        df["Tarikh"] = pd.to_datetime(df["Tarikh"], errors='coerce')
        return df
    except Exception as e:
        log_error(f"Gagal load rekod berat: {e}")
        st.error(f"❌ Error load rekod berat: {e}")
        return pd.DataFrame(columns=HEADER_REKOD_BERAT)


# ==============================================
# ✅ Simpan Rekod Berat
# ==============================================
def simpan_rekod_berat(nama: str, nostaf: str, tarikh: str, berat: float) -> bool:
    try:
        bmi = None
        kategori = None

        df_peserta = load_data_peserta()
        peserta = df_peserta[df_peserta["Nama"] == nama]

        if not peserta.empty:
            tinggi = peserta.iloc[0]["Tinggi"]
            bmi = round(berat / ((tinggi / 100) ** 2), 2)
            kategori = kategori_bmi_asia(bmi)

            # ✅ Update ke data peserta
            update_data_peserta(nama, {
                "BeratTerkini": berat,
                "TarikhTimbang": tarikh,
                "BMI": bmi,
                "Kategori": kategori
            })

        rekod = {
            "Nama": nama,
            "NoStaf": nostaf,
            "Tarikh": tarikh,
            "Berat": berat,
            "BMI": bmi,
            "Kategori": kategori
        }

        df_rekod = load_rekod_berat_semua()
        df_rekod = pd.concat([df_rekod, pd.DataFrame([rekod])], ignore_index=True)

        save_df_to_worksheet(SPREADSHEET_RANKING, "rekod_berat", df_rekod)
        log_dev("Rekod Berat", f"{nama} - {berat}kg pada {tarikh}")
        return True

    except Exception as e:
        log_error(f"Gagal simpan rekod berat: {e}")
        return False
