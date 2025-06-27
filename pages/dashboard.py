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
from app.helper_logic import tambah_kiraan_peserta
from app.helper_ranking import leaderboard_dengan_status, sejarah_ranking, simpan_ranking_bulanan
from app.helper_log import log_dev
from app.settings import TARIKH_MULA, TARIKH_TIMBANG_SET, VERSI, LAST_UPDATE

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

# ==========================
# ✅ Tabs
# ==========================

tab1, tab2, tab3 = st.tabs(["📊 Info Program", "🏆 Leaderboard", "🧍‍♂️ BMI"])

# ==========================
# ✅ Function Tab 1 — Info Program
# ==========================


def paparan_info_program(df):
    with tab1:
        st.subheader("Info Program & Perkembangan Peserta")

        col1, col2, col3 = st.columns(3)
        col1.metric("Jumlah Peserta", len(df))
        col2.metric("Tarikh Mula", "18 Mei 2025")
        col3.metric("Tarikh Timbang Seterusnya", "20 Julai 2025")

        st.warning("📅 Sila bersedia untuk sesi timbangan seterusnya pada **20 Julai 2025.**")
        st.divider()

        # Kiraan Timbangan
        total = len(df)
        sudah = df["TarikhTimbang"].notna().sum()
        belum = total - sudah
        peratus_sudah = (sudah / total * 100).round(1) if total else 0
        peratus_belum = (belum / total * 100).round(1) if total else 0

        # Paparan Metrik
        col1, col2, col3 = st.columns(3)
        col1.metric("👥 Jumlah Peserta", total)
        col2.metric("✅ Sudah Timbang", f"{sudah} ({peratus_sudah}%)")
        col3.metric("❌ Belum Timbang", f"{belum} ({peratus_belum}%)")

        st.divider()

        # Carta Pie Status Timbang
        df_status = pd.DataFrame({
            "Status": ["Sudah Timbang", "Belum Timbang"],
            "Bilangan": [sudah, belum]
        })
        fig = px.pie(df_status, names="Status", values="Bilangan",
                     title="Status Timbangan Peserta",
                     color_discrete_sequence=["#00cc96", "#EF553B"],
                     hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
        st.divider()

        # Senarai Peserta Belum Timbang
        st.subheader("📋 Senarai Peserta Belum Timbang")
        df_belum = df[df["TarikhTimbang"].isna()][["Nama", "NoStaf", "Jabatan"]].reset_index(drop=True)
        df_belum.index += 1
        st.dataframe(df_belum, use_container_width=True)

with tab2:
    st.subheader("Leaderboard Penurunan Berat (%)")

    df_leaderboard = leaderboard_dengan_status()

    if df_leaderboard.empty:
        st.warning("❌ Tiada data untuk leaderboard.")
    else:
        # 🔥 Sediakan dataframe untuk paparan
        df_display = df_leaderboard.copy()

        # 🧹 Sembunyikan kolum tidak perlu
        df_display = df_display.drop(
            columns=['Jabatan', 'BeratAwal', 'TarikhTimbang', 'BeratTerkini', 'Ranking', 'Jantina'],
            errors='ignore'
        )

        # ✅ Guna terus kolum Ranking_Trend sebagai Ranking
        df_display = df_display.rename(columns={'Ranking_Trend': 'Ranking'})

        # ✅ Format % Penurunan — kosong jadi 0.00
        df_display['% Penurunan'] = df_display['% Penurunan'].fillna(0).round(2)

        # ✅ Ambil hanya Top 10
        df_display = df_display.sort_values(by='% Penurunan', ascending=False).head(10).reset_index(drop=True)

        # ✅ Susun semula kolum — Ranking di depan
        cols = df_display.columns.tolist()
        if 'Ranking' in cols and 'Nama' in cols:
            cols.insert(0, cols.pop(cols.index('Ranking')))  # Bawa Ranking ke depan
            cols.insert(1, cols.pop(cols.index('Nama')))     # Nama selepas Ranking
            df_display = df_display[cols]

        # 🔝 Highlight Top3 - berdasarkan Ranking ada emoji 🥇🥈🥉
        def highlight_top3(row):
            if str(row['Ranking']).startswith("🥇"):
                return ['background-color: gold'] * len(row)
            elif str(row['Ranking']).startswith("🥈"):
                return ['background-color: silver'] * len(row)
            elif str(row['Ranking']).startswith("🥉"):
                return ['background-color: #cd7f32'] * len(row)  # bronze
            else:
                return [''] * len(row)

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(
                df_display.style.apply(highlight_top3, axis=1),
                hide_index=True,
                use_container_width=True
            )

        with col2:
            fig = px.bar(
                df_leaderboard.sort_values('% Penurunan', ascending=False),
                x='Nama',
                y='% Penurunan',
                color='Jantina',  # ✅ Legend ikut Jantina
                text='Ranking_Trend',
                title="Leaderboard Terkini Berdasarkan % Penurunan Berat"
            )
            fig.update_layout(
                xaxis={'categoryorder': 'total descending'},
                legend_title="Jantina"
            )
            st.plotly_chart(fig, use_container_width=True)

        log_dev("Leaderboard", "Paparan leaderboard semasa")


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
        with st.expander("📋 Lihat Senarai Peserta Mengikut Kategori BMI"):
                df_bmi_table = df_tapis[["NoStaf", "BMI", "KategoriBMI"]].sort_values(
                    "KategoriBMI", na_position="last"
                ).reset_index(drop=True)
                df_bmi_table.index = df_bmi_table.index + 1
                st.dataframe(df_bmi_table, use_container_width=True)

# === Footer ===
papar_footer(
    owner="MKR Dev Team",
    version="v3.2.5",
    last_update="2025-06-26",
    tagline="Empowering Data-Driven Decisions."
)
