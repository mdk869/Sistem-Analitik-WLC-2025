from app.helper_connection import conn
import pandas as pd
import streamlit as st

# Spreadsheet ID
SPREADSHEET_PESERTA = "1K9JiK8FE1-Cd9fYnDU8Pzqj42TWOGi10wHzHt0avbJ0"
SPREADSHEET_REKOD = "1ADI9k8cd8v9QuPUog5dMLzQTqDo7JXVy0fiw0bZ-Wpw"
SPREADSHEET_LOG = "1d6sQbRRByi4RgglGzmsOIpMA0d2nOjoBc_eACPUa1VE"


def load_data_peserta():
    try:
        sheet = conn.open_by_key(SPREADSHEET_PESERTA).worksheet("peserta")
        data = sheet.get_all_records()
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        st.error(f"❌ Gagal load data peserta: {e}")
        return pd.DataFrame()


def load_rekod_berat_semua():
    try:
        sheet = conn.open_by_key(SPREADSHEET_REKOD).worksheet("rekod_berat")
        data = sheet.get_all_records()
        df = pd.DataFrame(data)

        expected_header = ['Nama', 'NoStaf', 'Tarikh', 'Berat', 'SesiBulan']
        if not set(expected_header).issubset(df.columns):
            st.warning(f"⚠️ Header pada sheet 'rekod_berat' tidak lengkap. Ditemui: {df.columns.tolist()}")
            return pd.DataFrame()

        return df

    except Exception as e:
        st.error(f"❌ Gagal load data rekod berat: {e}")
        return pd.DataFrame()


def save_log_dev(activity, desc, status):
    try:
        sheet = conn.open_by_key(SPREADSHEET_LOG).worksheet("log_dev")
        now = pd.Timestamp.now(tz='Asia/Kuala_Lumpur').strftime('%Y-%m-%d %H:%M:%S')
        sheet.append_row([now, activity, desc, status])
    except Exception as e:
        st.error(f"❌ Gagal simpan log: {e}")
