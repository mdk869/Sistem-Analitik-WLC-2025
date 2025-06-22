import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import streamlit as st

# --- Setup sambungan Google Sheets
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
credentials = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"], scopes=scope
)
gc = gspread.authorize(credentials)

sheet = gc.open("data_peserta")
ws_peserta = sheet.worksheet("peserta")
ws_rekod = sheet.worksheet("rekod_berat")

# === Fungsi: Load Data
def load_data_cloud_or_local():
    df = pd.DataFrame(ws_peserta.get_all_records())
    return df

# === Fungsi: Tambah Peserta Baru
def tambah_peserta_google_sheet(nama, nostaf, tinggi, berat_awal):
    tarikh = datetime.now().strftime("%Y-%m-%d")
    row = [nama, nostaf, "", "", "", tinggi, berat_awal, tarikh, berat_awal, tarikh, "", ""]
    ws_peserta.append_row(row)

# === Fungsi: Kemaskini Berat
def kemaskini_berat_peserta(nama, berat_baru):
    data = ws_peserta.get_all_records()
    for idx, row in enumerate(data):
        if row["Nama"] == nama:
            ws_peserta.update_cell(idx+2, 9, berat_baru)  # BeratTerkini
            ws_peserta.update_cell(idx+2, 10, datetime.now().strftime("%Y-%m-%d"))  # TarikhTimbang
            break
    # Simpan ke sheet1 sebagai sejarah
    ws_rekod.append_row([nama, berat_baru, datetime.now().strftime("%Y-%m-%d")])

# === Fungsi: Sejarah Berat
def sejarah_berat(nama):
    rekod = pd.DataFrame(ws_rekod.get_all_records())
    rekod["Tarikh"] = pd.to_datetime(rekod["Tarikh"])
    return rekod[rekod["Nama"] == nama].sort_values("Tarikh")

# === Fungsi: Padam Peserta
def padam_peserta_dari_sheet(nama):
    data = ws_peserta.get_all_records()
    for idx, row in enumerate(data):
        if row["Nama"] == nama:
            ws_peserta.delete_row(idx + 2)
            break
