# app/helper_log.py

import streamlit as st
from datetime import datetime
from app.helper_connection import SPREADSHEET_LOG, get_worksheet


# ====================================================
# ✅ Log Aktiviti Developer
# ====================================================
def log_dev(page, aktiviti, status="Success"):
    try:
        ws = get_worksheet(SPREADSHEET_LOG, "log")

        sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        row = [sekarang, page, aktiviti, status]
        ws.append_row(row)
    except Exception as e:
        st.warning(f"⚠️ Gagal log aktiviti: {e}")

def log_error(detail):
    """
    Log error ke Google Sheet 'log_dev'.
    
    Args:
        detail (str): Detail atau exception error.
    """
    try:
        from datetime import datetime

        # ✅ Masa semasa
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # ✅ Akses worksheet log_dev
        ws = get_worksheet(SPREADSHEET_LOG, "log_dev")

        # ✅ Masukkan log error
        ws.append_row([now, "ERROR", detail, "Error"])

    except Exception as e:
        print(f"❌ Log Error Gagal: {e}")
