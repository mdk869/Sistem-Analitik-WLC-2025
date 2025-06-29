import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


def connect_gspread():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scopes
    )
    client = gspread.authorize(creds)
    return client


def connect_drive_service():
    scopes = [
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scopes
    )
    service = build('drive', 'v3', credentials=creds)
    return service
