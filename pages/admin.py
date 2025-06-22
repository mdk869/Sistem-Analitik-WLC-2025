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
    upload_file_to_drive
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

# === Leaderboard ===
st.subheader("🏆 Leaderboard Semasa")
df["PenurunanKg"] = df["BeratAwal"] - df["BeratTerkini"]
df["% Penurunan"] = (df["PenurunanKg"] / df["BeratAwal"] * 100).round(2)
df_leaderboard = df.sort_values("% Penurunan", ascending=False).reset_index(drop=True)
df_leaderboard["Ranking"] = df_leaderboard.index + 1

SHEET_ID = "1K9JiK8FE1-Cd9fYnDU8Pzqj42TWOGi10wHzHt0avbJ0"
GID_REKOD_RANKING = "1930381739"  # contoh gid, pastikan betul
df_ranking_lama = None
try:
    df_ranking_lama = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID_REKOD_RANKING}")
except:
    pass

if df_ranking_lama is not None and not df_ranking_lama.empty:
    df_leaderboard = df_leaderboard.merge(df_ranking_lama, on="Nama", how="left", suffixes=("", "_Lama"))
    df_leaderboard["Status"] = df_leaderboard.apply(kira_status_ranking, axis=1)
else:
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
        GID_REKOD_BERAT = "987654321"  # contoh gid, pastikan betul
        df_rekod = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID_REKOD_BERAT}")
        df_sejarah = df_rekod[df_rekod["Nama"] == nama_dicari]
        if not df_sejarah.empty:
            df_sejarah["Tarikh"] = pd.to_datetime(df_sejarah["Tarikh"], dayfirst=True)
            st.line_chart(df_sejarah.set_index("Tarikh")["Berat"])
    except:
        st.warning("⚠️ Tiada rekod sejarah peserta.")

# === Export Data ===
st.subheader("🗃️ Export & Backup")
col1, col2 = st.columns(2)

with col1:
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0)
    st.download_button("⬇️ Muat Turun Data Peserta", excel_buffer, file_name="data_peserta.xlsx")

    try:
        df_rekod_berat = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID_REKOD_BERAT}")
        rekod_buffer = io.BytesIO()
        df_rekod_berat.to_excel(rekod_buffer, index=False)
        rekod_buffer.seek(0)
        st.download_button("⬇️ Muat Turun Rekod Berat", rekod_buffer, file_name="rekod_berat.xlsx")
    except:
        st.warning("⚠️ Tiada rekod berat untuk dimuat turun.")

with col2:
    if st.button("📦 Backup Semua ke Google Drive"):
        st.info("✅ Google Sheet digunakan — backup automatik tidak diperlukan.")

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
