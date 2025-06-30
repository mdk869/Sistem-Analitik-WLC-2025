import streamlit as st
import gspread
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


# =========================================
# ✅ GCP Service Account Credentials
# =========================================
def get_gcp_credentials():
    return service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ],
    )


# =========================================
# ✅ Gspread Client (Google Sheets)
# =========================================
@st.cache_resource
def get_gspread_client():
    creds = get_gcp_credentials()
    return gspread.authorize(creds)


# =========================================
# ✅ Google Sheets Connection
# =========================================
@st.cache_resource
def get_sheet(sheet_id):
    gc = get_gspread_client()
    return gc.open_by_key(sheet_id)


# =========================================
# ✅ Google Drive Service
# =========================================
@st.cache_resource
def get_drive_service():
    creds = get_gcp_credentials()
    return build("drive", "v3", credentials=creds)


# =========================================
# ✅ Load Spreadsheet ID dari st.secrets
# =========================================
SPREADSHEET_PESERTA = st.secrets["gsheet"]["data_peserta_id"]
SPREADSHEET_LOG = st.secrets["gsheet"]["log_wlc_dev_id"]
SPREADSHEET_RANKING = st.secrets["gsheet"]["rekod_ranking"]

DRIVE_FOLDER_ID = st.secrets["drive"]["folder_id"]
