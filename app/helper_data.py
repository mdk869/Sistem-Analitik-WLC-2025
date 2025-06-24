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

def load_rekod_data_from_gsheet(st_secrets: dict, spreadsheet_name: str = "data_peserta") -> pd.DataFrame:
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(st_secrets["gcp_service_account"], scopes=scope)
    client = gspread.authorize(creds)
    sh = client.open(spreadsheet_name)
    worksheet = sh.worksheet("rekod_berat")
    
    df_rekod = pd.DataFrame(worksheet.get_all_records())
    df_rekod.columns = df_rekod.columns.str.strip()

    if df_rekod.empty:
        return pd.DataFrame()

    # Tukar jenis tarikh
    if "Timestamp" in df_rekod.columns:
        df_rekod["Timestamp"] = pd.to_datetime(df_rekod["Timestamp"], errors="coerce")
    if "Tarikh Rekod" in df_rekod.columns:
        df_rekod["Tarikh Rekod"] = pd.to_datetime(df_rekod["Tarikh Rekod"], errors="coerce").dt.date
    else:
        raise KeyError("Kolum 'Tarikh Rekod' tidak dijumpai dalam rekod timbang.")

    # Tambah kolum 'Sesi' jika tiada
    if "Sesi" not in df_rekod.columns:
        def label_sesi(tarikh):
            if pd.isna(tarikh):
                return "Tidak Diketahui"
            bulan = pd.to_datetime(tarikh).month
            if bulan == 6:
                return "Jun"
            elif bulan == 7:
                return "Julai"
            elif bulan == 8:
                return "Ogos"
            else:
                return "Luar Program"
        df_rekod["Sesi"] = df_rekod["Tarikh Rekod"].apply(label_sesi)

    return df_rekod


# === Fungsi: Tambah Peserta
def tambah_peserta_google_sheet(nama, nostaf, umur, jantina, jabatan,
                                 tinggi, berat_awal, berat_terkini,
                                 tarikh_timbang, bmi, kategori):
    tarikh_daftar = datetime.now(pytz.timezone("Asia/Kuala_Lumpur")).strftime("%Y-%m-%d %H:%M:%S")
    ws_peserta.append_row([
        nama, nostaf, umur, jantina, jabatan, tinggi,
        berat_awal, tarikh_daftar, berat_terkini,
        tarikh_timbang, round(bmi, 2), kategori
    ])

# === Fungsi: Kemaskini Berat
def kemaskini_berat_peserta(nama, berat_baru):
    today = datetime.now().strftime("%Y-%m-%d")
    df = pd.DataFrame(ws_peserta.get_all_records())
    for idx, row in df.iterrows():
        if row["Nama"] == nama:
            ws_peserta.update_cell(idx + 2, df.columns.get_loc("BeratTerkini") + 1, berat_baru)
            ws_peserta.update_cell(idx + 2, df.columns.get_loc("TarikhTimbang") + 1, today)
            break
    ws_rekod.append_row([nama, berat_baru, today])

# === Fungsi: Sejarah Berat
def sejarah_berat(nama):
    rekod = pd.DataFrame(ws_rekod.get_all_records())
    rekod.columns = [str(col).strip() for col in rekod.columns]
    if rekod.empty or "Tarikh" not in rekod.columns:
        return pd.DataFrame()
    rekod["Tarikh"] = pd.to_datetime(rekod["Tarikh"], format="mixed", errors="coerce")
    rekod = rekod.dropna(subset=["Tarikh"])
    return rekod[rekod["Nama"] == nama].sort_values("Tarikh")

# === Fungsi: Padam Peserta
def padam_peserta_dari_sheet(nama):
    data = ws_peserta.get_all_records()
    for idx, row in enumerate(data):
        if row["Nama"] == nama:
            ws_peserta.delete_rows(idx + 2)
            break
