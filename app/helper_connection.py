import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from app.helper_utils import check_or_create_worksheet


# ============================================================
# ✅ Google Sheets Connection
# ============================================================
def connect_gspread():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scopes
    )
    client = gspread.authorize(creds)
    return client


# ============================================================
# ✅ Google Drive Connection
# ============================================================
def connect_drive():
    gauth = GoogleAuth()
    gauth.settings['client_config'] = {
        "client_id": st.secrets["gcp_service_account"]["client_id"],
        "client_secret": "dummy",  # Not used, but required by pydrive2
        "auth_uri": st.secrets["gcp_service_account"]["auth_uri"],
        "token_uri": st.secrets["gcp_service_account"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["gcp_service_account"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["gcp_service_account"]["client_x509_cert_url"]
    }
    gauth.credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/drive.file"
        ]
    )
    drive = GoogleDrive(gauth)
    return drive


# ============================================================
# ✅ Spreadsheet Connections
# ============================================================
gc = connect_gspread()

SHEET_PESERTA = gc.open_by_key(st.secrets["gsheet"]["data_peserta_id"])
SHEET_LOG = gc.open_by_key(st.secrets["gsheet"]["log_wlc_dev_id"])
SHEET_REKOD_RANKING = gc.open_by_key(st.secrets["gsheet"]["rekod_ranking"])

# ✅ Google Drive Folder
FOLDER_DRIVE_ID = st.secrets["drive"]["folder_id"]
DRIVE = connect_drive()
