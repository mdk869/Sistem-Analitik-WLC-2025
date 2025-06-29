import streamlit as st
import pandas as pd
import datetime

from app.styles import papar_footer
from app.helper_connection import (
    SPREADSHEET_RANKING, SPREADSHEET_LOG, SPREADSHEET_PESERTA
)
from app.helper_drive import list_files_in_folder
from app.helper_gsheet import get_worksheet

from app.helper_log_utils import (
    log_event, log_error, clear_log, load_log, check_system_health
)


# ===============================
# ✅ Page Setup
# ===============================
st.set_page_config(page_title="🛠️ WLC DevTools", layout="wide")
st.title("🛠️ Developer Tools - WLC 2025")
st.caption("⚙️ Sistem ini dibangunkan khas untuk DevTeam sahaja. Tidak diakses oleh umum atau penganjur.")


# ===============================
# ✅ Tabs Layout
# ===============================
tab1, tab2 = st.tabs(["🔗 Status Sambungan", "🪛 Debug Console"])


# ===============================
# ✅ Tab 1: Status Sambungan
# ===============================
with tab1:
    st.subheader("🔗 Status Sambungan Google Sheets & Drive")

    try:
        ws_peserta = get_worksheet(SPREADSHEET_PESERTA, "peserta")
        peserta = ws_peserta.get_all_records()
        st.success(f"✅ Data Peserta: {len(peserta)} rekod dijumpai.")
    except Exception as e:
        st.error(f"❌ Data Peserta GAGAL: {e}")

    try:
        ws_log_event = get_worksheet(SPREADSHEET_LOG, "log_event")
        log_event_data = ws_log_event.get_all_records()
        st.success(f"✅ Log Event: {len(log_event_data)} rekod.")
    except Exception as e:
        st.error(f"❌ Log Event GAGAL: {e}")

    try:
        ws_log_error = get_worksheet(SPREADSHEET_LOG, "log_error")
        log_error_data = ws_log_error.get_all_records()
        st.success(f"✅ Log Error: {len(log_error_data)} rekod.")
    except Exception as e:
        st.error(f"❌ Log Error GAGAL: {e}")

    try:
        ws_ranking = get_worksheet(SPREADSHEET_RANKING, "rekod")
        ranking = ws_ranking.get_all_records()
        st.success(f"✅ Rekod Ranking: {len(ranking)} rekod.")
    except Exception as e:
        st.error(f"❌ Rekod Ranking GAGAL: {e}")

    try:
        files = list_files_in_folder()
        st.success(f"✅ Google Drive OK: {len(files)} fail dalam folder.")
        with st.expander("📂 Senarai Fail dalam Google Drive"):
            for file in files:
                st.write(f"📄 {file['name']} (ID: {file['id']})")
    except Exception as e:
        st.error(f"❌ Google Drive GAGAL: {e}")


# ===============================
# ✅ Tab 2: Debug Console
# ===============================
with tab2:
    st.subheader("🪛 Debug Console")

    action = st.selectbox("Pilih Debug Action", [
        "✅ Check System Health",
        "📜 Show Event Log",
        "🪲 Show Error Log",
        "♻️ Clear Event Log",
        "♻️ Clear Error Log"
    ])

    st.divider()

    if action == "✅ Check System Health":
        st.subheader("✅ System Health Report")
        df = check_system_health()
        st.dataframe(df, use_container_width=True)

    elif action == "📜 Show Event Log":
        st.subheader("📜 Event Log")
        df = load_log(log_type="event")
        if df.empty:
            st.info("⚠️ Tiada rekod event.")
        else:
            st.dataframe(df, use_container_width=True)

    elif action == "🪲 Show Error Log":
        st.subheader("🪲 Error Log")
        df = load_log(log_type="error")
        if df.empty:
            st.info("⚠️ Tiada rekod error.")
        else:
            st.dataframe(df, use_container_width=True)

    elif action == "♻️ Clear Event Log":
        st.subheader("♻️ Clear Event Log")
        if st.button("🚨 Kosongkan Event Log"):
            result = clear_log("event")
            if result:
                st.success("✅ Event Log berjaya dikosongkan.")

    elif action == "♻️ Clear Error Log":
        st.subheader("♻️ Clear Error Log")
        if st.button("🚨 Kosongkan Error Log"):
            result = clear_log("error")
            if result:
                st.success("✅ Error Log berjaya dikosongkan.")


# ===============================
# ✅ Footer
# ===============================
papar_footer(
    owner="MKR Dev Team",
    version="v4.1.0",
    last_update="2025-06-29",
    tagline="Empowering Data-Driven Decisions."
)
