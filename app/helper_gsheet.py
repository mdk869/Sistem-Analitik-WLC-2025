import streamlit as st
import pandas as pd
from app.helper_connection import gc
from app.helper_log import log_error


# ✅ Dapatkan worksheet (akan create jika tak wujud)
def get_worksheet(spreadsheet, worksheet_name):
    try:
        ws = spreadsheet.worksheet(worksheet_name)
    except gspread.exceptions.WorksheetNotFound:
        ws = spreadsheet.add_worksheet(title=worksheet_name, rows="1000", cols="20")
    return ws


# ✅ Load data dari worksheet ke DataFrame
def load_worksheet_to_df(spreadsheet, worksheet_name):
    try:
        ws = get_worksheet(spreadsheet, worksheet_name)
        data = ws.get_all_records()
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        st.error(f"❌ Gagal load data {worksheet_name}: {e}")
        log_error(f"load_worksheet_to_df error - {worksheet_name} - {e}")
        return pd.DataFrame()


# ✅ Simpan rekod ke worksheet (append row)
def append_row(spreadsheet, worksheet_name, row_data):
    try:
        ws = get_worksheet(spreadsheet, worksheet_name)
        ws.append_row(row_data)
    except Exception as e:
        st.error(f"❌ Gagal append row ke {worksheet_name}: {e}")
        log_error(f"append_row error - {worksheet_name} - {e}")


# ✅ Update sel berdasarkan nama kolum
def update_cell(spreadsheet, worksheet_name, row, col, value):
    try:
        ws = get_worksheet(spreadsheet, worksheet_name)
        ws.update_cell(row, col, value)
    except Exception as e:
        st.error(f"❌ Gagal update cell di {worksheet_name}: {e}")
        log_error(f"update_cell error - {worksheet_name} - {e}")
