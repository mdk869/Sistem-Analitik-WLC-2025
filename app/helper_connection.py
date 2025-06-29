import gspread
from google.oauth2.service_account import Credentials
import streamlit as st


scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credentials = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

conn = gspread.authorize(credentials)
