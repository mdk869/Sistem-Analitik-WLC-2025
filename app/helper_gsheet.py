# app/helper_gsheet.py

import streamlit as st
import pandas as pd
from app.helper_connection import gc
from app.helper_log import log_error
from app.helper_gsheet_utils import get_worksheet


# ====================================================
# ✅ Load Worksheet ke DataFrame
# ====================================================
def load_worksheet_to_df(spreadsheet, worksheet_name):
    try:
        ws = get_worksheet(spreadsheet, worksheet_name)
        data = ws.get_all_records()
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        st.error(f"❌ Gagal load data {worksheet_name}: {e}")
        log_error(f"load_worksheet_to_df error {worksheet_name} - {e}")
        return pd.DataFrame()


# ====================================================
# ✅ Simpan DataFrame ke Worksheet (Replace All)
# ====================================================
def save_df_to_worksheet(spreadsheet, worksheet_name, df: pd.DataFrame):
    try:
        ws = get_worksheet(spreadsheet, worksheet_name)
        ws.clear()
        if not df.empty:
            ws.update([df.columns.tolist()] + df.values.tolist())
        return True
    except Exception as e:
        st.error(f"❌ Gagal simpan data ke {worksheet_name}: {e}")
        log_error(f"save_df_to_worksheet error {worksheet_name} - {e}")
        return False
