import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io



# =====================================
# ✅ Setup Google Drive Connection
# =====================================
scope = ["https://www.googleapis.com/auth/drive"]

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

# ✅ Connect ke Google Drive
DRIVE = build('drive', 'v3', credentials=credentials)

# ✅ Folder Default Drive (ambil dari secrets)
DRIVE_FOLDER_ID = st.secrets["drive"]["folder_id"]


# =====================================
# ✅ Fungsi Upload ke Google Drive
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
# ✅ Fungsi List File Dalam Folder Drive
# =====================================
def list_files_in_folder(folder_id=DRIVE_FOLDER_ID):
    try:
        query = f"'{folder_id}' in parents and trashed = false"
        results = DRIVE.files().list(q=query, fields="files(id, name)").execute()
        items = results.get('files', [])
        return items

    except Exception as e:
        st.error(f"Gagal senarai file dari Drive: {e}")
        log_error(f"list_files_in_folder error - {e}")
        return []
