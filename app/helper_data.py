# app/helper_data.py
import os
import pandas as pd
import streamlit as st
import gspread
from google.oauth2 import service_account

# === Tentukan sama ada dalam mod Cloud atau Local ===
try:
    _ = st.secrets["gcp_service_account"]
    IS_CLOUD = True
except st.errors.StreamlitSecretNotFoundError:
    IS_CLOUD = False

# === Laluan Fail Local ===
DIR_SEMASA = os.path.dirname(os.path.abspath(__file__))
DIR_ROOT = os.path.dirname(DIR_SEMASA)  # folder projek utama
FILE_EXCEL = os.path.join(DIR_ROOT, "peserta.xlsx")
FILE_REKOD = os.path.join(DIR_ROOT, "rekod_ranking_semasa.xlsx")
FILE_REKOD_BERAT = os.path.join(DIR_ROOT, "rekod_berat.xlsx")

def load_data_cloud_or_local():
    """Muat data peserta dari Google Sheets (Cloud) atau Excel (Local)."""
    if IS_CLOUD:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"], scopes=scope
        )
        client = gspread.authorize(credentials)
        sheet = client.open("peserta").worksheet("Sheet1")
        data = sheet.get_all_records()
        df = pd.DataFrame(data)
    else:
        if not os.path.exists(FILE_EXCEL):
            st.error("❌ Fail peserta.xlsx tidak dijumpai.")
            st.stop()
        df = pd.read_excel(FILE_EXCEL)
    
    # Auto tambah kolum berkaitan jika tiada
    if "BeratAwal" in df.columns and "BeratTerkini" in df.columns:
        df["PenurunanKg"] = df["BeratAwal"] - df["BeratTerkini"]
        df["% Penurunan"] = (df["PenurunanKg"] / df["BeratAwal"] * 100).round(2)
    return df

def save_ranking_to_excel(df_ranking):
    """Simpan ranking ke fail Excel dan upload ke Google Drive jika cloud."""
    df_ranking.to_excel(FILE_REKOD, index=False)

    if IS_CLOUD:
        from pydrive2.auth import GoogleAuth
        from pydrive2.drive import GoogleDrive

        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.file"]
        )
        gauth = GoogleAuth()
        gauth.credentials = credentials
        drive = GoogleDrive(gauth)

        file_drive = drive.CreateFile({
            'title': 'rekod_ranking_semasa.xlsx',
            'parents': [{'id': '1XR6OlFeiDLet9niwsUdmvKW4GGKNOkgT'}]
        })
        file_drive.SetContentFile(FILE_REKOD)
        file_drive.Upload()

def upload_file_to_drive(file_path):
    """Backup sebarang fail ke Google Drive."""
    if not IS_CLOUD:
        return
    from pydrive2.auth import GoogleAuth
    from pydrive2.drive import GoogleDrive
    from google.oauth2 import service_account

    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.file"]
    )
    gauth = GoogleAuth()
    gauth.credentials = credentials
    drive = GoogleDrive(gauth)

    filename = os.path.basename(file_path)
    file_drive = drive.CreateFile({
        'title': filename,
        'parents': [{'id': '1XR6OlFeiDLet9niwsUdmvKW4GGKNOkgT'}]
    })
    file_drive.SetContentFile(file_path)
    file_drive.Upload()
    

# === Untuk akses laluan dari fail lain ===
__all__ = [
    "load_data_cloud_or_local",
    "save_ranking_to_excel",
    "upload_fil_"
]