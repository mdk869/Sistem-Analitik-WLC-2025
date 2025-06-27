from datetime import datetime
import pytz
import streamlit as st

import gspread
from google.oauth2.service_account import Credentials


# === Setup sambungan Google Sheet untuk Log
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
credentials = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"], scopes=scope
)
gc = gspread.authorize(credentials)

# Sambungan ke Spreadsheet Log
sheet_log = gc.open_by_key(st.secrets["gsheet"]["log_wlc_dev_id"])

# Worksheet untuk log
ws_log = sheet_log.worksheet("log_dev")


# === Fungsi Logging Aktiviti Developer
def log_dev(aktiviti, keterangan):
    waktu = datetime.now(pytz.timezone('Asia/Kuala_Lumpur')).strftime('%Y-%m-%d %H:%M:%S')
    try:
        ws_log.append_row([waktu, aktiviti, keterangan])
    except Exception as e:
        st.warning(f"Gagal log aktiviti dev: {e}")
