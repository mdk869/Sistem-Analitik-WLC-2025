# app/helper_gsheet_utils.py

import streamlit as st

# ====================================================
# ✅ Dapatkan Worksheet (Auto Create Jika Tiada)
# ====================================================
def get_worksheet(spreadsheet, worksheet_name):
    try:
        ws = spreadsheet.worksheet(worksheet_name)
    except Exception:
        ws = spreadsheet.add_worksheet(title=worksheet_name, rows="1000", cols="20")
    return ws

# ====================================================
# ✅ Semak & Cipta Worksheet
# ====================================================
def check_and_create_worksheet(spreadsheet, sheet_name, header):
    try:
        ws = spreadsheet.worksheet(sheet_name)
    except:
        ws = spreadsheet.add_worksheet(title=sheet_name, rows="1000", cols="20")
        ws.append_row(header)
    return ws


# ====================================================
# ✅ Dapatkan Column Index
# ====================================================
def get_column_index(ws, column_name):
    header = ws.row_values(1)
    for idx, col in enumerate(header, start=1):
        if col.strip().lower() == column_name.strip().lower():
            return idx
    return None