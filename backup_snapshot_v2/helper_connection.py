import streamlit as st
import gspread
from google.oauth2 import service_account
from googleapiclient.discovery import build


# ✅ Setup credentials
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

try:
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scope
    )
except Exception as e:
    st.error(f"❌ Gagal setup credentials: {e}")
    st.stop()


# ✅ Authorize Google Sheet
gc = gspread.authorize(credentials)


# ✅ Google Drive Service
def get_drive_service():
    try:
        service = build('drive', 'v3', credentials=credentials)
        return service
    except Exception as e:
        st.error(f"❌ Gagal setup Google Drive Service: {e}")
        return None


# ✅ Fungsi dapatkan ID dari secrets
def get_secret_id(section, key):
    try:
        return st.secrets[section][key]
    except KeyError:
        st.error(f"❌ Missing key [{section}][{key}] dalam secrets.toml!")
        st.stop()


# ✅ Fungsi sambung Spreadsheet
def get_spreadsheet_by_id(sheet_id):
    try:
        return gc.open_by_key(sheet_id)
    except Exception as e:
        st.error(f"❌ Gagal sambung ke Spreadsheet ID: {sheet_id} - {e}")
        return None


# ✅ Setup Spreadsheet dan Drive Folder ID
SPREADSHEET_PESERTA = get_spreadsheet_by_id(get_secret_id("gsheet", "data_peserta_id"))
SPREADSHEET_LOG = get_spreadsheet_by_id(get_secret_id("gsheet", "log_wlc_dev_id"))
SPREADSHEET_RANKING = get_spreadsheet_by_id(get_secret_id("gsheet", "rekod_ranking"))

DRIVE_FOLDER_ID = get_secret_id("drive", "folder_id")
