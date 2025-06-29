import pandas as pd
from app.helper_connection import client


def get_worksheet(spreadsheet, worksheet_name):
    """Dapatkan objek worksheet."""
    try:
        return spreadsheet.worksheet(worksheet_name)
    except Exception as e:
        print(f"❌ Error get_worksheet: {e}")
        return None


def load_worksheet_to_df(spreadsheet, worksheet_name):
    """Muat naik worksheet ke DataFrame."""
    try:
        ws = get_worksheet(spreadsheet, worksheet_name)
        if ws:
            data = ws.get_all_records()
            df = pd.DataFrame(data)
            return df
        else:
            return pd.DataFrame()
    except Exception as e:
        print(f"❌ Error load_worksheet_to_df: {e}")
        return pd.DataFrame()


def save_df_to_worksheet(spreadsheet, worksheet_name, df):
    """Simpan DataFrame ke worksheet (overwrite)."""
    try:
        ws = get_worksheet(spreadsheet, worksheet_name)
        if ws:
            ws.clear()
            ws.update([df.columns.values.tolist()] + df.values.tolist())
            return True
        else:
            return False
    except Exception as e:
        print(f"❌ Error save_df_to_worksheet: {e}")
        return False
