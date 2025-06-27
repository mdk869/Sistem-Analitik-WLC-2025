# app/helper_log.py

import streamlit as st
from datetime import datetime
from app.helper_connection import SHEET_LOG, get_worksheet


# ====================================================
# ✅ Log Aktiviti Developer
# ====================================================
def log_dev(page, aktiviti, status="Success"):
    try:
        ws = get_worksheet(SHEET_LOG, "log")

        sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        row = [sekarang, page, aktiviti, status]
        ws.append_row(row)
    except Exception as e:
        st.warning(f"⚠️ Gagal log aktiviti: {e}")
