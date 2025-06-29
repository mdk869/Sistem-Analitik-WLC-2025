<<<<<<< HEAD
<<<<<<< HEAD
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
=======
# app/helper_drive.py

import streamlit as st
import os
from app.helper_connection import drive_service, DRIVE_FOLDER_ID
from app.helper_log import log_dev, log_error
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io


# =====================================================
# ✅ Upload File ke Google Drive
# =====================================================
def upload_to_drive(file_path, file_name):
    try:
        file_metadata = {
            "name": file_name,
            "parents": [DRIVE_FOLDER_ID]
        }
        media = MediaFileUpload(file_path, resumable=True)
        file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id"
        ).execute()
        log_dev("Backup", f"Upload {file_name} ke Drive.")
        return file.get("id")
    except Exception as e:
        st.error(f"❌ Gagal upload ke Drive: {e}")
        log_error(f"Upload ke Drive gagal: {e}")
        return None
>>>>>>> parent of c68d2f3 (update log)


def list_files_in_folder():
<<<<<<< HEAD
    query = f"'{DRIVE_FOLDER_ID}' in parents and trashed = false"
    results = drive_service.files().list(q=query).execute()
    return results.get('files', [])
=======
import streamlit as st
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload, MediaIoBaseUpload
from app.helper_log import log_error, log_warning

=======
    try:
        query = f"'{DRIVE_FOLDER_ID}' in parents and trashed = false"
        results = drive_service.files().list(
            q=query,
            fields="files(id, name, mimeType, modifiedTime)"
        ).execute()
        return results.get("files", [])
    except Exception as e:
        st.error(f"❌ Gagal list file dari Drive: {e}")
        log_error(f"List file gagal: {e}")
        return []
>>>>>>> parent of c68d2f3 (update log)

# =====================================
# ✅ Setup Google Drive Connection
# =====================================
scope = ["https://www.googleapis.com/auth/drive"]

<<<<<<< HEAD
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

DRIVE = build('drive', 'v3', credentials=credentials)
DRIVE_FOLDER_ID = st.secrets["drive"]["folder_id"]


# =====================================
# ✅ Fungsi Upload Dari File Path
# =====================================
def upload_to_drive(file_path, file_name, folder_id=DRIVE_FOLDER_ID):
    try:
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

    except Exception as e:
        st.error(f"Gagal upload ke Drive: {e}")
        log_error(f"upload_to_drive error - {e}")
        return None


# =====================================
# ✅ Fungsi Upload Dari Memory Bytes
# =====================================
def upload_bytes_to_drive(file_bytes, file_name, folder_id=DRIVE_FOLDER_ID):
    try:
        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }
        media = MediaIoBaseUpload(
            file_bytes,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            resumable=True
        )
        file = DRIVE.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        return file.get('id')

    except Exception as e:
        st.error(f"Gagal upload ke Drive: {e}")
        log_error(f"upload_bytes_to_drive error - {e}")
        return None


# =====================================
# ✅ Fungsi Download dari Google Drive
# =====================================
def download_from_drive(file_id, destination_path):
    try:
        request = DRIVE.files().get_media(fileId=file_id)
        fh = io.FileIO(destination_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False

        while not done:
            status, done = downloader.next_chunk()

        fh.close()
        return True

    except Exception as e:
        st.error(f"Gagal download dari Drive: {e}")
        log_error(f"download_from_drive error - {e}")
        return False


# =====================================
# ✅ Fungsi Download sebagai BytesIO
# =====================================
def download_file_as_bytes(file_id):
    try:
        request = DRIVE.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False

        while not done:
            status, done = downloader.next_chunk()

        fh.seek(0)
        return fh

    except Exception as e:
        st.error(f"Gagal download file: {e}")
        log_error(f"download_file_as_bytes error - {e}")
        return None


# =====================================
# ✅ List Files dalam Folder Drive
# =====================================
def list_files_in_folder(folder_id=DRIVE_FOLDER_ID):
    try:
        query = f"'{folder_id}' in parents and trashed = false"
        results = DRIVE.files().list(q=query, fields="files(id, name, createdTime, size)").execute()
        items = results.get('files', [])
        return items

    except Exception as e:
        st.error(f"Gagal senarai file dari Drive: {e}")
        log_error(f"list_files_in_folder error - {e}")
        return []


# =====================================
# ✅ Delete File Dari Drive
# =====================================
def delete_file_from_drive(file_id):
    try:
        DRIVE.files().delete(fileId=file_id).execute()
        return True

    except Exception as e:
        st.error(f"Gagal padam file dari Drive: {e}")
        log_error(f"delete_file_from_drive error - {e}")
        return False


# =====================================
# ✅ Get File Metadata
# =====================================
def get_file_metadata(file_id):
    try:
        file = DRIVE.files().get(fileId=file_id, fields='id, name, mimeType, createdTime, size').execute()
        return file

    except Exception as e:
        st.error(f"Gagal dapatkan metadata file: {e}")
        log_error(f"get_file_metadata error - {e}")
        return None


# =====================================
# ✅ Export Fungsi
# =====================================
__all__ = [
    "upload_to_drive",
    "upload_bytes_to_drive",
    "download_from_drive",
    "download_file_as_bytes",
    "list_files_in_folder",
    "delete_file_from_drive",
    "get_file_metadata"
]
>>>>>>> parent of 71cba5f (restructure modular)
=======
# =====================================================
# ✅ Download File Dari Google Drive
# =====================================================
def download_from_drive(file_id, save_as):
    try:
        request = drive_service.files().get_media(fileId=file_id)
        fh = open(save_as, "wb")
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while done is False:
            status, done = downloader.next_chunk()

        fh.close()
        log_dev("Restore", f"Download {save_as} dari Drive.")
        return True
    except Exception as e:
        st.error(f"❌ Gagal download dari Drive: {e}")
        log_error(f"Download gagal: {e}")
        return False
>>>>>>> parent of c68d2f3 (update log)
