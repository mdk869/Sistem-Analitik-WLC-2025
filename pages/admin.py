# admin.py
import streamlit as st
import pandas as pd
import io
from datetime import datetime
import pytz

from app.styles import paparkan_tema, papar_footer, papar_header
from app.helper_auth import check_login
from app.helper_logic import (
    kira_bmi,
    kategori_bmi_asia,
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

# === Google Sheet Setup ===
sheet_id = "1K9JiK8FE1-Cd9fYnDU8Pzqj42TWOGi10wHzHt0avbJ0"
gid_peserta = "0"            # GID untuk tab "peserta"
gid_rekod_berat = "123456789"  # GID sebenar untuk tab "rekod_berat" (update manual jika tahu)
gid_ranking_lama = "987654321"  # GID sebenar untuk tab "ranking" (update manual jika tahu)

# === Data Peserta ===
url_peserta = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid_peserta}"
df = pd.read_csv(url_peserta)
df["PenurunanKg"] = df["BeratAwal"] - df["BeratTerkini"]
df["% Penurunan"] = (df["PenurunanKg"] / df["BeratAwal"] * 100).round(2)
df["BMI"] = df.apply(lambda row: kira_bmi(row["BeratTerkini"], row["Tinggi"]), axis=1)
df["Kategori"] = df["BMI"].apply(kategori_bmi_asia)

# === Leaderboard ===
st.subheader("🏆 Leaderboard Semasa")
df_leaderboard = df.sort_values("% Penurunan", ascending=False).reset_index(drop=True)
df_leaderboard["Ranking"] = df_leaderboard.index + 1

try:
    url_ranking = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid_ranking_lama}"
    df_ranking_lama = pd.read_csv(url_ranking)
    if not df_ranking_lama.empty:
        df_leaderboard = df_leaderboard.merge(df_ranking_lama, on="Nama", how="left", suffixes=("", "_Lama"))
        df_leaderboard["Status"] = df_leaderboard.apply(lambda row: kira_status_ranking(row["BeratAwal"], row["BeratTerkini"]), axis=1)
    else:
        df_leaderboard["Status"] = "-"
except:
    df_leaderboard["Status"] = "-"

st.dataframe(df_leaderboard[["Ranking", "Nama", "% Penurunan", "Status"]], use_container_width=True)

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
        url_rekod_berat = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid_rekod_berat}"
        df_rekod = pd.read_csv(url_rekod_berat)
        df_sejarah = df_rekod[df_rekod["Nama"] == nama_dicari]
        if not df_sejarah.empty:
            df_sejarah["Tarikh"] = pd.to_datetime(df_sejarah["Tarikh"], dayfirst=True)
            st.line_chart(df_sejarah.set_index("Tarikh")["Berat"])
    except:
        st.warning("⚠️ Tiada rekod sejarah peserta.")

# === Export Data ===
st.subheader("🗃️ Export")
excel_buffer = io.BytesIO()
df.to_excel(excel_buffer, index=False)
excel_buffer.seek(0)
st.download_button("⬇️ Muat Turun Data Peserta", excel_buffer, file_name="data_peserta.xlsx")

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
