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

# ✅ Authorize Google Sheet
gc = gspread.authorize(credentials)

# ✅ Google Drive Service
drive_service = build('drive', 'v3', credentials=credentials)

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

# ✅ Google Sheet Connection (auto bind)
SPREADSHEET_PESERTA = gc.open_by_key(st.secrets["gsheet"]["data_peserta_id"])
SPREADSHEET_LOG = gc.open_by_key(st.secrets["gsheet"]["log_wlc_dev_id"])
SPREADSHEET_RANKING = gc.open_by_key(st.secrets["gsheet"]["rekod_ranking"])

# ✅ Drive Folder ID
DRIVE_FOLDER_ID = st.secrets["drive"]["folder_id"]

# ✅ Fungsi tambahan jika perlu (optional)
def get_spreadsheet_by_id(sheet_id):
    return gc.open_by_key(sheet_id)

def get_spreadsheet_by_name(sheet_name):
    return gc.open(sheet_name)
