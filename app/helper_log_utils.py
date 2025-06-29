import datetime
import pandas as pd
import traceback
from app.helper_gsheet import get_worksheet
from app.helper_connection import SPREADSHEET_LOG


# ==========================
# ✅ Log Event
# ==========================
def log_event(event, detail):
    """
    Log aktiviti ke worksheet 'log_event'.
    """
    try:
        ws = get_worksheet(SPREADSHEET_LOG, "log_event")
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ws.append_row([now, event, detail])
        return True
    except Exception as e:
        print(f"[LOG EVENT ERROR] {e}")
        return False


# ==========================
# ✅ Log Error
# ==========================
def log_error(error_detail):
    """
    Log error ke worksheet 'log_error'.
    """
    try:
        ws = get_worksheet(SPREADSHEET_LOG, "log_error")
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ws.append_row([now, error_detail])
        return True
    except Exception as e:
        print(f"[LOG ERROR] {e}")
        return False


# ==========================
# ✅ Clear Log (Event/Error)
# ==========================
def clear_log(log_type="event"):
    """
    Kosongkan log. Pilihan: 'event' atau 'error'.
    """
    try:
        ws = get_worksheet(SPREADSHEET_LOG, f"log_{log_type}")
        ws.clear()

        # Tambah header semula
        if log_type == "event":
            ws.append_row(["Timestamp", "Event", "Detail"])
        else:
            ws.append_row(["Timestamp", "ErrorDetail"])

        return True
    except Exception as e:
        print(f"[CLEAR LOG ERROR] {e}")
        return False


# ==========================
# ✅ Load Log (Event/Error)
# ==========================
def load_log(log_type="event"):
    """
    Load log 'event' atau 'error' sebagai DataFrame.
    """
    try:
        ws = get_worksheet(SPREADSHEET_LOG, f"log_{log_type}")
        data = ws.get_all_records()
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        print(f"[LOAD LOG ERROR] {e}")
        return pd.DataFrame()


# ==========================
# ✅ Health Check Function
# ==========================
from app.helper_data import load_data_peserta


def check_system_health():
    """
    Semak kesihatan sistem: missing BMI, Berat, Tarikh.
    """
    try:
        df = load_data_peserta()

        result = pd.DataFrame([{
            "Status": "✅ OK",
            "Total Peserta": len(df),
            "Missing BMI": df['BMI'].isnull().sum(),
            "Missing Berat Terkini": df['BeratTerkini'].isnull().sum(),
            "Missing Tarikh Timbang": df['TarikhTimbang'].isnull().sum(),
            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }])

        log_event("HealthCheck", "Check OK")
        return result

    except Exception as e:
        error_detail = traceback.format_exc()
        log_error(error_detail)
        return pd.DataFrame([{
            "Status": "❌ Error",
            "Detail": str(e),
            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }])
