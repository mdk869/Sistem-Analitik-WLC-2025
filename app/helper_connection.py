# app/helper_connection.py

import gspread
from google.oauth2.service_account import Credentials
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import streamlit as st


# ============================================
# ✅ Sambungan Google Sheet
# ============================================
def connect_gsheet(spreadsheet_id):
    """Sambungkan ke Google Spreadsheet berdasarkan ID."""
    try:
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"], scopes=scope
        )
        gc = gspread.authorize(credentials)
        sheet = gc.open_by_key(spreadsheet_id)
        return sheet
    except Exception as e:
        st.error(f"❌ Gagal sambung ke Google Sheet: {e}")
        st.stop()


# ============================================
# ✅ Sambungan Google Drive
# ============================================
def connect_drive():
    """Sambungkan ke Google Drive."""
    try:
        gauth = GoogleAuth()
        gauth.credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=["https://www.googleapis.com/auth/drive"]
        )
        drive = GoogleDrive(gauth)
        return drive
    except Exception as e:
        st.error(f"❌ Gagal sambung ke Google Drive: {e}")
        st.stop()


# ============================================
# ✅ Fungsi Ringkas Dapatkan ID dari Secrets
# ============================================
def get_secret_id(section, key):
    """Periksa dan dapatkan ID dari secrets.toml."""
    try:
        return st.secrets[section][key]
    except KeyError:
        st.error(f"❌ Missing key [{section}][{key}] dalam secrets.toml!")
        st.stop()


# ============================================
# ✅ Shortcut Connection (Auto Connect)
# ============================================
# 📄 Spreadsheet
SHEET_PESERTA = connect_gsheet(get_secret_id("gsheet", "data_peserta_id"))
SHEET_LOG = connect_gsheet(get_secret_id("gsheet", "log_wlc_dev_id"))
SHEET_RANKING = connect_gsheet(get_secret_id("gsheet", "rekod_ranking"))

# 🗂️ Google Drive
DRIVE = connect_drive()


# ============================================
# ✅ Export Fungsi
# ============================================
__all__ = [
    "connect_gsheet",
    "connect_drive",
    "get_secret_id",
    "SHEET_PESERTA",
    "SHEET_LOG",
    "SHEET_RANKING",
    "DRIVE"
]
