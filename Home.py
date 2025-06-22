# Home.py
import streamlit as st
from app.styles import paparkan_tema, papar_tajuk_utama, papar_kandungan_home, papar_header, papar_footer

# === Setup Paparan ===
st.set_page_config(
    page_title="Sistem Analitik WLC 2025",
    page_icon="📊",
    layout="wide"
)

# === Tema dan Kandungan ===
paparkan_tema()
papar_tajuk_utama()
papar_kandungan_home()
papar_footer("MKR")
