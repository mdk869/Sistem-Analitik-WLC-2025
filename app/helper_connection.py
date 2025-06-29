import streamlit as st
import gspread
from google.oauth2 import service_account
from googleapiclient.discovery import build

# ✅ Setup credentials
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

# ✅ Authorize gspread
gc = gspread.authorize(credentials)

# ✅ Google Drive Service
def create_drive_service():
    return build('drive', 'v3', credentials=credentials)

drive_service = create_drive_service()

# ✅ Fungsi akses spreadsheet by ID
def get_spreadsheet_by_id(sheet_id):
    return gc.open_by_key(sheet_id)

# ✅ Fungsi akses spreadsheet by name
def get_spreadsheet_by_name(sheet_name):
    return gc.open(sheet_name)

# ✅ Secrets ID
def get_secret_id(key):
    return st.secrets["gsheet"].get(key, None)
