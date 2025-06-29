from app.helper_connection import client
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



def tambah_data_peserta(spreadsheet_id, worksheet_name, data_dict):
    """
    Tambah satu row data peserta ke Google Sheet.
    """
    sh = client.open_by_key(spreadsheet_id)
    ws = sh.worksheet(worksheet_name)

    df_existing = pd.DataFrame(ws.get_all_records())

    new_row = pd.DataFrame([data_dict])

    df_updated = pd.concat([df_existing, new_row], ignore_index=True)

    ws.clear()
    ws.update([df_updated.columns.values.tolist()] + df_updated.values.tolist())

    return True
