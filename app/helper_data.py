import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import streamlit as st
import pytz

# === Import logik tambahan ===
from app.helper_logic import kira_bmi, kategori_bmi_asia

# === Setup sambungan Google Sheet ===
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
credentials = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"], scopes=scope
)
gc = gspread.authorize(credentials)

sheet = gc.open(st.secrets["gsheet"]["spreadsheet"])
ws_peserta = sheet.worksheet("peserta")
ws_rekod = sheet.worksheet("rekod_berat")


# === Load Data Peserta ===
def load_data_peserta():
    return pd.DataFrame(ws_peserta.get_all_records())


# === Load Rekod Berat ===
def load_rekod_berat():
    return pd.DataFrame(ws_rekod.get_all_records())


# === Tambah Peserta Baru ===
def tambah_peserta_google_sheet(nama, nostaf, umur, jantina, jabatan,
                                 tinggi, berat_awal, berat_terkini,
                                 tarikh_timbang, bmi, kategori):
    tarikh_daftar = datetime.now(pytz.timezone("Asia/Kuala_Lumpur")).strftime("%Y-%m-%d %H:%M:%S")
    ws_peserta.append_row([
        nama, nostaf, umur, jantina, jabatan, tinggi,
        berat_awal, tarikh_daftar, berat_terkini,
        tarikh_timbang, round(bmi, 2), kategori
    ])


# === Kemaskini Berat Peserta ===
def kemaskini_berat_peserta(nama, berat_baru):
    today = datetime.now().strftime("%Y-%m-%d")
    df = load_data_peserta()

    try:
        idx = df.index[df["Nama"] == nama].tolist()[0]
        ws_peserta.update_cell(idx + 2, df.columns.get_loc("BeratTerkini") + 1, berat_baru)
        ws_peserta.update_cell(idx + 2, df.columns.get_loc("TarikhTimbang") + 1, today)
        ws_rekod.append_row([nama, berat_baru, today])
        return True
    except:
        st.error(f"Nama {nama} tidak dijumpai dalam senarai peserta.")
        return False


# === Sejarah Berat Individu ===
def sejarah_berat(nama):
    rekod = load_rekod_berat()

    if rekod.empty or "Tarikh" not in rekod.columns:
        return pd.DataFrame()

    rekod["Tarikh"] = pd.to_datetime(rekod["Tarikh"], errors="coerce")
    rekod = rekod.dropna(subset=["Tarikh"])

    return rekod[rekod["Nama"] == nama].sort_values("Tarikh")


# === Padam Peserta ===
def padam_peserta_dari_sheet(nama):
    data = ws_peserta.get_all_records()

    for idx, row in enumerate(data):
        if row["Nama"] == nama:
            ws_peserta.delete_row(idx + 2)
            break


# === Berat Terkini Semua Peserta ===
def get_berat_terkini():
    df_rekod = load_rekod_berat()

    if df_rekod.empty:
        return pd.DataFrame(columns=["Nama", "Berat", "Tarikh"])

    df_rekod["Tarikh"] = pd.to_datetime(df_rekod["Tarikh"], errors="coerce")
    df_rekod = df_rekod.dropna(subset=["Tarikh"])

    df_latest = (
        df_rekod.sort_values('Tarikh', ascending=False)
        .drop_duplicates(subset=['Nama'], keep='first')
        .reset_index(drop=True)
    )

    return df_latest[["Nama", "Berat", "Tarikh"]]
