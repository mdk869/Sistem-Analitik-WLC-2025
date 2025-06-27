import streamlit as st
import gspread
from google.oauth2 import service_account
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
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
        scope = ["https://www.googleapis.com/auth/drive"]

        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            {
                "type": st.secrets["gcp_service_account"]["type"],
                "project_id": st.secrets["gcp_service_account"]["project_id"],
                "private_key_id": st.secrets["gcp_service_account"]["private_key_id"],
                "private_key": st.secrets["gcp_service_account"]["private_key"],
                "client_email": st.secrets["gcp_service_account"]["client_email"],
                "client_id": st.secrets["gcp_service_account"]["client_id"],
                "auth_uri": st.secrets["gcp_service_account"]["auth_uri"],
                "token_uri": st.secrets["gcp_service_account"]["token_uri"],
                "auth_provider_x509_cert_url": st.secrets["gcp_service_account"]["auth_provider_x509_cert_url"],
                "client_x509_cert_url": st.secrets["gcp_service_account"]["client_x509_cert_url"],
                "universe_domain": st.secrets["gcp_service_account"]["universe_domain"],
            },
            scope,
        )

        gauth = GoogleAuth()
        gauth.credentials = credentials
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

def check_or_create_worksheet(spreadsheet, worksheet_name, header: list = None):
    """
    Fungsi untuk semak sama ada worksheet wujud dalam spreadsheet.
    Jika tidak wujud, ia akan cipta worksheet baru dengan nama dan header yang diberikan.

    Args:
        spreadsheet: objek spreadsheet (gspread).
        worksheet_name (str): Nama worksheet yang hendak diperiksa/dicreate.
        header (list, optional): Senarai header untuk row pertama. Default None.

    Returns:
        worksheet object (gspread.models.Worksheet)
    """
    try:
        ws = spreadsheet.worksheet(worksheet_name)
    except Exception:
        ws = spreadsheet.add_worksheet(title=worksheet_name, rows="1000", cols="20")
        if header:
            ws.append_row(header)
    return ws

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
