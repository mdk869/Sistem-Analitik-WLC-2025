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

local_tz = pytz.timezone("Asia/Kuala_Lumpur")


# ============================================
# ✅ Logging Function
# ============================================
def log_dev(modul, aktiviti, status="OK", catatan="-"):
    try:
        now = datetime.now(local_tz).strftime('%Y-%m-%d %H:%M:%S')
        ws_log.append_row([now, modul, aktiviti, status, catatan])
    except Exception as e:
        print(f"[Log Error] {e}")


# ============================================
# ✅ Export Fungsi
# ============================================
__all__ = ["log_dev"]
