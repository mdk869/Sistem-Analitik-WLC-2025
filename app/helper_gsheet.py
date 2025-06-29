from app.helper_connection import conn
import pandas as pd
import streamlit as st


def open_worksheet(spreadsheet_id, worksheet_name):
    try:
        sheet = conn.open_by_key(spreadsheet_id).worksheet(worksheet_name)
        return sheet
    except Exception as e:
        st.error(f"❌ Gagal buka sheet '{worksheet_name}': {e}")
        return None


def load_worksheet_to_df(spreadsheet_id, worksheet_name):
    sheet = open_worksheet(spreadsheet_id, worksheet_name)
    if sheet:
        data = sheet.get_all_records()
        df = pd.DataFrame(data)
        return df
    return pd.DataFrame()


def save_df_to_worksheet(spreadsheet_id, worksheet_name, df):
    sheet = open_worksheet(spreadsheet_id, worksheet_name)
    if sheet is None:
        return False

    sheet.clear()
    sheet.update([df.columns.values.tolist()] + df.values.tolist())
    return True
