import datetime
import traceback
import pandas as pd
from app.helper_connection import SPREADSHEET_LOG
from app.helper_gsheet import get_worksheet


def log_event(page, event, status="Success"):
    """Log aktiviti."""
    try:
        ws = get_worksheet(SPREADSHEET_LOG, "log_event")
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ws.append_row([now, page, event, status])
    except Exception as e:
        print(f"❌ Log Event Error: {e}")


def log_error(page, error_message):
    """Log error."""
    try:
        ws = get_worksheet(SPREADSHEET_LOG, "log_error")
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ws.append_row([now, page, error_message])
    except Exception as e:
        print(f"❌ Log Error Error: {e}")


def load_log(log_type="event"):
    """Load log event atau error."""
    try:
        sheet_name = "log_event" if log_type == "event" else "log_error"
        ws = get_worksheet(SPREADSHEET_LOG, sheet_name)
        data = ws.get_all_records()
        return pd.DataFrame(data)
    except Exception as e:
        print(f"❌ Load Log Error: {e}")
        return pd.DataFrame()
