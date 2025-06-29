# app/helper_drive.py

import streamlit as st
import os
from app.helper_connection import drive_service, DRIVE_FOLDER_ID
import io
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload


# =====================================================
# ✅ Upload File ke Google Drive
# =====================================================
def upload_to_drive(file_path, file_name):
    file_metadata = {'name': file_name, 'parents': [DRIVE_FOLDER_ID]}
    media = MediaFileUpload(file_path, resumable=True)
    file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    return file.get('id')


# =====================================================
# ✅ List File Dalam Folder
# =====================================================
def list_files_in_folder():
    query = f"'{DRIVE_FOLDER_ID}' in parents and trashed=false"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    return results.get('files', [])



# =====================================================
# ✅ Download File Dari Google Drive
# =====================================================
def download_from_drive(file_id, save_as):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.FileIO(save_as, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
