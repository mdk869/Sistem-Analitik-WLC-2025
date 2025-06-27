import streamlit as st
from app.helper_connection import (
    SHEET_PESERTA,
    SHEET_LOG,
    SHEET_REKOD_RANKING,
    DRIVE,
    get_secret_id,
    list_files_in_folder
)

st.set_page_config(page_title="Test Connection", page_icon="🔗", layout="wide")

st.title("🔗 Ujian Sambungan Google Sheets & Drive")

# =============================================
# ✅ Test Google Sheets Connection
# =============================================
st.subheader("🗒️ Google Sheets")

try:
    sheet_list = SHEET_PESERTA.worksheets()
    st.success(f"✅ Data Peserta - OK ({len(sheet_list)} worksheet dijumpai)")
except Exception as e:
    st.error(f"❌ Data Peserta - Gagal\n\n{e}")

try:
    sheet_list = SHEET_LOG.worksheets()
    st.success(f"✅ Log Dev - OK ({len(sheet_list)} worksheet dijumpai)")
except Exception as e:
    st.error(f"❌ Log Dev - Gagal\n\n{e}")

try:
    sheet_list = SHEET_REKOD_RANKING.worksheets()
    st.success(f"✅ Rekod Ranking - OK ({len(sheet_list)} worksheet dijumpai)")
except Exception as e:
    st.error(f"❌ Rekod Ranking - Gagal\n\n{e}")

# =============================================
# ✅ Test Google Drive Connection
# =============================================
st.subheader("☁️ Google Drive")

try:
    files = list_files_in_folder()
    st.success(f"✅ Google Drive - OK ({len(files)} files dijumpai dalam folder)")
    for file in files:
        st.write(f"- {file['name']} (ID: {file['id']})")
except Exception as e:
    st.error(f"❌ Google Drive - Gagal\n\n{e}")

# =============================================
# 🔍 Debug Info (Pilihan)
# =============================================
with st.expander("🔑 Debug Secret ID"):
    st.code(st.secrets)

with st.expander("📄 Debug Sheet ID"):
    st.write(f"ID Data Peserta: {get_secret_id('data_peserta_id')}")
    st.write(f"ID Log Dev: {get_secret_id('log_wlc_dev_id')}")
    st.write(f"ID Rekod Ranking: {get_secret_id('rekod_ranking')}")
