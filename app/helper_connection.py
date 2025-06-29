import streamlit as st
import gspread
from google.oauth2 import service_account
from googleapiclient.discovery import build

# ========================
# ✅ Credential Setup
# ========================
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scopes
)

# ✅ GSpread client (boleh pakai sebagai gc)
gc = gspread.authorize(creds)  # ===> ✅ Ini gc

# ✅ Alias untuk konsisten (pilihan)
client = gc  # Supaya boleh pakai sama ada client atau gc

# ✅ Google Drive Service
drive_service = build("drive", "v3", credentials=creds)

# ========================
# ✅ Spreadsheet Connection
# ========================
SPREADSHEET_PESERTA = gc.open_by_key(st.secrets["gsheet"]["data_peserta_id"])
SPREADSHEET_LOG = gc.open_by_key(st.secrets["gsheet"]["log_wlc_dev_id"])
SPREADSHEET_RANKING = gc.open_by_key(st.secrets["gsheet"]["rekod_ranking"])

# ========================
# ✅ Drive Folder ID
# ========================
DRIVE_FOLDER_ID = st.secrets["drive"]["folder_id"]

# ========================
# ✅ Fungsi Dapatkan Secret ID (Optional)
# ========================
def get_secret_id(section, key):
    """Mudah panggil ID dari secrets"""
    try:
        return st.secrets[section][key]
    except Exception as e:
        st.error(f"❌ Key '{key}' dalam section [{section}] tidak dijumpai. {e}")
        return None
