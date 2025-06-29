# app/helper_log.py

import streamlit as st
from datetime import datetime
from app.helper_connection import gc, get_secret_id
from app.helper_gsheet_utils import get_worksheet


# =====================================================
# ✅ Setup Spreadsheet Log
# =====================================================
try:
    SPREADSHEET_LOG = gc.open_by_key(get_secret_id("gsheet", "log_wlc_dev_id"))
except Exception as e:
    st.error(f"❌ Gagal sambung ke Spreadsheet Log: {e}")
    SPREADSHEET_LOG = None


# =====================================================
# ✅ Simpan Log ke Local Fail jika gagal
# =====================================================
def save_log_local(tarikh, page, aktiviti, status):
    try:
        with open("log_wlc.txt", "a", encoding="utf-8") as file:
            file.write(f"{tarikh} | {page} | {aktiviti} | {status}\n")
    except Exception as e:
        print(f"⚠️ Gagal simpan log ke fail tempatan: {e}")


# =====================================================
# ✅ Tulis Log ke Spreadsheet
# =====================================================
def write_log(page: str, aktiviti: str, status: str = "Success"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        if SPREADSHEET_LOG:
            ws = get_worksheet(SPREADSHEET_LOG, "log_dev")
            ws.append_row([now, page, aktiviti, status])
        else:
            raise Exception("SPREADSHEET_LOG tidak wujud.")

    except Exception as e:
        save_log_local(now, page, aktiviti, status)
        print(f"❌ Gagal tulis log ke Google Sheet. Log disimpan ke local. Error: {e}")


# =====================================================
# ✅ Fungsi Log Developer
# =====================================================
def log_dev(page: str, aktiviti: str, status: str = "Success"):
    write_log(page, aktiviti, status)


# =====================================================
# ✅ Fungsi Log Error
# =====================================================
def log_error(detail: str):
    write_log("ERROR", detail, "Error")


# =====================================================
# ✅ Fungsi Log Info
# =====================================================
def log_info(detail: str):
    write_log("INFO", detail, "Info")


# =====================================================
# ✅ Fungsi Log Warning
# =====================================================
def log_warning(detail: str):
    write_log("WARNING", detail, "Warning")
