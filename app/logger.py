# logger.py

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import streamlit as st
import requests

# =========================================
# ✅ Get Visitor Info (IP, Location, User Agent)
# =========================================
def get_visitor_info():
    try:
        res = requests.get("https://ipinfo.io/json", timeout=5).json()
        ip = res.get("ip", "Unknown")
        location = f"{res.get('city', '')}, {res.get('region', '')}".strip(', ')
        org = res.get("org", "Unknown")
    except Exception:
        ip, location, org = "Unknown", "Unknown", "Unknown"

    # Attempt to detect user agent from request headers
    try:
        user_agent = st.runtime.scriptrunner.get_script_run_ctx().request.headers.get("User-Agent", "Unknown")
    except Exception:
        user_agent = "Unknown"

    return ip, location, org, user_agent


# =========================================
# ✅ Log Traffic to Google Sheet
# =========================================
def log_traffic_to_sheet():
    try:
        # Setup scope
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]

        # Prepare credentials (read-only, not modifying secrets)
        creds_dict = dict(st.secrets["gcp_service_account"])  # create a copy
        creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)

        # Access specific sheet by name (lebih stabil dari .sheet1)
        sheet_id = st.secrets["gsheet"]["log_wlc_dev_id"]
        sheet = client.open_by_key(sheet_id).worksheet("LogTraffic")  # Pastikan tab ini wujud

        # Collect traffic info
        ip, location, org, user_agent = get_visitor_info()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Simpan log ke sheet
        sheet.append_row([timestamp, ip, location, org, user_agent])

    except Exception as e:
        st.warning(f"❌ Gagal log traffic: {e}")
