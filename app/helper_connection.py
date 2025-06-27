import streamlit as st
import gspread
from google.oauth2 import service_account
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import json
import tempfile


# ===========================
# ✅ Google Sheets Connection
# ===========================
# Setup credential dari st.secrets
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

CREDENTIALS = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"], scopes=SCOPE
)

gc = gspread.authorize(CREDENTIALS)

# ===========================
# ✅ Google Drive Connection
# ===========================
def connect_drive():
    try:
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp:
            json.dump(st.secrets["gcp_service_account"], temp)
            temp.flush()

            gauth = GoogleAuth()
            gauth.LoadServiceConfigFile(temp.name)
            drive = GoogleDrive(gauth)

        return drive

    except Exception as e:
        st.error(f"❌ Gagal sambung ke Google Drive: {e}")
        return None


# ===========================
# ✅ Spreadsheet ID
# ===========================
SHEET_PESERTA = st.secrets["gsheet"]["data_peserta_id"]
SHEET_LOG = st.secrets["gsheet"]["log_wlc_dev_id"]
SHEET_RANKING = st.secrets["gsheet"]["rekod_ranking"]

# ===========================
# ✅ Google Drive Folder
# ===========================
DRIVE_FOLDER_ID = st.secrets["drive"]["folder_id"]

from app.helper_connection import gc, connect_drive, SHEET_PESERTA, SHEET_LOG, SHEET_RANKING, DRIVE_FOLDER_ID


def connection_checker():
    status = {}

    # === Check Google Sheets ===
    try:
        sheets = {
            "Data Peserta": SHEET_PESERTA,
            "Log Dev": SHEET_LOG,
            "Rekod Ranking": SHEET_RANKING,
        }

        for name, sheet_id in sheets.items():
            try:
                gc.open_by_key(sheet_id)
                status[name] = "✅ OK"
            except Exception as e:
                status[name] = f"❌ ERROR: {e}"

    except Exception as e:
        for name in sheets.keys():
            status[name] = f"❌ ERROR Auth: {e}"

    # === Check Google Drive ===
    try:
        drive = connect_drive()
        folder_id = DRIVE_FOLDER_ID
        file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()

        status["Google Drive"] = "✅ OK"
    except Exception as e:
        status["Google Drive"] = f"❌ ERROR: {e}"

    return status
