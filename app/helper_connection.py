import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import streamlit as st

# ===== ✅ Sambungan ke Google API =====
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

client = gspread.authorize(creds)

# ===== ✅ Google Drive Service =====
drive_service = build("drive", "v3", credentials=creds)

# ===== ✅ ID Google Drive Folder =====
DRIVE_FOLDER_ID = st.secrets["drive_folder_id"]

# ===== ✅ Spreadsheet Utama =====
SPREADSHEET_PESERTA = client.open("data_peserta")
SPREADSHEET_RANKING = client.open("data_ranking")
SPREADSHEET_LOG = client.open("log_dev")
