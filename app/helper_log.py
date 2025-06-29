from app.helper_gsheet import open_worksheet
import pandas as pd
import streamlit as st


SPREADSHEET_LOG = st.secrets["gsheet"]["log_dev"]


def save_log_dev(activity, desc, status):
    try:
        sheet = open_worksheet(SPREADSHEET_LOG, "log_dev")
        now = pd.Timestamp.now(tz='Asia/Kuala_Lumpur').strftime('%Y-%m-%d %H:%M:%S')
        sheet.append_row([now, activity, desc, status])
    except Exception as e:
        st.error(f"❌ Gagal simpan log: {e}")
