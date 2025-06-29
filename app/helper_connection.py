import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# ===== ✅ Authentication Google API =====
creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"])
client = gspread.authorize(creds)
drive_service = build("drive", "v3", credentials=creds)

# ===== ✅ Google Drive Folder ID =====
DRIVE_FOLDER_ID = st.secrets["drive"]["folder_id"]

# ===== ✅ Spreadsheet IDs =====
SPREADSHEET_PESERTA = client.open_by_key(st.secrets["gsheet"]["data_peserta_id"])
SPREADSHEET_LOG = client.open_by_key(st.secrets["gsheet"]["log_wlc_dev_id"])
SPREADSHEET_RANKING = client.open_by_key(st.secrets["gsheet"]["rekod_ranking"])
