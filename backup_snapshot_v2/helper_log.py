# ==========================================
# ✅ Helper Log Aktiviti (Versi Stabil)
# ==========================================

from datetime import datetime
import streamlit as st
from app.helper_gsheet import append_row_to_worksheet, load_worksheet_to_df


# ==========================================
# ✅ Fungsi Log Developer
# ==========================================
def log_dev(module, activity, status="Success"):
    """
    Simpan log aktiviti developer ke Sheet 'log_dev'.

    Args:
        module (str): Nama modul/page (contoh: 'Dashboard', 'Admin').
        activity (str): Deskripsi aktiviti (contoh: 'Buka Tab Info Program').
        status (str): Status aktiviti. Default 'Success'.
    """
    try:
        spreadsheet_id = st.secrets["gsheet"]["log_wlc_dev_id"]
        worksheet_name = "log_dev"

        log_data = {
            "Tarikh": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Module": module,
            "Aktiviti": activity,
            "Status": status
        }

        append_row_to_worksheet(spreadsheet_id, worksheet_name, log_data)

    except Exception as e:
        print(f"❌ Gagal simpan log_dev: {e}")


# ==========================================
# ✅ Fungsi Log Admin/Operasi
# ==========================================
def log_admin(module, activity, status="Success"):
    """
    Simpan log aktiviti admin atau operasi ke Sheet 'log'.

    Args:
        module (str): Nama modul/page.
        activity (str): Deskripsi aktiviti.
        status (str): Status aktiviti.
    """
    try:
        spreadsheet_id = st.secrets["gsheet"]["log_wlc_dev_id"]
        worksheet_name = "log"

        log_data = {
            "Tarikh": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Module": module,
            "Aktiviti": activity,
            "Status": status
        }

        append_row_to_worksheet(spreadsheet_id, worksheet_name, log_data)

    except Exception as e:
        print(f"❌ Gagal simpan log_admin: {e}")


# ==========================================
# ✅ Fungsi Log Umum ke Sheet1 (Opsional)
# ==========================================
def log_umum(module, activity, status="Success"):
    """
    Simpan log umum ke Sheet 'Sheet1'.

    Args:
        module (str): Nama modul/page.
        activity (str): Deskripsi aktiviti.
        status (str): Status aktiviti.
    """
    try:
        spreadsheet_id = st.secrets["gsheet"]["log_wlc_dev_id"]
        worksheet_name = "Sheet1"

        log_data = {
            "Tarikh": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Module": module,
            "Aktiviti": activity,
            "Status": status
        }

        append_row_to_worksheet(spreadsheet_id, worksheet_name, log_data)

    except Exception as e:
        print(f"❌ Gagal simpan log_umum: {e}")


# ==========================================
# ✅ Fungsi Load Log (Papar Log)
# ==========================================
def load_log(sheet_name="log_dev"):
    """
    Load data log dari sheet yang dipilih.

    Args:
        sheet_name (str): Nama sheet ('log_dev', 'log', 'Sheet1').

    Returns:
        pd.DataFrame: Data log.
    """
    try:
        spreadsheet_id = st.secrets["gsheet"]["log_wlc_dev_id"]
        df = load_worksheet_to_df(spreadsheet_id, sheet_name)
        return df

    except Exception as e:
        print(f"❌ Gagal load log dari sheet {sheet_name}: {e}")
        return None
