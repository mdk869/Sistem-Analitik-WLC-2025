# devtools.py

import streamlit as st
import pandas as pd
import datetime
import traceback
from app.styles import papar_footer
from app.helper_connection import connection_checker, connect_drive, connect_gsheet
from googleapiclient.errors import HttpError

# ===============================
# ✅ Setup Page
# ===============================
st.set_page_config(page_title="🛠️ WLC DevTools", layout="wide")
st.title("🛠️ Developer Tools - WLC 2025")
st.caption("⚙️ Sistem ini dibangunkan khas untuk DevTeam sahaja. Tidak diakses oleh penganjur atau umum.")

st.subheader("🔌 Health Check: Connection Status")

status = connection_checker()

for key, value in status.items():
    if "✅" in value:
        st.success(f"{key}: {value}")
    else:
        st.error(f"{key}: {value}")

st.divider()

st.info("🟢 Status ini menunjukkan sama ada sistem dapat berhubung dengan Google Sheets dan Google Drive dengan betul.")

# ===============================
# ✅ Connection Google Sheet/Drive
# ===============================
@st.cache_resource
def init_connection():
    try:
        sheet_conn = connect_gsheet()
        drive_conn = connect_drive()
        return sheet_conn, drive_conn
    except Exception as e:
        st.error("❌ Gagal sambung ke Google Sheet/Drive.")
        st.stop()


sheet_conn, drive_conn = init_connection()


# ===============================
# ✅ Logger Function
# ===============================
def log_event(event, detail):
    try:
        log_sheet = sheet_conn.worksheet("log_event")
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_sheet.append_row([now, event, detail])
    except Exception as e:
        st.error("❌ Gagal log event.")


def log_error(error_detail):
    try:
        error_sheet = sheet_conn.worksheet("log_error")
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_sheet.append_row([now, error_detail])
    except Exception as e:
        st.error("❌ Gagal log error.")


# ===============================
# ✅ Health Check Function
# ===============================
def check_system_health():
    try:
        df = load_data()

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
            sheet = sheet_conn.worksheet("log_event")
        else:
            sheet = sheet_conn.worksheet("log_error")

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