# app/helper_log.py

from datetime import datetime
import pytz
import streamlit as st
from app.helper_connection import SHEET_LOG


# ============================================
# ✅ Setup Sheet Log
# ============================================
SHEET_NAME = "log_wlc_dev"

try:
    ws_log = SHEET_LOG.worksheet(SHEET_NAME)
except:
    ws_log = SHEET_LOG.add_worksheet(title=SHEET_NAME, rows="1000", cols="5")
    ws_log.append_row(["Tarikh", "Modul", "Aktiviti", "Status", "Catatan"])


# ============================================
# ✅ Fungsi Log Aktiviti Developer
# ============================================
def log_dev(modul, aktiviti, status="Selesai", catatan=""):
    waktu = datetime.now(pytz.timezone('Asia/Kuala_Lumpur')).strftime('%Y-%m-%d %H:%M:%S')
    try:
        ws_log.append_row([waktu, modul, aktiviti, status, catatan])
    except Exception as e:
        st.warning(f"⚠️ Gagal log aktiviti dev: {e}")


# ============================================
# ✅ Export Fungsi
# ============================================
__all__ = ["log_dev"]
