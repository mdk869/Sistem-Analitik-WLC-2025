import gspread
from google.oauth2.service_account import Credentials
import streamlit as st

# ✅ Authentication
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credentials = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"], scopes=scopes
)

client = gspread.authorize(credentials)

# ✅ Spreadsheet
SPREADSHEET_PESERTA = client.open("data_peserta")
SPREADSHEET_RANKING = client.open("ranking_peserta")
SPREADSHEET_LOG = client.open("log_dev")

# ✅ Drive
DRIVE_FOLDER_ID = st.secrets["drive_folder_id"]
