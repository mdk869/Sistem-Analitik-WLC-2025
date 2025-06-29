import streamlit as st
from datetime import datetime
from app.helper_connection import gc, get_secret_id
from app.helper_gsheet import get_worksheet


# ✅ Setup spreadsheet log
SPREADSHEET_LOG = gc.open_by_key(get_secret_id("gsheet", "log_wlc_dev_id"))


# ✅ Fungsi utama untuk log
def write_log(page, aktiviti, status):
    try:
        ws = get_worksheet(SPREADSHEET_LOG, "log_dev")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ws.append_row([now, page, aktiviti, status])
    except Exception as e:
        print(f"❌ Gagal tulis log: {e}")


# ✅ Fungsi-fungsi log mengikut kategori
def log_dev(page, aktiviti, status="Success"):
    write_log(page, aktiviti, status)


def log_error(detail):
    write_log("ERROR", detail, "Error")


def log_info(detail):
    write_log("INFO", detail, "Info")


def log_warning(detail):
    write_log("WARNING", detail, "Warning")
