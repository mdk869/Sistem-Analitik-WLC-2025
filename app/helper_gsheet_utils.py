import streamlit as st

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