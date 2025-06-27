# pages/connection_test.py

import streamlit as st
from app.helper_connection import (
    SPREADSHEET_PESERTA,
    SPREADSHEET_LOG,
    SPREADSHEET_RANKING,
    get_worksheet,
    list_files_in_folder
)

st.title("🔗 Test Connection Google Sheets & Drive")

try:
    ws = get_worksheet(SPREADSHEET_PESERTA, "data")
    data = ws.get_all_records()
    st.success("✅ Berjaya connect ke Google Sheet: Data Peserta")
    st.write(data)
except Exception as e:
    st.error(f"❌ Gagal connect ke Data Peserta: {e}")

try:
    files = list_files_in_folder()
    st.success("✅ Berjaya connect ke Google Drive")
    st.write(files)
except Exception as e:
    st.error(f"❌ Gagal connect ke Google Drive: {e}")
