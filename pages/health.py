# pages/00_Connection_Checker.py

import streamlit as st
from app.helper_connection import (
    SPREADSHEET_PESERTA, SPREADSHEET_LOG, SPREADSHEET_RANKING,
    get_worksheet, list_files_in_folder
)

st.set_page_config(page_title="Connection Checker", page_icon="🔗", layout="wide")

st.title("🔗 Connection Checker | WLC 2025")

st.markdown("Semak status sambungan ke Google Sheets & Google Drive")

st.divider()

# ================================
# ✅ Check Google Sheets
# ================================
st.subheader("📄 Google Sheets")

try:
    ws_peserta = get_worksheet(SPREADSHEET_PESERTA, "data")
    peserta = ws_peserta.get_all_records()
    st.success(f"✅ Data Peserta: {len(peserta)} rekod dijumpai")
except Exception as e:
    st.error(f"❌ Data Peserta GAGAL: {e}")

try:
    ws_log = get_worksheet(SPREADSHEET_LOG, "log")
    log = ws_log.get_all_records()
    st.success(f"✅ Log Dev: {len(log)} rekod")
except Exception as e:
    st.error(f"❌ Log Dev GAGAL: {e}")

try:
    ws_ranking = get_worksheet(SPREADSHEET_RANKING, "rekod")
    rekod = ws_ranking.get_all_records()
    st.success(f"✅ Rekod Ranking: {len(rekod)} rekod")
except Exception as e:
    st.error(f"❌ Rekod Ranking GAGAL: {e}")

# ================================
# ✅ Check Google Drive
# ================================
st.divider()
st.subheader("🗂️ Google Drive")

try:
    files = list_files_in_folder()
    st.success(f"✅ Google Drive OK: {len(files)} file dalam folder.")
    for file in files:
        st.write(f"📄 {file['name']} (ID: {file['id']})")
except Exception as e:
    st.error(f"❌ Google Drive GAGAL: {e}")

st.divider()

st.info("🔄 Jika ada masalah, sila semak kembali konfigurasi `st.secrets`.")
