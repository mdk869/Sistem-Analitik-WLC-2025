# helper_data.py

import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import streamlit as st
import pytz

from app.helper_logic import kira_bmi, kategori_bmi_asia


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

# === Check dan create worksheet jika tidak wujud
def check_or_create_worksheet(sheet, name, header):
    try:
        ws = sheet.worksheet(name)
    except:
        ws = sheet.add_worksheet(title=name, rows="1000", cols="20")
        ws.append_row(header)
    return ws

# === Worksheet peserta
ws_peserta = check_or_create_worksheet(
    sheet_peserta,
    "peserta",
    ["Nama", "NoStaf", "Umur", "Jantina", "Jabatan", "Tinggi",
     "BeratAwal", "TarikhDaftar", "BeratTerkini", "TarikhTimbang", "BMI", "Kategori"]
)

# === Worksheet rekod berat
ws_rekod = check_or_create_worksheet(
    sheet_peserta,
    "rekod_berat",
    ["Nama", "Tarikh", "Berat"]
)

# === Load Data Peserta
def load_data_peserta():
    return pd.DataFrame(ws_peserta.get_all_records())

# === Load Rekod Berat
def load_rekod_berat():
    return pd.DataFrame(ws_rekod.get_all_records())

# === Load Data Backup jika error
def load_data_cloud_or_local():
    try:
        df = load_data_peserta()
    except Exception as e:
        st.warning(f"⚠️ Gagal load dari Google Sheet: {e}")
        df = pd.read_excel("data_peserta_backup.xlsx")
        st.info("Data dimuat dari backup Excel")
    return df

# === Tambah Peserta Baru
def tambah_peserta_google_sheet(nama, nostaf, umur, jantina, jabatan, tinggi, berat_awal, tarikh_daftar):
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

# === Kemaskini Berat Terkini
def kemaskini_berat_peserta(nama, berat_baru, tarikh_baru):
    data = ws_peserta.get_all_records()

    for idx, row in enumerate(data):
        if row["Nama"] == nama:
            bmi_baru = kira_bmi(berat_baru, row["Tinggi"])
            kategori_baru = kategori_bmi_asia(bmi_baru)
            ws_peserta.update(f"I{idx+2}", berat_baru)
            ws_peserta.update(f"J{idx+2}", str(tarikh_baru))
            ws_peserta.update(f"K{idx+2}", bmi_baru)
            ws_peserta.update(f"L{idx+2}", kategori_baru)
            break

    ws_rekod.append_row([nama, str(tarikh_baru), berat_baru])

# === Padam Peserta
def padam_peserta_dari_sheet(nama):
    data = ws_peserta.get_all_records()

    for idx, row in enumerate(data):
        if row["Nama"] == nama:
            ws_peserta.delete_rows(idx + 2)
            return True
    return False

# === Get Berat Terkini
def get_berat_terkini():
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

# === Sejarah Berat Individu
def sejarah_berat(nama):
    rekod = pd.DataFrame(ws_rekod.get_all_records())
    rekod.columns = [str(col).strip() for col in rekod.columns]

    if rekod.empty or "Tarikh" not in rekod.columns:
        return pd.DataFrame()
    rekod["Tarikh"] = pd.to_datetime(rekod["Tarikh"], format="mixed", errors="coerce")
    rekod = rekod.dropna(subset=["Tarikh"])
    return rekod[rekod["Nama"] == nama].sort_values("Tarikh")
