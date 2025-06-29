<<<<<<< HEAD
import datetime
from app.helper_connection import SPREADSHEET_LOG
=======
import streamlit as st
from datetime import datetime
from app.helper_connection import gc, get_secret_id
from app.helper_gsheet import get_worksheet
>>>>>>> parent of baf1351 (Update helper_log.py)


def log_dev(page, event, status):
    sheet = SPREADSHEET_LOG.worksheet("log")
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([now, page, event, status])


def log_error(error_detail):
    sheet = SPREADSHEET_LOG.worksheet("error")
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([now, error_detail])
