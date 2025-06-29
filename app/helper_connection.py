# app/helper_connection.py

import streamlit as st
import gspread
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from app.helper_log import log_error
import io

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

# 🔑 Get ID dari secrets
def get_secret_id(key):
    return st.secrets["gsheet"].get(key, None)

# ✅ Connect ke Spreadsheet
SPREADSHEET_PESERTA = gc.open_by_key(get_secret_id("data_peserta_id"))
SPREADSHEET_LOG = gc.open_by_key(get_secret_id("log_wlc_dev_id"))
SPREADSHEET_RANKING = gc.open_by_key(get_secret_id("rekod_ranking"))

# ✅ Fungsi dapat spreadsheet
def get_spreadsheet(spreadsheet_name):
    """
    Dapatkan objek spreadsheet berdasarkan nama.
    Digunakan sebagai asas untuk akses worksheet dalam spreadsheet tersebut.

    Args:
        spreadsheet_name (str): Nama Google Spreadsheet (bukan ID).

    Returns:
        gspread.models.Spreadsheet: Objek Spreadsheet.
    """
    try:
        sh = get_worksheet.open(spreadsheet_name)
        return sh
    except Exception as e:
        st.error(f"❌ Gagal buka spreadsheet '{spreadsheet_name}': {e}")
        log_error(f"get_spreadsheet error - {spreadsheet_name} - {e}")
        return None


# ✅ Fungsi dapat worksheet
def get_worksheet(spreadsheet_name, worksheet_name):
    sh = get_spreadsheet(spreadsheet_name)
    if sh:
        return sh.worksheet(worksheet_name)
    else:
        return None
    
    try:
        ws = spreadsheet.worksheet(worksheet_name)
    except gspread.exceptions.WorksheetNotFound:
        ws = spreadsheet.add_worksheet(title=worksheet_name, rows="1000", cols="20")
    return ws


# ==========================
# ✅ Google Drive Connection
# ==========================

def create_drive_service():
    drive_creds = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    service = build('drive', 'v3', credentials=drive_creds)
    return service


DRIVE = create_drive_service()
DRIVE_FOLDER_ID = st.secrets["drive"]["folder_id"]

# ✅ Upload file ke Drive
def upload_to_drive(file_path, file_name, folder_id=DRIVE_FOLDER_ID):
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, resumable=True)
    file = DRIVE.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    return file.get('id')

# ✅ Download file dari Drive
def download_from_drive(file_id, destination_path):
    request = DRIVE.files().get_media(fileId=file_id)
    fh = io.FileIO(destination_path, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    fh.close()

# ✅ List file dalam folder Drive
def list_files_in_folder(folder_id=DRIVE_FOLDER_ID):
    query = f"'{folder_id}' in parents and trashed = false"
    results = DRIVE.files().list(q=query, fields="files(id, name)").execute()
    items = results.get('files', [])
    return items
