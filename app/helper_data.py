# app/helper_data.py

import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import streamlit as st
from datetime import datetime
from app.helper_utils import (
    check_or_create_worksheet,
    kira_bmi,
    kategori_bmi_asia
)

# === Setup sambungan Google Sheet
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
credentials = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"], scopes=scope
)
gc = gspread.authorize(credentials)


# === Sambungan ke Spreadsheet Data Peserta
sheet_peserta = gc.open_by_key(st.secrets["gsheet"]["data_peserta_id"])

# === Worksheet utama
ws_peserta = check_or_create_worksheet(
    sheet_peserta,
    "peserta",
    ["Nama", "NoStaf", "Umur", "Jantina", "Jabatan", "Tinggi",
     "BeratAwal", "TarikhDaftar", "BeratTerkini", "TarikhTimbang", "BMI", "Kategori"]
)

ws_rekod = check_or_create_worksheet(
    sheet_peserta,
    "rekod_berat",
    ["Nama", "Tarikh", "Berat"]
)

# === Load Data Peserta
def load_data_peserta():
    try:
        df = pd.DataFrame(ws_peserta.get_all_records())
        return df
    except Exception as e:
        st.error(f"❌ Gagal load data peserta: {e}")
        return pd.DataFrame()


# === Load Rekod Berat
def load_rekod_berat():
    try:
        df = pd.DataFrame(ws_rekod.get_all_records())
        return df
    except Exception as e:
        st.error(f"❌ Gagal load rekod berat: {e}")
        return pd.DataFrame()


# === Backup Data jika Cloud gagal
def load_data_cloud_or_local():
    try:
        df = load_data_peserta()
        if df.empty:
            raise Exception("Data Google Sheet kosong")
    except Exception as e:
        st.warning(f"⚠️ Gagal load dari Google Sheet: {e}")
        df = pd.read_excel("data_peserta_backup.xlsx")
        st.info("Data dimuat dari backup Excel")
    return df


# === Tambah Peserta Baru
def tambah_peserta_google_sheet(nama, nostaf, umur, jantina, jabatan, tinggi, berat_awal, tarikh_daftar):
    try:
        berat_terkini = berat_awal
        tarikh_timbang = tarikh_daftar
        bmi = kira_bmi(berat_awal, tinggi)
        kategori = kategori_bmi_asia(bmi)

        data_baru = [
            nama, nostaf, umur, jantina, jabatan, tinggi,
            berat_awal, str(tarikh_daftar), berat_terkini,
            str(tarikh_timbang), bmi, kategori
        ]

        ws_peserta.append_row(data_baru)
        ws_rekod.append_row([nama, str(tarikh_timbang), berat_terkini])
    except Exception as e:
        st.error(f"Gagal tambah peserta: {e}")


# === Kemaskini Berat Terkini
def kemaskini_berat_peserta(nama, berat_baru, tarikh_baru):
    try:
        data = ws_peserta.get_all_records()

        for idx, row in enumerate(data):
            if row["Nama"] == nama:
                bmi_baru = kira_bmi(berat_baru, row["Tinggi"])
                kategori_baru = kategori_bmi_asia(bmi_baru)
                ws_peserta.update(f"I{idx+2}", berat_baru)         # BeratTerkini
                ws_peserta.update(f"J{idx+2}", str(tarikh_baru))   # TarikhTimbang
                ws_peserta.update(f"K{idx+2}", bmi_baru)           # BMI
                ws_peserta.update(f"L{idx+2}", kategori_baru)      # Kategori
                break

        ws_rekod.append_row([nama, str(tarikh_baru), berat_baru])
    except Exception as e:
        st.error(f"Gagal kemaskini berat: {e}")


# === Padam Peserta
def padam_peserta_dari_sheet(nama):
    try:
        data = ws_peserta.get_all_records()

        for idx, row in enumerate(data):
            if row["Nama"] == nama:
                ws_peserta.delete_rows(idx + 2)
                return True
        return False
    except Exception as e:
        st.error(f"Gagal padam peserta: {e}")
        return False


# === Dapatkan Berat Terkini
def get_berat_terkini():
    try:
        df_rekod = load_rekod_berat()
        if df_rekod.empty:
            return pd.DataFrame(columns=["Nama", "Berat", "Tarikh"])

        df_rekod["Tarikh"] = pd.to_datetime(df_rekod["Tarikh"], errors="coerce")

        df_latest = (
            df_rekod.sort_values('Tarikh', ascending=False)
            .drop_duplicates('Nama')
            .reset_index(drop=True)
        )

        return df_latest[["Nama", "Berat", "Tarikh"]]
    except Exception as e:
        st.error(f"Gagal dapatkan berat terkini: {e}")
        return pd.DataFrame(columns=["Nama", "Berat", "Tarikh"])


# === Sejarah Berat Individu
def sejarah_berat(nama):
    try:
        rekod = load_rekod_berat()

        if rekod.empty or "Tarikh" not in rekod.columns:
            return pd.DataFrame()

        rekod["Tarikh"] = pd.to_datetime(rekod["Tarikh"], format="mixed", errors="coerce")
        rekod = rekod.dropna(subset=["Tarikh"])
        return rekod[rekod["Nama"] == nama].sort_values("Tarikh")
    except Exception as e:
        st.error(f"Gagal load sejarah berat: {e}")
        return pd.DataFrame()
