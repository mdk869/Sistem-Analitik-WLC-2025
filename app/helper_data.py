import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import streamlit as st
import pytz

# === Fungsi: Sambung Google Sheets ===
def sambung_gsheet():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=scope
    )
    client = gspread.authorize(credentials)
    return client

# === Fungsi: Load Data dari Google Sheet 'peserta' ===
def load_data_cloud_or_local():
    client = sambung_gsheet()
    ws = client.open("data_peserta").worksheet("peserta")
    df = pd.DataFrame(ws.get_all_records())
    return df

# === Fungsi: Load Data rekod_berat ===
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

    if "Timestamp" in df_rekod.columns:
        df_rekod["Timestamp"] = pd.to_datetime(df_rekod["Timestamp"], errors="coerce")
    if "Tarikh Rekod" in df_rekod.columns:
        df_rekod["Tarikh Rekod"] = pd.to_datetime(df_rekod["Tarikh Rekod"], errors="coerce").dt.date
    else:
        raise KeyError("Kolum 'Tarikh Rekod' tidak dijumpai dalam rekod timbang.")

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
