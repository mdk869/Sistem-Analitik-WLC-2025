import streamlit as st
from datetime import datetime
from app.helper_connection import gc, get_secret_id
from app.helper_gsheet import get_worksheet


# ✅ Setup spreadsheet log
SPREADSHEET_LOG = gc.open_by_key(get_secret_id("gsheet", "log_wlc_dev_id"))

# ✅ Log Aktiviti Developer
def log_dev(page, aktiviti, status="Success"):
    try:
        ws = get_worksheet(SPREADSHEET_LOG, "log_dev")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ws.append_row([now, page, aktiviti, status])
    except Exception as e:
        st.warning(f"⚠️ Gagal log aktiviti: {e}")


# ✅ Log Error
def log_error(detail):
    try:
        ws = get_worksheet(SPREADSHEET_LOG, "log_dev")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ws.append_row([now, "ERROR", detail, "Error"])
    except Exception as e:
        print(f"❌ Log Error Gagal: {e}")


# ✅ Log Info
def log_info(detail):
    try:
        ws = get_worksheet(SPREADSHEET_LOG, "log_dev")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ws.append_row([now, "ERROR", detail, "Error"])
    except Exception as e:
        print(f"❌ Log Info: {e}")


# ✅ Log Warning
def log_warning(detail):
    try:
        ws = get_worksheet(SPREADSHEET_LOG, "log_dev")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ws.append_row([now, "ERROR", detail, "Error"])
    except Exception as e:
        print(f"⚠️ Log Warning: {e}")

