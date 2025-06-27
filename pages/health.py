import streamlit as st
from app.helper_connection import connection_checker


st.set_page_config(page_title="Health Check", layout="wide")
st.title("🔧 Sistem Health Check")

st.info("Panel ini memeriksa sambungan ke Google Sheets dan Google Drive.")

status = connection_checker()

for name, stat in status.items():
    if "✅" in stat:
        st.success(f"{name}: {stat}")
    else:
        st.error(f"{name}: {stat}")

st.caption("Dibangunkan oleh MKR Dev Team")
