# dashboard.py (dikemaskini dengan struktur modular)
import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime
import pytz

from app.helper_data import load_data
from app.helper_logic import tambah_kiraan_peserta

# Laluan changelog
URL_CHANGELOG = "https://mdk869.github.io/Sistem-Analitik-WLC-2025/changelog2.html"

# ==== Setup Page ====
st.set_page_config(page_title="Dashboard WLC 2025", layout="wide")
st.title("📊 Dashboard Weight Loss Challenge 2025")

# ==== Papar Tarikh & Masa Terkini Berdasarkan Waktu Malaysia ====
local_tz = pytz.timezone("Asia/Kuala_Lumpur")

# ==== Muatkan data ====
df = load_data()

if not df.empty:
    df = tambah_kiraan_peserta(df)

    Kategori = st.sidebar.multiselect("Pilih Kategori", options=df["Kategori"].dropna().unique(), default=df["Kategori"].dropna().unique())
    jantina = st.sidebar.multiselect("Pilih Jantina", options=df["Jantina"].dropna().unique(), default=df["Jantina"].dropna().unique())

    df_tapis = df[(df["Kategori"].isin(Kategori)) & (df["Jantina"].isin(jantina))]

    total_peserta = df_tapis.shape[0]
    purata_bmi = df_tapis["BMI"].mean().round(1)
    purata_penurunan = df_tapis["% Penurunan"].mean().round(2)
    purata_kg = df_tapis["PenurunanKg"].mean().round(2)
else:
    st.warning("Google Sheet kosong atau tiada data.")

# Gaya CSS untuk kad metrik utama
card_style = """
<style>
.wlc-metric-box {
    background-color: #f9f9f9;
    border: 1px solid #ddd;
    padding: 1rem;
    border-radius: 10px;
    text-align: center;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
    margin-bottom: 1rem;
}
.wlc-metric-title {
    font-size: 0.95rem;
    color: #333;
    margin-bottom: 0.4rem;
}
.wlc-metric-value {
    font-size: 1.9rem;
    font-weight: bold;
    color: #0074D9;
}
@media screen and (max-width: 768px) {
    .wlc-metric-box {
        padding: 0.8rem;
    }
    .wlc-metric-title {
        font-size: 0.8rem;
    }
    .wlc-metric-value {
        font-size: 1.4rem;
    }
}
</style>
"""
st.markdown(card_style, unsafe_allow_html=True)

# Paparan metrik
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="wlc-metric-box">
        <div class="wlc-metric-title">👥 Jumlah Peserta</div>
        <div class="wlc-metric-value">{total_peserta}</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="wlc-metric-box">
        <div class="wlc-metric-title">📉 Purata BMI</div>
        <div class="wlc-metric-value">{purata_bmi}</div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="wlc-metric-box">
        <div class="wlc-metric-title">🏆 % Penurunan</div>
        <div class="wlc-metric-value">{purata_penurunan}%</div>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="wlc-metric-box">
        <div class="wlc-metric-title">⚖️ Berat Turun (kg)</div>
        <div class="wlc-metric-value">{purata_kg} kg</div>
    </div>""", unsafe_allow_html=True)

# ===== Tabs =====
tab1, tab2, tab3 = st.tabs(["📉 Penurunan Berat", "🏆 Leaderboard", "🧍‍♂️ BMI"])

with tab1:
    st.subheader("Perbandingan Berat Setiap Peserta")
    df_plot = df_tapis.sort_values("PenurunanKg", ascending=False)
    fig = px.bar(df_plot, x="Nama", y=["BeratAwal", "BeratTerkini"],
                 barmode="group", title="Perbandingan Berat Awal dan Terkini",
                 labels={"value": "Berat (kg)", "variable": "Kategori Berat"})
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("📊 Analisis BMI Peserta")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Kurang Berat Badan", (df_tapis["KategoriBMI"] == "Kurang Berat Badan").sum())
    col2.metric("Normal", (df_tapis["KategoriBMI"] == "Normal").sum())
    col3.metric("Lebih Berat Badan", (df_tapis["KategoriBMI"] == "Lebih Berat Badan").sum())
    col4.metric("Obesiti Tahap 1", (df_tapis["KategoriBMI"] == "Obesiti Tahap 1").sum())
    col5.metric("Obesiti Tahap 2", (df_tapis["KategoriBMI"] == "Obesiti Tahap 2").sum())
    col6.metric("Obesiti Morbid", (df_tapis["KategoriBMI"] == "Obesiti Morbid").sum())

    Kategori_df = df_tapis.groupby("KategoriBMI").size().reset_index(name="Bilangan")
    fig = px.pie(Kategori_df, names="KategoriBMI", values="Bilangan", title="Peratus Peserta Mengikut Tahap BMI")
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📋 Lihat Senarai Nama Peserta Mengikut Kategori BMI"):
        df_bmi_table = df_tapis[["Nama", "BMI", "KategoriBMI"]].sort_values("KategoriBMI", na_position="last").reset_index(drop=True)
        df_bmi_table.index = df_bmi_table.index + 1
        st.dataframe(df_bmi_table, use_container_width=True)

# Footer
st.markdown("---")
footer_date = datetime.now(local_tz).strftime("%d/%m/%Y")
st.markdown(f"""
<div style='font-size:15px;'>
    <strong>📊 Sistem Analitik WLC 2025</strong>
    <a href='{URL_CHANGELOG}' target='_blank' style='text-decoration:none;'>&nbsp;&nbsp;<span style='color:#1f77b4;'>v2.0</span></a><br>
    Kemaskini terakhir: {footer_date} | Dibangunkan oleh <strong>MKR</strong><br>
    &copy; 2025 Semua Hak Cipta Terpelihara
</div>
""", unsafe_allow_html=True)
