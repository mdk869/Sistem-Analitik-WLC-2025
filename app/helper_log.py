import datetime
from app.helper_connection import SPREADSHEET_LOG


def log_dev(page, event, status):
    sheet = SPREADSHEET_LOG.worksheet("log")
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([now, page, event, status])


def log_error(error_detail):
    sheet = SPREADSHEET_LOG.worksheet("error")
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([now, error_detail])
