import pandas as pd
<<<<<<< HEAD
from app.helper_connection import client


def get_worksheet(spreadsheet, sheet_name):
    return spreadsheet.worksheet(sheet_name)
=======
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
>>>>>>> parent of 95b04d2 (update utils dan get_worksheet)


def load_worksheet_to_df(spreadsheet, sheet_name):
    ws = spreadsheet.worksheet(sheet_name)
    data = ws.get_all_records()
    df = pd.DataFrame(data)
    return df


def save_df_to_worksheet(spreadsheet, sheet_name, df):
    ws = spreadsheet.worksheet(sheet_name)
    ws.clear()
    ws.update([df.columns.values.tolist()] + df.values.tolist())
