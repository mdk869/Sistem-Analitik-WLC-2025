import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

from app.helper_data import (
    load_data_peserta,
    load_data_cloud_or_local,
    tambah_peserta_google_sheet,
    kemaskini_berat_peserta,
    padam_peserta_dari_sheet
)

from app.helper_logic import (
    tambah_kiraan_peserta,
    kira_status_ranking
)

from app.styles import paparkan_tema, papar_header, papar_footer

paparkan_tema()
papar_header("Admin Panel | WLC 2025")

st.subheader("🔧 Pengurusan Peserta")

# === Load Data ===
data_peserta = load_data_peserta()
data_rekod = load_data_cloud_or_local()

# === Papar Senarai Peserta ===
st.markdown("### 📋 Senarai Peserta")
st.dataframe(data_peserta, use_container_width=True)

st.divider()

# === Tambah Peserta ===
st.markdown("### ➕ Tambah Peserta Baru")

with st.form("form_tambah_peserta"):
    nama_baru = st.text_input("Nama Peserta")
    no_staf_baru = st.text_input("No. Staf")
    berat_awal = st.number_input("Berat Awal (kg)", min_value=20.0, max_value=300.0, step=0.1)
    submit_tambah = st.form_submit_button("✅ Tambah Peserta")

    if submit_tambah:
        if nama_baru and no_staf_baru:
            tambah_peserta_google_sheet(nama_baru, no_staf_baru, berat_awal)
            st.success(f"✅ {nama_baru} berjaya ditambah.")
            st.rerun()
        else:
            st.warning("⚠️ Sila isi semua maklumat peserta.")

st.divider()

# === Kemaskini Berat ===
st.markdown("### ⚖️ Kemaskini Berat Terkini")

if len(data_peserta) > 0:
    nama_list = data_peserta["Nama"].tolist()
    nama_dipilih = st.selectbox("Pilih Nama", nama_list)
    berat_baru = st.number_input("Masukkan Berat Terkini (kg)", min_value=20.0, max_value=300.0, step=0.1)

    if st.button("💾 Simpan Berat Terkini"):
        kemaskini_berat_peserta(nama_dipilih, berat_baru)
        st.success(f"✅ Berat {nama_dipilih} berjaya dikemaskini!")
        st.rerun()
else:
    st.info("🚫 Tiada peserta dalam senarai.")

st.divider()

# === Padam Peserta ===
st.markdown("### 🗑️ Padam Peserta")

if len(data_peserta) > 0:
    nama_list = data_peserta["Nama"].tolist()
    nama_dipilih = st.selectbox("Pilih Nama untuk Dipadam", nama_list, key="padam")

    confirm = st.checkbox("⚠️ Saya benar-benar ingin padam peserta ini.")

    if st.button("🗑️ Padam Peserta"):
        if confirm:
            berjaya = padam_peserta_dari_sheet(nama_dipilih)
            if berjaya:
                st.success(f"✅ {nama_dipilih} telah dipadam dari Google Sheet.")
                st.rerun()
            else:
                st.warning("⚠️ Nama tidak dijumpai atau berlaku ralat.")
        else:
            st.info("👉 Tandakan kotak pengesahan sebelum padam.")
else:
    st.info("🚫 Tiada peserta untuk dipadam.")

st.divider()

# === Papar Sejarah Rekod Berat ===
st.markdown("### 🗂️ Sejarah Rekod Berat")
st.dataframe(data_rekod, use_container_width=True)

papar_footer()
