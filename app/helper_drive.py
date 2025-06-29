import io
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from app.helper_connection import drive_service, DRIVE_FOLDER_ID


def upload_to_drive(file_path, file_name):
    """Upload fail ke Google Drive."""
    try:
        file_metadata = {
            "name": file_name,
            "parents": [DRIVE_FOLDER_ID]
        }
        media = MediaFileUpload(file_path, resumable=True)
        file = drive_service.files().create(
            body=file_metadata, media_body=media, fields="id"
        ).execute()
        return file.get("id")
    except Exception as e:
        print(f"❌ Upload Error: {e}")
        return None


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
