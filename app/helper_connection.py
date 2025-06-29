import gspread
from google.oauth2.service_account import Credentials
import streamlit as st
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# ===============================
# ✅ Setup Connection Google
# ===============================
def connect_gspread():
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ],
    )
    client = gspread.authorize(creds)
    return client

def connect_drive():
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=["https://www.googleapis.com/auth/drive"],
    )
    service = build("drive", "v3", credentials=creds)
    return service
