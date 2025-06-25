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
    kira_status_ranking,
    kira_bmi,
    kategori_bmi_asia
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

st.dataframe(
    data_peserta.set_index(
        pd.Index(range(1, len(data_peserta) + 1), name="No.")
    ),
    use_container_width=True
)

st.divider()

# === Tambah Peserta ===
st.markdown("### ➕ Tambah Peserta Baru")

with st.form("form_tambah_peserta", clear_on_submit=True):
    st.subheader("🆕 Tambah Peserta Baru")

    nama = st.text_input("Nama")
    jantina = st.selectbox("Jantina", ["Lelaki", "Perempuan"])
    jabatan = st.text_input("Jabatan")
    tinggi = st.number_input("Tinggi (cm)", min_value=100, max_value=250)
    berat_awal = st.number_input("Berat Awal (kg)", min_value=30.0, max_value=300.0)
    tarikh_timbang = st.date_input("Tarikh Timbang Berat Awal")

    # Berat terkini sama dengan berat awal semasa daftar
    berat_terkini = berat_awal

    # === Kiraan BMI dan Kategori BMI ===
    bmi = kira_bmi(berat_awal, tinggi)
    kategori = kategori_bmi_asia(bmi)

    # === Papar Hasil Kiraan ===
    st.info(f"BMI: {bmi} ({kategori})")

    submitted = st.form_submit_button("➕ Tambah Peserta")

    if submitted:
        if nama and jabatan:
            tambah_peserta_google_sheet(
                nama, jantina, jabatan, tinggi, berat_awal,
                berat_terkini, str(tarikh_timbang), bmi, kategori
            )
            st.success(f"✅ Peserta '{nama}' berjaya ditambah.")
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

    confirm = st.checkbox("⚠️ Saya ingin padam peserta ini.")

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

st.dataframe(
    data_rekod.set_index(
        pd.Index(range(1, len(data_rekod) + 1), name="No.")
    ),
    use_container_width=True
)

st.divider()

papar_footer("MKR")
