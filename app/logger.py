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
        res = requests.get("https://ipinfo.io/json").json()
        ip = res.get("ip", "Unknown")
        location = f"{res.get('city', '')}, {res.get('region', '')}".strip(', ')
        org = res.get("org", "Unknown")
    except:
        ip, location, org = "Unknown", "Unknown", "Unknown"

    user_agent = st.session_state.get("user_agent", "Unknown")
    return ip, location, org, user_agent

# =========================================
# ✅ Log Traffic to Google Sheet
# =========================================
def log_traffic_to_sheet():
    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]

        # Credentials
        creds_dict = st.secrets["gcp_service_account"]
        creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)

        # Sheet Info
        sheet_id = st.secrets["gsheet"]["log_wlc_dev_id"]
        spreadsheet = client.open_by_key(sheet_id)

        try:
            sheet = spreadsheet.worksheet("LogTraffic")
        except gspread.exceptions.WorksheetNotFound:
            sheet = spreadsheet.add_worksheet(title="LogTraffic", rows="1000", cols="5")
            sheet.append_row(["Timestamp", "IP", "Location", "Org", "User Agent"])

        # Visitor Info
        ip, location, org, user_agent = get_visitor_info()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Log to Sheet
        sheet.append_row([timestamp, ip, location, org, user_agent])

    except Exception as e:
        st.warning(f"❌ Gagal log traffic: {e}")
