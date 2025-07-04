from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from app.helper_connection import get_drive_service
import io
import streamlit as st


# ======= Setup Connection =======
SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_INFO = st.secrets["gcp_service_account"]

credentials = Credentials.from_service_account_info(
    SERVICE_ACCOUNT_INFO, scopes=SCOPES
)

drive_service = build("drive", "v3", credentials=credentials)

# ======= Folder ID =======
DRIVE_FOLDER_ID = st.secrets["drive"]["folder_id"]

# ======= Upload Function =======

def upload_to_drive(file_path, file_name, folder_id=None):
    service = get_drive_service()
    file_metadata = {'name': file_name}
    if folder_id:
        file_metadata['parents'] = [folder_id]

    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')

def list_files_in_folder():
    """Senarai fail dalam folder Google Drive."""
    try:
        results = drive_service.files().list(
            q=f"'{DRIVE_FOLDER_ID}' in parents and trashed=false",
            fields="files(id, name, modifiedTime, mimeType)"
        ).execute()
        return results.get("files", [])
    except Exception as e:
        print(f"❌ List Files Error: {e}")
        return []


def download_file_from_drive(file_id, destination_path):
    """Download fail dari Google Drive."""
    try:
        request = drive_service.files().get_media(fileId=file_id)
        fh = io.FileIO(destination_path, "wb")
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
        return True
    except Exception as e:
        print(f"❌ Download Error: {e}")
        return False
