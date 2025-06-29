# app/helper_log.py

import streamlit as st
from datetime import datetime
from app.helper_connection import SPREADSHEET_LOG


# ====================================================
# ✅ Log Aktiviti Developer
# ====================================================
def log_dev(page, aktiviti, status="Success"):
    try:
        ws = SPREADSHEET_LOG.worksheet("log")
        sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = [sekarang, page, aktiviti, status]
        ws.append_row(row)
    except Exception as e:
        st.warning(f"⚠️ Gagal log aktiviti: {e}")

# ✅ Fungsi Logging Error
def log_error(detail):
    try:
        ws = SPREADSHEET_LOG.worksheet("log_dev")
        sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ws.append_row([sekarang, "ERROR", detail, "Error"])
    except Exception as e:
        print(f"❌ Log Error Gagal: {e}")
