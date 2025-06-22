# Home.py
import streamlit as st
from datetime import datetime
import pytz

from app.styles import paparkan_tema, papar_footer, papar_tajuk_utama, papar_kandungan_home

# === Setup Paparan ===
st.set_page_config(
    page_title="Sistem Analitik WLC 2025",
    page_icon="📊",
    layout="wide"
)

# === Paparkan Tema dan Tajuk ===
paparkan_tema()
papar_tajuk_utama()
papar_kandungan_home()

# === Navigasi Sidebar ===
with st.sidebar:
    st.header("📁 Navigasi")

    if st.button("🔐 Admin Panel"):
        st.switch_page("pages/admin.py")

    if st.button("📈 Dashboard"):
        st.switch_page("pages/dashboard.py")


# === Footer ===
local_tz = pytz.timezone("Asia/Kuala_Lumpur")
footer_date = datetime.now(local_tz).strftime("%d/%m/%Y")
papar_footer("MKR", footer_date)