from app.helper_gsheet import get_worksheet


def check_worksheet_exists(spreadsheet, worksheet_name):
    """Semak sama ada worksheet wujud."""
    try:
        worksheet = get_worksheet(spreadsheet, worksheet_name)
        return worksheet is not None
    except Exception:
        return False


def create_worksheet_if_not_exists(spreadsheet, worksheet_name, rows=1000, cols=20):
    """Cipta worksheet jika belum wujud."""
    if not check_worksheet_exists(spreadsheet, worksheet_name):
        spreadsheet.add_worksheet(title=worksheet_name, rows=str(rows), cols=str(cols))
        return True
    return False
