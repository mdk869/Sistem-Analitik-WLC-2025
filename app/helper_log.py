from datetime import datetime
import pytz
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials


# === Setup Google Sheet ===
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
credentials = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"], scopes=scope
)
gc = gspread.authorize(credentials)

# === Sambungan ke Spreadsheet Log
sheet_log = gc.open_by_key(st.secrets["gsheet"]["log_wlc_dev_id"])

# === Check & Auto Create Worksheet
try:
    ws_log = sheet_log.worksheet("log_wlc_dev")
except:
    ws_log = sheet_log.add_worksheet(title="log_wlc_dev", rows="1000", cols="5")
    ws_log.append_row(["Tarikh", "Modul", "Aktiviti", "Status", "Catatan"])

# === Fungsi Logging
def log_dev(modul, aktiviti, status="Selesai", catatan=""):
    waktu = datetime.now(pytz.timezone('Asia/Kuala_Lumpur')).strftime('%Y-%m-%d %H:%M:%S')
    try:
        ws_log.append_row([waktu, modul, aktiviti, status, catatan])
    except Exception as e:
        st.warning(f"Gagal log aktiviti dev: {e}")
