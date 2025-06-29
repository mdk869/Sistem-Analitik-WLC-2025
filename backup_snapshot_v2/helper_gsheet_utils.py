# app/helper_gsheet_utils.py

import streamlit as st
from app.helper_gsheet import get_worksheet
from app.helper_log import log_dev, log_error, log_warning


# ====================================================
# ✅ Semak & Cipta Worksheet
# ====================================================
def check_and_create_worksheet(spreadsheet, sheet_name, header):
    try:
        ws_list = [ws.title for ws in spreadsheet.worksheets()]
        if sheet_name not in ws_list:
            ws_new = spreadsheet.add_worksheet(title=sheet_name, rows=1000, cols=len(header) + 5)
            ws_new.append_row(header)
            log_dev("System", f"Sheet {sheet_name} dicipta dengan header.", "Success")
        ws = get_worksheet(spreadsheet, sheet_name)

        # Semak header
        current_header = ws.row_values(1)
        if [h.strip().lower() for h in current_header] != [h.strip().lower() for h in header]:
            ws.clear()
            ws.append_row(header)
            log_warning(f"Header sheet {sheet_name} tidak sepadan. Reset header.")

        return ws
    except Exception as e:
        log_error(f"❌ Gagal check/create sheet {sheet_name}: {e}")
        st.error(f"❌ Error check/create sheet {sheet_name}: {e}")
        return None


# ====================================================
# ✅ Dapatkan Column Index
# ====================================================
def get_column_index(worksheet, column_name):
    try:
        header = worksheet.row_values(1)
        return header.index(column_name) + 1
    except ValueError:
        st.error(f"❌ Kolum '{column_name}' tidak ditemui dalam worksheet.")
        return None
