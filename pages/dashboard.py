# dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys
from datetime import datetime
import pytz

from app.styles import paparkan_tema, papar_footer, papar_header
from app.helper_data import load_data_cloud_or_local as load_data
from app.helper_logic import tambah_kiraan_peserta

from app.helper_data import (
    load_data_peserta,
    load_rekod_berat,
    get_berat_terkini,
    list_ranking_sheets,
    load_ranking_bulanan,
    simpan_ranking_bulanan
)

from app.helper_logic import (
    proses_leaderboard,
    tambah_kiraan_peserta
)

# === Setup Paparan
st.set_page_config(page_title="Dashboard WLC 2025", layout="wide")
local_tz = pytz.timezone("Asia/Kuala_Lumpur")

# === Tema & Header
st.title("📊 Dashboard Weight Loss Challenge 2025")
paparkan_tema()

# === Data ===
df = load_data()
df_peserta = load_data_peserta()
df_rekod = load_rekod_berat()

df_berat_terkini = get_berat_terkini()

# Gabungkan berat awal + berat terkini
df_merge = df_peserta.merge(df_berat_terkini, on="Nama", how="left")
df_merge.rename(columns={"Berat": "BeratTerkini", "Tarikh": "TarikhTerkini"}, inplace=True)

# Kiraan penurunan berat + BMI
df_merge = tambah_kiraan_peserta(df_merge)


if not df.empty:
    df = tambah_kiraan_peserta(df)

    Kategori = st.sidebar.multiselect("Pilih Kategori", options=df["Kategori"].dropna().unique(), default=df["Kategori"].dropna().unique())
    jantina = st.sidebar.multiselect("Pilih Jantina", options=df["Jantina"].dropna().unique(), default=df["Jantina"].dropna().unique())

    df_tapis = df[(df["Kategori"].isin(Kategori)) & (df["Jantina"].isin(jantina))]

    # === KPI
    total_peserta = df_tapis.shape[0]
    purata_bmi = df_tapis["BMI"].mean().round(1)
    purata_penurunan = df_tapis["% Penurunan"].mean().round(2)
    purata_kg = df_tapis["PenurunanKg"].mean().round(2)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("👥 Jumlah Peserta", total_peserta)
    col2.metric("📉 Purata BMI", purata_bmi)
    col3.metric("🏆 % Purata Turun", f"{purata_penurunan}%")
    col4.metric("⚖️ Kg Purata Turun", f"{purata_kg} kg")

    # === Tabs
    tab1, tab2, tab3 = st.tabs(["📉 Penurunan Berat", "🏆 Leaderboard", "🧍‍♂️ BMI"])

    # =========================
    # Tab 1: Penurunan Berat
    # =========================
    with tab1:
        st.subheader("Penurunan Berat Peserta")

        # Susun ikut % Penurunan
        df_plot = df_tapis.sort_values("% Penurunan", ascending=False)

        colA, colB = st.columns(2)

        with colA:
            st.markdown("### 🏆 Ranking % Penurunan Berat")
            fig1 = px.bar(
                df_plot,
                x="Nama",
                y="% Penurunan",
                title="% Penurunan Berat Mengikut Peserta",
                labels={"% Penurunan": "% Penurunan", "Nama": "Peserta"},
                text="% Penurunan",
            )
            fig1.update_traces(texttemplate='%{text}%', textposition='outside')
            fig1.update_layout(xaxis_tickangle=-45, yaxis_title="% Penurunan")
            st.plotly_chart(fig1, use_container_width=True)

        with colB:
            st.markdown("### ⚖️ Penurunan Berat (Kg) Mengikut Peserta")
            fig2 = px.bar(
                df_plot,
                x="Nama",
                y="PenurunanKg",
                title="Penurunan Berat (Kg) Mengikut Peserta",
                labels={"PenurunanKg": "Kg Turun", "Nama": "Peserta"},
                text="PenurunanKg",
            )
            fig2.update_traces(texttemplate='%{text} kg', textposition='outside')
            fig2.update_layout(xaxis_tickangle=-45, yaxis_title="Kg Turun")
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("### 📊 Kategori Penurunan Berat")
        # Buat kategori berdasarkan berat turun
        def kategori_penurunan(kg):
            if kg >= 5:
                return "🔺 >5 kg"
            elif 3 <= kg < 5:
                return "⬆️ 3-5 kg"
            elif 1 <= kg < 3:
                return "↗️ 1-3 kg"
            elif kg > 0:
                return "➖ <1 kg"
            else:
                return "⏸️ Tiada Perubahan"

        df_plot["Kategori Penurunan"] = df_plot["PenurunanKg"].apply(kategori_penurunan)

        kategori_counts = df_plot["Kategori Penurunan"].value_counts().reset_index()
        kategori_counts.columns = ["Kategori", "Bilangan"]

        fig3 = px.pie(
            kategori_counts,
            values="Bilangan",
            names="Kategori",
            title="Peratusan Peserta Mengikut Kategori Penurunan Berat",
        )
        st.plotly_chart(fig3, use_container_width=True)

        with st.expander("📄 Lihat Senarai Penuh"):
            df_senarai = df_plot[["Nama", "PenurunanKg", "% Penurunan", "Kategori Penurunan"]]
            df_senarai = df_senarai.reset_index(drop=True)
            df_senarai.index = df_senarai.index + 1
            st.dataframe(df_senarai, use_container_width=True)

    # =========================
    # Tab 2: Leaderboard
    # =========================
    with tab2:
        st.subheader("🏆 Leaderboard dengan History Trend")

        # Load ranking history jika ada
        ranking_sheets = list_ranking_sheets()
        if ranking_sheets:
            pilihan_bulan = st.selectbox(
                "Pilih Ranking Sebelum (Bulan)",
                [s.split('_')[1] for s in ranking_sheets]
            )
            df_ranking_sebelum = load_ranking_bulanan(pilihan_bulan)
        else:
            df_ranking_sebelum = None

        # Proses leaderboard semasa
        df_rank = proses_leaderboard(df_merge, df_ranking_sebelum)

        # Pilihan jumlah Top Ranking
        top_n = st.selectbox("Pilih jumlah Top Ranking:", [5, 10, 20, 50], index=1)

        # Papar leaderboard
        st.dataframe(
            df_rank.head(top_n)[["Ranking_Trend", "Nama", "% Penurunan"]],
            use_container_width=True,
            hide_index=True
        )

        # Butang simpan ranking
        if st.button("💾 Simpan Ranking Terkini Bulan Ini"):
            df_simpan = df_rank[["Ranking", "Nama", "% Penurunan"]]
            simpan_ranking_bulanan(df_simpan)

    with tab3:
        st.subheader("📊 Analisis BMI Peserta")

        kategori_bmi_data = [
            ("Kurang Berat Badan", (df_tapis["KategoriBMI"] == "Kurang Berat Badan").sum()),
            ("Normal", (df_tapis["KategoriBMI"] == "Normal").sum()),
            ("Lebih Berat Badan", (df_tapis["KategoriBMI"] == "Lebih Berat Badan").sum()),
            ("Obesiti Tahap 1", (df_tapis["KategoriBMI"] == "Obesiti Tahap 1").sum()),
            ("Obesiti Tahap 2", (df_tapis["KategoriBMI"] == "Obesiti Tahap 2").sum()),
            ("Obesiti Morbid", (df_tapis["KategoriBMI"] == "Obesiti Morbid").sum()),
        ]

        col_bmi = st.columns(6)

        for col, (label, value) in zip(col_bmi, kategori_bmi_data):
            col.metric(label, value)

        kategori_bmi_df = df_tapis.groupby("KategoriBMI").size().reset_index(name="Bilangan")
        fig_bmi = px.pie(
            kategori_bmi_df,
            names="KategoriBMI",
            values="Bilangan",
            title="Peratus Peserta Mengikut Tahap BMI"
        )
        st.plotly_chart(fig_bmi, use_container_width=True)

        with st.expander("📋 Lihat Senarai Nama Peserta Mengikut Kategori BMI"):
            df_bmi_table = df_tapis[["Nama", "BMI", "KategoriBMI"]].sort_values("KategoriBMI").reset_index(drop=True)
            df_bmi_table.index = df_bmi_table.index + 1
            st.dataframe(df_bmi_table, use_container_width=True)

else:
    st.warning("Google Sheet kosong atau tiada data.")

# === Footer
footer_date = datetime.now(local_tz).strftime("%d/%m/%Y")
papar_footer("MKR", footer_date)
