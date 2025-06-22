# admin.py
import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

from app.styles import paparkan_tema, papar_footer, papar_header
from app.helper_auth import check_login
from app.helper_data import (
    load_data_cloud_or_local,
    tambah_peserta_google_sheet,
    kemaskini_berat_peserta,
    padam_peserta_dari_sheet,
    sejarah_berat
)
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

# === Data Semasa ===
df = load_data_cloud_or_local()

# === Tambah/Edit/Padam Peserta ===
st.subheader("👤 Pengurusan Peserta")

with st.expander("➕ Tambah Peserta Baru"):
    with st.form("form_tambah"):
        nama = st.text_input("Nama")
        nostaf = st.text_input("No Staf")
        umur = st.number_input("Umur", min_value=10, max_value=100, step=1)
        jantina = st.selectbox("Jantina", ["Lelaki", "Perempuan"])
        jabatan = st.text_input("Jabatan/Unit")
        tinggi = st.number_input("Tinggi (cm)", min_value=100.0, max_value=250.0, step=0.1)
        berat_awal = st.number_input("Berat Awal (kg)", min_value=30.0, max_value=200.0, step=0.1)

    if st.form_submit_button("Tambah Peserta"):
        if nama and nostaf:
            tinggi_meter = tinggi / 100
            bmi = kira_bmi(berat_awal, tinggi_meter)
            kategori = kategori_bmi_asia(bmi)
            berat_terkini = berat_awal
            tarikh_timbang = datetime.now(local_tz).strftime("%Y-%m-%d")
        
            tambah_peserta_google_sheet(
                nama, nostaf, umur, jantina, jabatan,
                tinggi, berat_awal, berat_terkini,
                tarikh_timbang, bmi, kategori
            )
            st.success("✅ Peserta berjaya ditambah!")
        else:
            st.error("❌ Sila lengkapkan semua maklumat!")


with st.expander("✏️ Edit & Padam Peserta"):
    peserta_list = df["Nama"].dropna().unique()
    nama_dipilih = st.selectbox("Pilih Peserta", peserta_list)
    if nama_dipilih:
        kol1, kol2 = st.columns(2)
        with kol1:
            new_berat = st.number_input("Kemaskini Berat (kg)", value=float(df[df["Nama"] == nama_dipilih]["BeratTerkini"].values[0]))
            if st.button("✅ Kemaskini Berat"):
                kemaskini_berat_peserta(nama_dipilih, new_berat)
                st.success("✅ Berat peserta berjaya dikemaskini!")
        with kol2:
            if st.button("🗑️ Padam Peserta"):
                padam_peserta_dari_sheet(nama_dipilih)
                st.warning("⚠️ Peserta telah dipadam.")

# === Paparan Sejarah Berat ===
st.subheader("📊 Sejarah Berat Peserta")
nama_dipilih2 = st.selectbox("Pilih Peserta untuk Sejarah Berat", df["Nama"].dropna().unique(), key="pilih_sejarah")
if nama_dipilih2:
    df_sejarah = sejarah_berat(nama_dipilih2)
    if not df_sejarah.empty:
        st.line_chart(df_sejarah.set_index("Tarikh")["Berat"])
    else:
        st.info("ℹ️ Tiada data sejarah berat untuk peserta ini.")

# === Paparan Jadual Peserta ===
st.subheader("📋 Senarai Peserta")
df_view = df.copy().reset_index(drop=True)
df_view.index += 1
st.dataframe(df_view, use_container_width=True)

# === Footer ===
footer_date = datetime.now(local_tz).strftime("%d/%m/%Y")
papar_footer("MKR", footer_date)
