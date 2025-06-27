# app/helper_log.py

import pytz
from datetime import datetime
from app.helper_connection import SHEET_LOG
from app.helper_utils import check_or_create_worksheet


# ============================================
# ✅ Sheet & Worksheet Setup
# ============================================
SHEET_NAME = "log_wlc_dev"
HEADER = ["Tarikh", "Modul", "Aktiviti", "Status", "Catatan"]

ws_log = check_or_create_worksheet(SHEET_LOG, SHEET_NAME, HEADER)


# ============================================
# ✅ Logging Function
# ============================================
def log_dev(modul, aktiviti, status, catatan="-"):
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ws_log.append_row([waktu, modul, aktiviti, status, catatan])


# ============================================
# ✅ Export Fungsi
# ============================================
__all__ = ["log_dev"]
