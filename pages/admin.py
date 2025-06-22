# admin.py (Simple Version)
import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

from app.styles import paparkan_tema, papar_footer, papar_header
from app.helper_auth import check_login
from app.helper_data import load_data_cloud_or_local
from app.helper_logic import kira_bmi, kategori_bmi_asia

# === Setup Paparan ===
st.set_page_config(page_title="Admin Panel", layout="wide")
local_tz = pytz.timezone("Asia/Kuala_Lumpur")

# === Tema & Header ===
paparkan_tema()
papar_header("🔐 Admin Panel - WLC 2025")

# === Login ===
if not check_login():
    st.stop()

# === Data ===
df = load_data_cloud_or_local()

# === Ringkasan Peserta ===
st.subheader("📋 Senarai Peserta")
st.dataframe(df, use_container_width=True)

# === Carian Individu ===
st.subheader("🔍 Carian Peserta")
nama_dicari = st.selectbox("Pilih Peserta", df["Nama"].dropna().unique())
if nama_dicari:
    peserta = df[df["Nama"] == nama_dicari].iloc[0]
    st.markdown(f"**Nama:** {nama_dicari}")
    st.markdown(f"**Tinggi:** {peserta['Tinggi']} cm")
    st.markdown(f"**Berat Terkini:** {peserta['BeratTerkini']} kg")
    bmi = kira_bmi(peserta['BeratTerkini'], peserta['Tinggi'])
    st.markdown(f"**BMI:** {bmi}")
    st.markdown(f"**Kategori BMI:** {kategori_bmi_asia(bmi)}")

# === Statistik Ringkas ===
st.subheader("📈 Statistik Ringkas")
total_peserta = df.shape[0]
purata_bmi = df["BMI"].mean().round(1) if "BMI" in df.columns else 0
col1, col2 = st.columns(2)
col1.metric("Peserta Aktif", total_peserta)
col2.metric("Purata BMI", purata_bmi)

# === Footer ===
footer_date = datetime.now(local_tz).strftime("%d/%m/%Y")
papar_footer("MKR", footer_date)