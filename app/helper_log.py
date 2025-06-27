# app/helper_log.py

import pandas as pd
from datetime import datetime
from app.helper_utils import get_tarikh_masa
from app.helper_data import connect_gsheet
import streamlit as st


# ============================================
# ✅ Nama Spreadsheet & Sheet
# ============================================
SPREADSHEET_NAME = st.secrets["gsheets"]["spreadsheet_log"]
SHEET_NAME = "log_wlc_dev"

# ============================================
# ✅ Fungsi Log Aktiviti Developer
# ============================================
def log_dev(modul: str, aktiviti: str, status: str = "Selesai", catatan: str = "") -> None:
    """
    Log aktiviti ke Google Sheet log_dev.

    Args:
        modul (str): Nama modul contoh: 'Dashboard'
        aktiviti (str): Info aktiviti contoh: 'Load Data'
        status (str): Status (default 'Selesai')
        catatan (str): Catatan tambahan
    """
    try:
        sh = connect_gsheet(SPREADSHEET_NAME)
        worksheet = sh.worksheet(SHEET_NAME)
    except Exception as e:
        st.warning(f"⚠️ Tidak dapat akses sheet log: {e}")
        return

    tarikh = get_tarikh_masa()

    # === Semak header atau cipta
    header = ["Tarikh", "Modul", "Aktiviti", "Status", "Catatan"]
    existing_header = worksheet.row_values(1)

    if existing_header != header:
        worksheet.update("A1", [header])

    # === Masukkan log
    new_row = [tarikh, modul, aktiviti, status, catatan]
    try:
        worksheet.append_row(new_row, value_input_option="USER_ENTERED")
    except Exception as e:
        st.warning(f"⚠️ Gagal log aktiviti: {e}")


# ============================================
# ✅ Load Log History
# ============================================
def load_log_history() -> pd.DataFrame:
    """
    Load semua log aktiviti developer.

    Returns:
        pd.DataFrame: DataFrame log aktiviti
    """
    try:
        sh = connect_gsheet(SPREADSHEET_NAME)
        worksheet = sh.worksheet(SHEET_NAME)
        data = worksheet.get_all_records()

        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data)
        return df

    except Exception as e:
        st.warning(f"⚠️ Tidak dapat load log: {e}")
        return pd.DataFrame()


# ============================================
# ✅ Export Fungsi
# ============================================
__all__ = [
    "log_dev",
    "load_log_history"
]
