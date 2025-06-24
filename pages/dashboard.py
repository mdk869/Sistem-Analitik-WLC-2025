# dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime
import pytz

from app.styles import paparkan_tema, papar_footer, papar_header
from app.helper_data import load_data_cloud_or_local as load_data
from app.helper_logic import tambah_kiraan_peserta

# === Setup Paparan ===
st.set_page_config(page_title="Dashboard WLC 2025", layout="wide")
local_tz = pytz.timezone("Asia/Kuala_Lumpur")

# === Tema & Header ===
st.set_page_config(page_title="Dashboard WLC 2025", layout="wide")
st.title("📊 Dashboard Weight Loss Challenge 2025")
paparkan_tema()

# === Data ===
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

    # Paparan metrik
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="wlc-box">
            <div class="wlc-sub-title">👥 Jumlah Peserta</div>
            <div class="wlc-value">{total_peserta}</div>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="wlc-box">
            <div class="wlc-sub-title">📉 Purata BMI</div>
            <div class="wlc-value">{purata_bmi}</div>
        </div>""", unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="wlc-box">
            <div class="wlc-sub-title">🏆 % Penurunan</div>
            <div class="wlc-value">{purata_penurunan}%</div>
        </div>""", unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="wlc-box">
            <div class="wlc-sub-title">⚖️ Berat Turun (kg)</div>
            <div class="wlc-value">{purata_kg} kg</div>
        </div>""", unsafe_allow_html=True)

    # Tabs
    tab1, tab2, tab3 = st.tabs(["📉 Penurunan Berat", "🏆 Leaderboard", "🧍‍♂️ BMI"])

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

    with tab2:
        st.subheader("Leaderboard")
        #Susun berdasarkan % Penurunan
        df_rank = df_tapis.sort_values("% Penurunan", ascending=False).reset_index(drop=True)
        #Tambah kolum Ranking
        df_rank["Ranking"] = df_rank.index + 1
        #Tambah label medal untuk Top 3
        def add_medal(rank):
            if rank == 1:
                return "🥇"
            elif rank == 2:
                return "🥈"
            elif rank == 3:
                return "🥉"
            else:
                return str(rank)

        df_rank["Ranking"] = df_rank["Ranking"].apply(add_medal)
        # Pilihan berapa Top Ranking nak tunjuk
        top_n = st.selectbox("Pilih jumlah Top Ranking:", [5, 10, 20, 50], index=1)
        # Paparkan leaderboard
        st.dataframe(df_rank[["Ranking", "Nama", "% Penurunan"]], use_container_width=True, hide_index=True)

        st.subheader("🏅 10 Terbaik - % Penurunan Berat")
        top10 = df_rank.head(10)
        fig_top10 = px.bar(top10, x="Nama", y="% Penurunan",
                       title="Top 10 Peserta Berdasarkan % Penurunan Berat",
                       labels={"% Penurunan": "% Turun"},
                       color="% Penurunan", color_continuous_scale="Blues")
        st.plotly_chart(fig_top10, use_container_width=True)


    with tab3:
        st.subheader("📊 Analisis BMI Peserta")
        col1, col2, col3, col4, col5, col6 = st.columns(6)

        # Paparan metrik kategori BMI dengan gaya mengikut warna
        cols = st.columns(6)
        kategori_bmi_data = [
            ("Kurang Berat Badan", "kurang", (df_tapis["KategoriBMI"] == "Kurang Berat Badan").sum()),
            ("Normal", "normal", (df_tapis["KategoriBMI"] == "Normal").sum()),
            ("Lebih Berat Badan", "lebih", (df_tapis["KategoriBMI"] == "Lebih Berat Badan").sum()),
            ("Obesiti Tahap 1", "obes1", (df_tapis["KategoriBMI"] == "Obesiti Tahap 1").sum()),
            ("Obesiti Tahap 2", "obes2", (df_tapis["KategoriBMI"] == "Obesiti Tahap 2").sum()),
            ("Obesiti Morbid", "morbid", (df_tapis["KategoriBMI"] == "Obesiti Morbid").sum()),
        ]

        for col, (label, css_class, value) in zip(cols, kategori_bmi_data):
            col.markdown(f"""
            <div class="bmi-box {css_class}">
                <div class="bmi-title">{label}</div>
                <div class="bmi-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)

        Kategori_df = df_tapis.groupby("KategoriBMI").size().reset_index(name="Bilangan")
        fig = px.pie(Kategori_df, names="KategoriBMI", values="Bilangan", title="Peratus Peserta Mengikut Tahap BMI")
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("📋 Lihat Senarai Nama Peserta Mengikut Kategori BMI"):
            df_bmi_table = df_tapis[["Nama", "BMI", "KategoriBMI"]].sort_values("KategoriBMI", na_position="last").reset_index(drop=True)
            df_bmi_table.index = df_bmi_table.index + 1
            st.dataframe(df_bmi_table, use_container_width=True)
else:
    st.warning("Google Sheet kosong atau tiada data.")

# === Footer ===
footer_date = datetime.now(local_tz).strftime("%d/%m/%Y")
papar_footer("MKR", footer_date)