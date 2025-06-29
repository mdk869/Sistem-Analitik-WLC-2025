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


# =====================================================
# ✅ List File Dalam Folder
# =====================================================
def list_files_in_folder():
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
