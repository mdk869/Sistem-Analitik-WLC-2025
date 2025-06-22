import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import streamlit as st

# --- Setup sambungan Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_service_account_info(
    st.secrets["gcp_service_account"], scopes=scope
)
gc = gspread.authorize(credentials)
sheet = gc.open_by_key("1K9JiK8FE1-Cd9fYnDU8Pzqj42TWOGi10wHzHt0avbJ0")

ws_peserta = sheet.worksheet("peserta")
ws_rekod = sheet.worksheet("sheet1")

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

# === Fungsi: Padam Peserta
def padam_peserta_dari_sheet(nama):
    data = ws_peserta.get_all_records()
    for idx, row in enumerate(data):
        if row["Nama"] == nama:
            ws_peserta.delete_row(idx + 2)
            break
