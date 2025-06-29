from app.helper_connection import client
import pandas as pd
import streamlit as st


def open_worksheet(spreadsheet_id, worksheet_name):
    try:
        sheet = client.open_by_key(spreadsheet_id).worksheet(worksheet_name)
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


def append_data_to_worksheet(spreadsheet_id, worksheet_name, data_dict):
    """
    Tambah satu row data ke worksheet Google Sheet.
    """
    sh = client.open_by_key(spreadsheet_id)
    worksheet = sh.worksheet(worksheet_name)

    existing_data = worksheet.get_all_values()

    if not existing_data:
        headers = list(data_dict.keys())
        worksheet.append_row(headers)

    values = list(data_dict.values())
    worksheet.append_row(values)

    return True


def padam_baris_dari_worksheet(spreadsheet_id, worksheet_name, column_key, value):
    """
    Padam baris daripada worksheet berdasarkan nilai dalam column tertentu.
    """
    sh = client.open_by_key(spreadsheet_id)
    worksheet = sh.worksheet(worksheet_name)

    data = worksheet.get_all_records()

    if not data:
        return False

    df = pd.DataFrame(data)

    # Semak jika data wujud
    if value not in df[column_key].values:
        return False

    # Buang baris yang sepadan
    df = df[df[column_key] != value]

    # Clear worksheet dan update semula
    worksheet.clear()
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())

    return True