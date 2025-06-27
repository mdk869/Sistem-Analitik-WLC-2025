# app/helper_connection.py

import gspread
from google.oauth2.service_account import Credentials
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import streamlit as st

# ============================================
# ✅ Semak Sambungan
# ============================================
def connection_checker():
    status = {}

    # === Check Google Sheet Connection ===
    try:
        gc = gspread.authorize(Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive",
            ],
        ))

        sheets = {
            "Data Peserta": st.secrets["gsheet"]["data_peserta_id"],
            "Log Dev": st.secrets["gsheet"]["log_wlc_dev_id"],
            "Rekod Ranking": st.secrets["gsheet"]["rekod_ranking"],
        }

        for name, sheet_id in sheets.items():
            try:
                gc.open_by_key(sheet_id)
                status[name] = "✅ OK"
            except Exception as e:
                status[name] = f"❌ ERROR: {e}"

    except Exception as e:
        for name in ["Data Peserta", "Log Dev", "Rekod Ranking"]:
            status[name] = f"❌ ERROR Auth: {e}"

    # === Check Google Drive Connection ===
    try:
        gauth = GoogleAuth()
        gauth.credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=["https://www.googleapis.com/auth/drive"],
        )
        drive = GoogleDrive(gauth)

        folder_id = st.secrets["drive"]["folder_id"]
        file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()

        status["Google Drive"] = "✅ OK"
    except Exception as e:
        status["Google Drive"] = f"❌ ERROR: {e}"

    return status

# ============================================
# ✅ Sambungan Google Sheet
# ============================================
def connect_gsheet(spreadsheet_id):
    """Sambungkan ke Google Spreadsheet berdasarkan ID."""
    try:
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"], scopes=scope
        )
        gc = gspread.authorize(credentials)
        sheet = gc.open_by_key(spreadsheet_id)
        return sheet
    except Exception as e:
        st.error(f"❌ Gagal sambung ke Google Sheet: {e}")
        st.stop()


# ============================================
# ✅ Sambungan Google Drive
# ============================================
def connect_drive():
    """Sambungkan ke Google Drive."""
    try:
        gauth = GoogleAuth()
        gauth.credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=["https://www.googleapis.com/auth/drive"]
        )
        drive = GoogleDrive(gauth)
        return drive
    except Exception as e:
        st.error(f"❌ Gagal sambung ke Google Drive: {e}")
        st.stop()

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


# ============================================
# ✅ Shortcut Connection (Auto Connect)
# ============================================
# 📄 Spreadsheet
SHEET_PESERTA = connect_gsheet(get_secret_id("gsheet", "data_peserta_id"))
SHEET_LOG = connect_gsheet(get_secret_id("gsheet", "log_wlc_dev_id"))
SHEET_RANKING = connect_gsheet(get_secret_id("gsheet", "rekod_ranking"))

# 🗂️ Google Drive
DRIVE = connect_drive()


# ============================================
# ✅ Export Fungsi
# ============================================
__all__ = [
    "connect_gsheet",
    "connect_drive",
    "get_secret_id",
    "SHEET_PESERTA",
    "SHEET_LOG",
    "SHEET_RANKING",
    "DRIVE"
]
