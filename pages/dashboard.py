# dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime
import pytz

from app.helper_auth import check_login
from app.styles import paparkan_tema, papar_footer, papar_header
from app.helper_data import load_data_cloud_or_local as load_data
from app.helper_logic import tambah_kiraan_peserta, proses_leaderboard

# ✅ Login check
is_admin = check_login()

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
    tab1, tab2, tab3 = st.tabs(["📊 Info Program", "🏆 Leaderboard", "🧍‍♂️ BMI"])

    with tab1:
        st.subheader("Info Program & Perkembangan Peserta")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Jumlah Peserta", len(df_tapis))
        with col2:
            st.metric("Tarikh Mula", "18 Mei 2025")
        with col3:
            st.metric("Tarikh Timbang Seterusnya", "20 Julai 2025")

        st.warning("📅 Sila bersedia untuk sesi timbangan seterusnya pada **20 Julai 2025.**")

        st.divider()

    with st.expander("📋 Aktiviti Timbang / Progres Timbang", expanded=True):
        st.subheader("📈 Statistik Progres Timbang Peserta")

        # === Kiraan Statistik Timbangan ===
        total_peserta = df.shape[0]
        sudah_timbang = df["TarikhTimbang"].notna().sum()
        belum_timbang = total_peserta - sudah_timbang

        peratus_sudah = (sudah_timbang / total_peserta * 100).round(1) if total_peserta != 0 else 0
        peratus_belum = (belum_timbang / total_peserta * 100).round(1) if total_peserta != 0 else 0

        # === Paparan Metrik ===
        col1, col2, col3 = st.columns(3)
        col1.metric("👥 Jumlah Peserta", total_peserta)
        col2.metric("✅ Sudah Timbang", f"{sudah_timbang} ({peratus_sudah}%)")
        col3.metric("❌ Belum Timbang", f"{belum_timbang} ({peratus_belum}%)")

        st.divider()

        # === Carta Pie ===
        df_status = pd.DataFrame({
            "Status": ["Sudah Timbang", "Belum Timbang"],
            "Bilangan": [sudah_timbang, belum_timbang]
        })

        fig = px.pie(df_status, names="Status", values="Bilangan",
                    title="Status Timbangan Peserta",
                    color_discrete_sequence=["#00cc96", "#EF553B"],
                    hole=0.4)  # Pie separuh donat

        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # === Senarai Peserta Belum Timbang ===
        st.subheader("📋 Senarai Peserta Belum Timbang")
        df_belum = df[df["TarikhTimbang"].isna()][["Nama", "NoStaf", "Jabatan"]].reset_index(drop=True)
        df_belum.index = df_belum.index + 1

        st.dataframe(df_belum, use_container_width=True)

        st.divider()

    # === Paparan Progress Penurunan Berat ===
        with st.expander("📉 Trend Penurunan Berat Program Ini (Klik Disini)"):
            df_plot = (df_tapis)

            fig = px.bar(
                df_plot.sort_values("PenurunanKg", ascending=False),
                x="Nama",
                y="PenurunanKg",
                title="Jumlah Penurunan Berat Setakat Ini",
                labels={"PenurunanKg": "Penurunan (kg)"},
                color="PenurunanKg",
                color_continuous_scale="Tealgrn"
            )
            st.plotly_chart(fig, use_container_width=True)

            st.divider()

    # === Interaktif Kad Maklumat ===
        st.subheader("🩺 Info Nutrisi & Kesihatan")

        info_col1, info_col2 = st.columns(2)

        with info_col1:
            st.info("🍎 **Kalori Harian:**\nAnggaran kalori untuk kekal sihat adalah sekitar 1800-2200 kcal sehari bergantung pada aktiviti harian.")
            st.info("💧 **Keperluan Air:**\nMinum 30-35ml air per kg berat badan. Contoh: 70kg × 35ml = 2.45 liter sehari.")

        with info_col2:
            st.info("🚶‍♂️ **Aktiviti Disarankan:**\n- Jalan kaki 8000-10000 langkah sehari.\n- Senaman 3-4 kali seminggu.")
            st.info("🧠 **Kesihatan Mental:**\nRehat mencukupi, kurangkan stres untuk membantu kawalan berat badan.")

    with tab2:
        st.subheader("🏆 Leaderboard")

        # Pilihan untuk filter berapa peserta nak paparkan
        pilihan_top = st.selectbox(
            "Pilih jumlah peserta untuk dipaparkan:",
            options=[5, 10, 20, 50, "Semua"],
            index=1
        )

        df_rank = df_tapis.sort_values("% Penurunan", ascending=False).reset_index(drop=True)
        df_rank["Ranking"] = df_rank.index + 1
        
        # Top N filter
        if pilihan_top != "Semua":
            df_rank = df_rank.head(int(pilihan_top))

        st.dataframe(
            df_rank[["Ranking", "Nama", "% Penurunan"]],
            use_container_width=True,
            hide_index=True
        )

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

        # === Senarai Nama Peserta Mengikut Kategori BMI (Akses Admin Sahaja) ===
        with st.expander("📋 Lihat Senarai Nama Peserta Mengikut Kategori BMI"):
            if is_admin:
                df_bmi_table = df_tapis[["Nama", "BMI", "KategoriBMI"]].sort_values(
                    "KategoriBMI", na_position="last"
                ).reset_index(drop=True)
                df_bmi_table.index = df_bmi_table.index + 1
                st.dataframe(df_bmi_table, use_container_width=True)
            else:
                st.warning("🔒 Jadual BMI dilindungi untuk privasi peserta. Sila login sebagai Admin untuk akses.")

# === Footer ===
papar_footer(
    owner="MKR Dev Team",
    version="v3.2.5",
    last_update="2025-06-26",
    tagline="Empowering Data-Driven Decisions."
)