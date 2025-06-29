import io
import streamlit as st
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.oauth2.service_account import Credentials

# ✅ Authentication
credentials = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/drive"]
)

drive_service = build('drive', 'v3', credentials=credentials)

# ✅ Folder ID
DRIVE_FOLDER_ID = st.secrets["drive_folder_id"]


def upload_to_drive(local_file_path, remote_file_name):
    file_metadata = {
        'name': remote_file_name,
        'parents': [DRIVE_FOLDER_ID]
    }
    media = MediaFileUpload(local_file_path)
    file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    return file.get('id')


def list_files_in_folder():
    query = f"'{DRIVE_FOLDER_ID}' in parents and trashed = false"
    results = drive_service.files().list(q=query).execute()
    return results.get('files', [])
