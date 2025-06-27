# devtools.py

import streamlit as st
import pandas as pd
import datetime
import traceback
from app.styles import papar_footer
from app.helper_connection import SHEET_PESERTA, DRIVE_FOLDER_ID, DRIVE_SERVICE, SHEET_LOG, SHEET_REKOD_RANKING
from googleapiclient.errors import HttpError

# ===============================
# ✅ Setup Page
# ===============================
st.set_page_config(page_title="🛠️ WLC DevTools", layout="wide")
st.title("🛠️ Developer Tools - WLC 2025")
st.caption("⚙️ Sistem ini dibangunkan khas untuk DevTeam sahaja. Tidak diakses oleh penganjur atau umum.")

st.subheader("🔗 Status Sambungan")

try:
    SHEET_PESERTA.worksheets()
    st.success("✅ Data Peserta: OK")
except:
    st.error("❌ Data Peserta: Gagal")

try:
    SHEET_LOG.worksheets()
    st.success("✅ Log Dev: OK")
except:
    st.error("❌ Log Dev: Gagal")

try:
    SHEET_REKOD_RANKING.worksheets()
    st.success("✅ Rekod Ranking: OK")
except:
    st.error("❌ Rekod Ranking: Gagal")

try:
    DRIVE_SERVICE.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    st.success("✅ Google Drive: OK")
except:
    st.error("❌ Google Drive: Gagal")

try:
    DRIVE_FOLDER_ID.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    st.success("✅ Google Drive: OK")
except:
    st.error("❌ Google Drive: Gagal")

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