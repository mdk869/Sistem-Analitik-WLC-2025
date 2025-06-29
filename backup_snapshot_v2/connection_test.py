import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from app.helper_connection import client, drive_service
import traceback

# ==========================
# ✅ Load Secrets
# ==========================
SPREADSHEET_LIST = {
    "Data Peserta": st.secrets["gsheet"]["data_peserta_id"],
    "Log WLC Dev": st.secrets["gsheet"]["log_wlc_dev_id"],
    "Rekod Ranking": st.secrets["gsheet"]["rekod_ranking"]
}

DRIVE_FOLDER_ID = st.secrets["drive"]["folder_id"]

# ==========================
# ✅ UI Setup
# ==========================
st.set_page_config(page_title="🔗 Connection Test | WLC 2025", layout="wide")
st.title("🔗 Connection Health Check - WLC 2025")
st.caption("Skrip ini digunakan untuk menguji sambungan ke Google Sheets dan Google Drive.")

st.divider()

# ==========================
# ✅ Check Google Sheets
# ==========================
st.subheader("📄 Google Sheets Connection")

for name, sheet_id in SPREADSHEET_LIST.items():
    try:
        sheet = client.open_by_key(sheet_id)
        ws_list = sheet.worksheets()
        ws_names = [ws.title for ws in ws_list]
        st.success(f"✅ {name}: Berjaya dibuka — Worksheet: {', '.join(ws_names)}")
    except Exception as e:
        st.error(f"❌ {name}: Gagal dibuka — {e}")

st.divider()

# ==========================
# ✅ Check Google Drive
# ==========================
st.subheader("🗂️ Google Drive Connection")

try:
    results = drive_service.files().list(
        q=f"'{DRIVE_FOLDER_ID}' in parents and trashed = false",
        fields="files(id, name, mimeType)"
    ).execute()

    items = results.get('files', [])

    if not items:
        st.warning("⚠️ Tiada fail dalam folder Google Drive.")
    else:
        st.success(f"✅ {len(items)} fail dijumpai dalam folder Google Drive.")
        for item in items:
            st.write(f"📄 {item['name']} — {item['id']}")

except HttpError as error:
    st.error(f"❌ Google Drive Error: {error}")
except Exception as e:
    st.error(f"❌ Google Drive Connection Error: {e}")

st.divider()

# ==========================
# ✅ Summary
# ==========================
st.info("💡 Pastikan semua sambungan bertanda ✅ sebelum meneruskan operasi sistem.")
