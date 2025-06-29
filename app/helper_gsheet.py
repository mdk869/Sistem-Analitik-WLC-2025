import pandas as pd
import streamlit as st
from app.helper_log import log_error


# ✅ Fungsi dapatkan worksheet, cipta jika tidak wujud
def get_worksheet(spreadsheet, worksheet_name, create_if_not_exist=True):
    try:
        ws = spreadsheet.worksheet(worksheet_name)
    except Exception:
        if create_if_not_exist:
            ws = spreadsheet.add_worksheet(title=worksheet_name, rows="1000", cols="20")
            st.info(f"✅ Worksheet '{worksheet_name}' telah dicipta.")
        else:
            st.error(f"❌ Worksheet '{worksheet_name}' tidak wujud.")
            log_error(f"Worksheet '{worksheet_name}' tidak wujud.")
            return None
    return ws


# ✅ Fungsi load worksheet kepada DataFrame
def load_worksheet_to_df(spreadsheet, worksheet_name):
    try:
        ws = get_worksheet(spreadsheet, worksheet_name)
        if ws is None:
            return pd.DataFrame()

        data = ws.get_all_records()
        if data:
            df = pd.DataFrame(data)
        else:
            df = pd.DataFrame()
            st.warning(f"⚠️ Worksheet '{worksheet_name}' kosong.")
        return df
    except Exception as e:
        st.error(f"❌ Gagal load data '{worksheet_name}': {e}")
        log_error(f"load_worksheet_to_df error on '{worksheet_name}' - {e}")
        return pd.DataFrame()


# ✅ Fungsi simpan DataFrame ke worksheet
def save_df_to_worksheet(spreadsheet, worksheet_name, dataframe):
    try:
        ws = get_worksheet(spreadsheet, worksheet_name)

        if ws is None:
            return False

        ws.clear()  # Kosongkan worksheet dahulu
        ws.update([dataframe.columns.values.tolist()] + dataframe.values.tolist())
        st.success(f"✅ Data berjaya disimpan ke '{worksheet_name}'.")
        return True
    except Exception as e:
        st.error(f"❌ Gagal simpan data ke '{worksheet_name}': {e}")
        log_error(f"save_df_to_worksheet error on '{worksheet_name}' - {e}")
        return False
