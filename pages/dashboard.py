# pages/dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

from app.helper_auth import check_login
from app.helper_data import load_data_peserta, load_data_cloud_or_local
from app.helper_ranking import leaderboard_dengan_status
from app.helper_log import log_dev
from app.helper_utils import check_header_consistency
from app.styles import paparkan_tema, papar_header, papar_footer


# =============================================================
# ✅ Semakan Login
# =============================================================
is_admin = check_login()

if not is_admin:
    st.error("❌ Akses ditolak! Halaman ini hanya untuk Admin.")
    st.stop()


# =============================================================
# ✅ Layout
# =============================================================
paparkan_tema()
papar_header("Dashboard | WLC 2025")

st.title("📊 Dashboard Analitik")
st.markdown("Selamat datang ke dashboard analitik program WLC 2025.")

# =============================================================
# ✅ Load Data
# =============================================================
data_peserta = load_data_peserta()
data_rekod = load_data_cloud_or_local()

HEADER_PESERTA = [
    'Nama', 'NoStaf', 'Umur', 'Jantina', 'Jabatan',
    'Tinggi', 'BeratAwal', 'TarikhDaftar',
    'BeratTerkini', 'TarikhTimbang', 'BMI', 'Kategori'
]

# =============================================================
# ✅ Tabs Layout
# =============================================================
tab1, tab2, tab3 = st.tabs(["📈 Info Program", "🏆 Leaderboard", "📊 Analitik BMI"])

# =============================================================
# ✅ Tab 1: Info Program
# =============================================================
with tab1:
    st.subheader("📜 Maklumat Program WLC 2025")

    if check_header_consistency(data_peserta, HEADER_PESERTA, "Data Peserta"):
        total_peserta = len(data_peserta)
        avg_berat = data_peserta["BeratAwal"].mean()

        st.metric("Jumlah Peserta", total_peserta)
        st.metric("Berat Awal Purata (kg)", f"{avg_berat:.2f}")

        st.markdown("---")

        st.subheader("📅 Senarai Pendaftaran")
        st.dataframe(
            data_peserta[["Nama", "NoStaf", "Jabatan", "TarikhDaftar"]].set_index(
                pd.Index(range(1, len(data_peserta) + 1), name="No.")
            ),
            use_container_width=True
        )

    log_dev("Dashboard", "Buka Tab Info Program", "Success")

# =============================================================
# ✅ Tab 2: Leaderboard
# =============================================================
with tab2:
    st.subheader("🏆 Leaderboard Berat Badan")

    leaderboard = leaderboard_dengan_status(data_rekod)

    if leaderboard is not None and not leaderboard.empty:
        st.dataframe(
            leaderboard.set_index(
                pd.Index(range(1, len(leaderboard) + 1), name="No.")
            ),
            use_container_width=True
        )
    else:
        st.info("⚠️ Tiada data leaderboard untuk dipaparkan.")

    log_dev("Dashboard", "Buka Tab Leaderboard", "Success")

# =============================================================
# ✅ Tab 3: Analitik BMI
# =============================================================
with tab3:
    st.subheader("📊 Analitik BMI Peserta")

    if check_header_consistency(data_rekod, HEADER_PESERTA, "Rekod Ranking"):

        bmi_summary = data_rekod["Kategori"].value_counts().reset_index()
        bmi_summary.columns = ["Kategori", "Bilangan"]

        fig = px.pie(
            bmi_summary,
            names="Kategori",
            values="Bilangan",
            title="Peratusan Kategori BMI Peserta",
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        fig_bar = px.bar(
            bmi_summary,
            x="Kategori",
            y="Bilangan",
            color="Kategori",
            title="Bilangan Peserta Mengikut Kategori BMI",
            text_auto=True
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    log_dev("Dashboard", "Buka Tab Analitik BMI", "Success")


# =============================================================
# ✅ Footer
# =============================================================
papar_footer(
    owner="MKR Dev Team",
    version="v3.2.5",
    last_update="2025-06-27",
    tagline="Empowering Data-Driven Decisions."
)
