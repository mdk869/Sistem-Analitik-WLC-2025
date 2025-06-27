import streamlit as st
import gspread
from google.oauth2 import service_account
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

# ---- Fungsi Get Secret ----
def get_secret_id(id_name):
    return st.secrets["gsheet"][id_name]

# ---- Sambungan Google Sheets ----
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.file"
]

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope,
)

gc = gspread.authorize(credentials)

# ---- Connect Google Sheet ----
SHEET_PESERTA = gc.open_by_key(get_secret_id("data_peserta"))
SHEET_LOG = gc.open_by_key(get_secret_id("log_wlc_dev"))
SHEET_REKOD_RANKING = gc.open_by_key(get_secret_id("rekod_ranking"))

# ---- Connect Google Drive ----
gauth = GoogleAuth()
gauth.credentials = credentials
drive = GoogleDrive(gauth)

DRIVE = drive
