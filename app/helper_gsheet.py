from app.helper_connection import client


def load_worksheet_to_df(spreadsheet, worksheet_name):
    """Load data dari worksheet ke DataFrame"""
    try:
        ws = spreadsheet.worksheet(worksheet_name)
        data = ws.get_all_records()
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        print(f"❌ Error load_worksheet_to_df: {e}")
        return pd.DataFrame()


def save_df_to_worksheet(spreadsheet, worksheet_name, df):
    """Simpan DataFrame ke worksheet (overwrite)"""
    try:
        ws = spreadsheet.worksheet(worksheet_name)
        ws.clear()
        ws.update([df.columns.values.tolist()] + df.values.tolist())
        return True
    except Exception as e:
        print(f"❌ Error save_df_to_worksheet: {e}")
        return False


def get_worksheet(spreadsheet, worksheet_name):
    """Get worksheet object"""
    try:
        return spreadsheet.worksheet(worksheet_name)
    except Exception as e:
        print(f"❌ Error get_worksheet: {e}")
        return None
