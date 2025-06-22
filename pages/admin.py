# admin.py
import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime
import pytz

from app.styles import paparkan_tema, papar_footer, papar_header
from app.helper_auth import check_login
from app.helper_data import (
    load_data_cloud_or_local,
    save_ranking_to_excel,
    upload_file_to_drive,
    tambah_peserta_google_sheet,
    kemaskini_berat_peserta,
    padam_peserta_dari_sheet
)
from app.helper_logic import (
    kira_bmi,
    kategori_bmi_asia,
    tambah_kiraan_peserta,
    kira_status_ranking
)

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

# === Tambah/Edit/Padam Peserta ===
st.subheader("👤 Pengurusan Peserta")
with st.expander("➕ Tambah Peserta Baru"):
    with st.form("form_tambah"):
        nama = st.text_input("Nama")
        nostaf = st.text_input("No Staf")
        tinggi = st.number_input("Tinggi (cm)", min_value=100.0, max_value=250.0, step=0.1)
        berat_awal = st.number_input("Berat Awal (kg)", min_value=30.0, max_value=200.0, step=0.1)
        if st.form_submit_button("Tambah Peserta"):
            if nama and nostaf:
                tambah_peserta_google_sheet(nama, nostaf, tinggi, berat_awal)
                st.success("Peserta berjaya ditambah!")
            else:
                st.error("Sila lengkapkan semua maklumat!")

with st.expander("✏️ Edit & Padam Peserta"):
    peserta_list = df["Nama"].dropna().unique()
    nama_dipilih = st.selectbox("Pilih Peserta", peserta_list)
    if nama_dipilih:
        kol1, kol2 = st.columns(2)
        with kol1:
            new_berat = st.number_input("Kemaskini Berat (kg)", value=float(df[df["Nama"] == nama_dipilih]["BeratTerkini"].values[0]))
            if st.button("✅ Kemaskini Berat"):
                kemaskini_berat_peserta(nama_dipilih, new_berat)
                st.success("Berat peserta berjaya dikemaskini!")
        with kol2:
            if st.button("🗑️ Padam Peserta"):
                padam_peserta_dari_sheet(nama_dipilih)
                st.warning("Peserta dipadam dari senarai!")

# === Leaderboard ===
st.subheader("🏆 Leaderboard Semasa")
df = tambah_kiraan_peserta(df)
df_leaderboard = df.sort_values("% Penurunan", ascending=False).reset_index(drop=True)
df_leaderboard["Ranking"] = df_leaderboard.index + 1

sheet_id_ranking = "1K9JiK8FE1-Cd9fYnDU8Pzqj42TWOGi10wHzHt0avbJ0"
gid_ranking = "0"
url_ranking = f"https://docs.google.com/spreadsheets/d/{sheet_id_ranking}/export?format=csv&gid={gid_ranking}"

try:
    df_ranking_lama = pd.read_csv(url_ranking)
    if not df_ranking_lama.empty:
        df_leaderboard = df_leaderboard.merge(df_ranking_lama, on="Nama", how="left", suffixes=("", "_Lama"))
        df_leaderboard["Status"] = df_leaderboard.apply(lambda row: kira_status_ranking(row["BeratAwal"], row["BeratTerkini"]), axis=1)
    else:
        df_leaderboard["Status"] = "-"
except:
    df_leaderboard["Status"] = "-"

st.dataframe(df_leaderboard[["Ranking", "Nama", "% Penurunan", "Status"]], use_container_width=True)

if st.button("💾 Simpan Ranking Semasa"):
    rekod_df = df_leaderboard[["Nama", "Ranking"]]
    save_ranking_to_excel(rekod_df)
    st.success("✅ Ranking disimpan dan dimuat naik.")

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

    try:
        gid_berat = "987654321"
        url_rekod_berat = f"https://docs.google.com/spreadsheets/d/{sheet_id_ranking}/export?format=csv&gid={gid_berat}"
        df_rekod = pd.read_csv(url_rekod_berat)
        df_sejarah = df_rekod[df_rekod["Nama"] == nama_dicari]
        if not df_sejarah.empty:
            df_sejarah["Tarikh"] = pd.to_datetime(df_sejarah["Tarikh"], dayfirst=True)
            st.line_chart(df_sejarah.set_index("Tarikh")["Berat"])
    except:
        st.warning("⚠️ Tiada rekod sejarah peserta.")

# === Statistik Ringkas ===
st.subheader("📈 Statistik Ringkas")
total_peserta = df.shape[0]
purata_bmi = df["BMI"].mean().round(1)
purata_penurunan = df["% Penurunan"].mean().round(2)

col1, col2, col3 = st.columns(3)
col1.markdown(f"<div class='metric-box'><div class='metric-value'>{total_peserta}</div>Peserta Aktif</div>", unsafe_allow_html=True)
col2.markdown(f"<div class='metric-box'><div class='metric-value'>{purata_bmi}</div>Purata BMI</div>", unsafe_allow_html=True)
col3.markdown(f"<div class='metric-box'><div class='metric-value'>{purata_penurunan}%</div>Purata Penurunan</div>", unsafe_allow_html=True)

# === Footer ===
footer_date = datetime.now(local_tz).strftime("%d/%m/%Y")
papar_footer("MKR", footer_date)
