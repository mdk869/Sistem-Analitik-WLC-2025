import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import streamlit as st
import pytz
from app.helper_logic import kira_bmi, kategori_bmi_asia

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

# === Fungsi: Tambah Peserta ===
def tambah_peserta_google_sheet(nama, nostaf, umur, jantina, jabatan, tinggi, berat_awal, tarikh_timbang):
    tinggi_m = tinggi / 100
    bmi = berat_awal / (tinggi_m ** 2)
    kategori = kategori_bmi_asia(bmi)
    tarikh_daftar = datetime.now(pytz.timezone("Asia/Kuala_Lumpur")).strftime("%Y-%m-%d %H:%M:%S")

    ws_peserta.append_row([
        nama, nostaf, umur, jantina, jabatan, tinggi, berat_awal, tarikh_daftar, berat_awal, tarikh_timbang, round(bmi, 2), kategori
    ])


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
    rekod.columns = [str(col).strip() for col in rekod.columns]  # Bersih ruang kosong

    if rekod.empty or "Tarikh" not in rekod.columns:
        return pd.DataFrame()  # Pulangkan dataframe kosong

    rekod["Tarikh"] = pd.to_datetime(rekod["Tarikh"], format="mixed", errors="coerce")
    return rekod[rekod["Nama"] == nama].sort_values("Tarikh")



# === Fungsi: Kemaskini Berat
def kemaskini_berat_peserta(nama, berat_baru):
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")

    # 1. Update berat terkini di sheet peserta
    df = pd.DataFrame(ws_peserta.get_all_records())
    for idx, row in df.iterrows():
        if row["Nama"] == nama:
            ws_peserta.update_cell(idx + 2, df.columns.get_loc("BeratTerkini") + 1, berat_baru)
            ws_peserta.update_cell(idx + 2, df.columns.get_loc("TarikhTimbang") + 1, today)
            break

    # 2. Rekod sejarah berat (rekod_berat)
    ws_rekod.append_row([nama, berat_baru, today])


# === Fungsi: Padam Peserta
def padam_peserta_dari_sheet(nama):
    data = ws_peserta.get_all_records()
    for idx, row in enumerate(data):
        if row["Nama"] == nama:
            ws_peserta.delete_row(idx + 2)
            break
