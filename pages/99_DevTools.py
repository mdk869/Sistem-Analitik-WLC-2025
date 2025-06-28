# devtools.py

import streamlit as st
import pandas as pd
import datetime
import traceback
from app.styles import papar_footer
from app.helper_connection import SPREADSHEET_RANKING, SPREADSHEET_LOG, SPREADSHEET_PESERTA, DRIVE, DRIVE_FOLDER_ID, get_worksheet, list_files_in_folder
from app.helper_data import load_data_peserta
from googleapiclient.errors import HttpError

# ===============================
# ✅ Setup Page
# ===============================
st.set_page_config(page_title="🛠️ WLC DevTools", layout="wide")
st.title("🛠️ Developer Tools - WLC 2025")
st.caption("⚙️ Sistem ini dibangunkan khas untuk DevTeam sahaja. Tidak diakses oleh penganjur atau umum.")

st.subheader("🔗 Status Sambungan")

try:
    ws_peserta = get_worksheet(SPREADSHEET_PESERTA, "data")
    peserta = ws_peserta.get_all_records()
    st.success(f"✅ Data Peserta: {len(peserta)} rekod dijumpai")
except Exception as e:
    st.error(f"❌ Data Peserta GAGAL: {e}")

try:
    ws_log = get_worksheet(SPREADSHEET_LOG, "log")
    log = ws_log.get_all_records()
    st.success(f"✅ Log Dev: {len(log)} rekod")
except Exception as e:
    st.error(f"❌ Log Dev GAGAL: {e}")

try:
    ws_ranking = get_worksheet(SPREADSHEET_RANKING, "rekod")
    rekod = ws_ranking.get_all_records()
    st.success(f"✅ Rekod Ranking: {len(rekod)} rekod")
except Exception as e:
    st.error(f"❌ Rekod Ranking GAGAL: {e}")

try:
    files = list_files_in_folder()
    st.success(f"✅ Google Drive OK: {len(files)} file dalam folder.")
    for file in files:
        st.write(f"📄 {file['name']} (ID: {file['id']})")
except Exception as e:
    st.error(f"❌ Google Drive GAGAL: {e}")

# ===============================
# ✅ Logger Function
# ===============================
def log_event(event, detail):
    try:
        log_sheet = SPREADSHEET_LOG.worksheet("log_event")
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_sheet.append_row([now, event, detail])
    except Exception as e:
        st.error("❌ Gagal log event.")


def log_error(error_detail):
    try:
        error_sheet = SPREADSHEET_LOG.worksheet("log_error")
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_sheet.append_row([now, error_detail])
    except Exception as e:
        st.error("❌ Gagal log error.")


# ===============================
# ✅ Health Check Function
# ===============================
def check_system_health():
    try:
        df = load_data_peserta()

        missing_bmi = df['BMI'].isnull().sum()
        missing_berat = df['BeratTerkini'].isnull().sum()
        missing_tarikh = df['TarikhTimbang'].isnull().sum()

        status = "✅ Google Sheet Connected"
        result = {
            "Status": status,
            "Total Peserta": len(df),
            "Missing BMI": missing_bmi,
            "Missing Berat Terkini": missing_berat,
            "Missing Tarikh Timbang": missing_tarikh,
        }

        log_event("HealthCheck", f"Check OK: {result}")
        return result

    except Exception as e:
        error_detail = traceback.format_exc()
        log_error(error_detail)
        return {"Status": "❌ Error", "Detail": str(e)}


# ===============================
# ✅ Load Log Function
# ===============================
def load_log(log_type="event"):
    try:
        if log_type == "event":
            sheet = SPREADSHEET_LOG.worksheet("log_event")
        else:
            sheet = SPREADSHEET_LOG.worksheet("log_error")

        data = sheet.get_all_records()
        df = pd.DataFrame(data)
        return df

    except Exception as e:
        st.error("❌ Gagal load log.")
        return pd.DataFrame()


# ===============================
# ✅ Debug Console
# ===============================
def debug_console():
    st.subheader("🔧 Debug Console")

    action = st.selectbox("Pilih Debug Action", [
        "Check Health",
        "Show Event Log",
        "Show Error Log"
    ])

    if action == "Check Health":
        st.json(check_system_health())

    elif action == "Show Event Log":
        df = load_log(log_type="event")
        st.dataframe(df, use_container_width=True)

    elif action == "Show Error Log":
        df = load_log(log_type="error")
        st.dataframe(df, use_container_width=True)


# ===============================
# ✅ La

papar_footer(
    owner="MKR Dev Team",
    version="v3.2.5",
    last_update="2025-06-27",
    tagline="Empowering Data-Driven Decisions."
)