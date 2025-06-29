import pandas as pd
import streamlit as st



def get_worksheet(spreadsheet, worksheet_name):
    try:
        ws = spreadsheet.worksheet(worksheet_name)
    except Exception:
        ws = spreadsheet.add_worksheet(title=worksheet_name, rows="1000", cols="20")
    return ws


def load_worksheet_to_df(spreadsheet, worksheet_name):
    try:
        ws = get_worksheet(spreadsheet, worksheet_name)
        data = ws.get_all_records()
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        st.error(f"Gagal load data {worksheet_name}: {e}")
        log_error(f"load_worksheet_to_df error {worksheet_name} - {e}")
        return pd.DataFrame()
