# widgets_admin.py

import streamlit as st
import pandas as pd
from admin_core import (
    proses_tambah_peserta,
    proses_kemaskini_peserta,
    proses_padam_peserta,
    dapatkan_senarai_peserta
)


# ========== 1. Tambah Peserta ==========

def borang_tambah_peserta():
    st.subheader("➕ Tambah Peserta Baru")

    with st.form("form_tambah"):
        nama = st.text_input("Nama Penuh")
        no_staf = st.text_input("No Staf")
        jantina = st.selectbox("Jantina", ["Lelaki", "Perempuan"])
        tinggi = st.number_input("Tinggi (cm)", min_value=100, max_value=250, step=1)
        berat = st.number_input("Berat Awal (kg)", min_value=30.0, max_value=250.0, step=0.1)
        hantar = st.form_submit_button("Tambah")

        if hantar:
            if not nama or not no_staf:
                st.warning("Sila isi semua maklumat.")
                return

            data = {
                "Nama": nama.strip(),
                "No Staf": no_staf.strip(),
                "Jantina": jantina,
                "Tinggi": tinggi,
                "Berat Awal": berat
            }
            peserta = proses_tambah_peserta(data)
            st.success(f"✅ Peserta {peserta['Nama']} berjaya ditambah.")


# ========== 2. Edit Peserta ==========

def borang_edit_peserta():
    st.subheader("✏️ Kemaskini Maklumat Peserta")
    df = dapatkan_senarai_peserta()

    peserta_list = df["No Staf"] + " - " + df["Nama"]
    pilihan = st.selectbox("Pilih Peserta", peserta_list)

    if pilihan:
        no_staf = pilihan.split(" - ")[0]
        data_peserta = df[df["No Staf"] == no_staf].iloc[0]

        with st.form("form_edit"):
            nama = st.text_input("Nama Penuh", data_peserta["Nama"])
            jantina = st.selectbox("Jantina", ["Lelaki", "Perempuan"], index=0 if data_peserta["Jantina"] == "Lelaki" else 1)
            tinggi = st.number_input("Tinggi (cm)", value=int(data_peserta["Tinggi"]), step=1)
            berat = st.number_input("Berat Awal (kg)", value=float(data_peserta["Berat Awal"]), step=0.1)
            hantar = st.form_submit_button("Kemaskini")

            if hantar:
                data_kemaskini = {
                    "Nama": nama.strip(),
                    "Jantina": jantina,
                    "Tinggi": tinggi,
                    "Berat Awal": berat
                }
                berjaya = proses_kemaskini_peserta(no_staf, data_kemaskini)
                if berjaya:
                    st.success(f"✅ Maklumat peserta {nama} dikemaskini.")
                else:
                    st.error("❌ Gagal kemaskini.")


# ========== 3. Padam Peserta ==========

def borang_padam_peserta():
    st.subheader("🗑️ Padam Peserta")
    df = dapatkan_senarai_peserta()

    peserta_list = df["No Staf"] + " - " + df["Nama"]
    pilihan = st.selectbox("Pilih Peserta untuk Padam", peserta_list)

    if pilihan:
        no_staf, nama = pilihan.split(" - ")
        confirm = st.button(f"Padam {nama}?")

        if confirm:
            proses_padam_peserta(no_staf)
            st.success(f"✅ Peserta {nama} telah dipadam.")


# ========== 4. Paparan Senarai ==========

def papar_senarai_peserta():
    st.subheader("👥 Senarai Semua Peserta")
    df = dapatkan_senarai_peserta()
    st.dataframe(df, use_container_width=True)


# ========== 5. Statistik Mini ==========

def paparan_statistik_mini():
    df = dapatkan_senarai_peserta()
    total = len(df)
    lelaki = len(df[df["Jantina"] == "Lelaki"])
    perempuan = len(df[df["Jantina"] == "Perempuan"])
    purata_bmi = round(df["BMI"].astype(float).mean(), 2)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Peserta", total)
    col2.metric("Lelaki", lelaki)
    col3.metric("Perempuan", perempuan)
    col4.metric("BMI Purata", purata_bmi)
