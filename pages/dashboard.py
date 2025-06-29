# pages/dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from datetime import datetime

# Import helper
from app.helper_data import load_data_peserta, load_rekod_berat_semua
from app.helper_log import log_dev
from app.helper_utils import check_header_consistency
from app.styles import paparkan_tema, papar_header, papar_footer
from app.helper_logic import tambah_kiraan_peserta, kira_progress_program

# ========================================
# ✅ Layout
# ========================================
paparkan_tema()
papar_header("Dashboard | WLC 2025")

st.title("📊 Dashboard Analitik")
st.markdown("Selamat datang ke dashboard analitik program **WLC 2025**.")

# ========================================
# ✅ Load Data
# ========================================
data_peserta = load_data_peserta()
data_rekod = load_data_peserta()

HEADER_PESERTA = [
    'Nama', 'NoStaf', 'Umur', 'Jantina', 'Jabatan',
    'Tinggi', 'BeratAwal', 'TarikhDaftar',
    'BeratTerkini', 'TarikhTimbang', 'BMI', 'Kategori'
]

# ========================================
# ✅ Tabs Layout
# ========================================
tab1, tab2, tab3, tab4 = st.tabs(
    ["📈 Info Program", "🏆 Leaderboard", "📉 Status Timbang", "📊 Analitik BMI"]
)

# ========================================
# ✅ Tab 1: Info Program
# ========================================
with tab1:
    st.subheader("📜 Maklumat Program WLC 2025")

    if check_header_consistency(data_peserta, HEADER_PESERTA, "Data Peserta"):
        # ✅ Tambah kiraan peserta
        df_kiraan = tambah_kiraan_peserta(data_peserta)

        # ✅ Kiraan asas
        total_peserta = len(df_kiraan)
        avg_bmi = df_kiraan["BMI"].mean().round(2)
        avg_penurunan = df_kiraan["% Penurunan"].mean().round(2)

        # ✅ Split ikut jantina
        total_lelaki = len(df_kiraan[df_kiraan["Jantina"].str.lower() == "lelaki"])
        total_perempuan = len(df_kiraan[df_kiraan["Jantina"].str.lower() == "perempuan"])

        # ✅ Paparan metrik utama
        col1, col2, col3 = st.columns(3)
        col1.metric("👥 Jumlah Peserta", total_peserta)
        col2.metric("⚖️ BMI Purata", f"{avg_bmi:.2f}")
        col3.metric("📉 Penurunan Berat Purata (%)", f"{avg_penurunan:.2f}%")

        with col1:
            st.markdown(
                f"""
                <div style='text-align: left'>
                    👨‍🦱 <b>Lelaki:</b> {total_lelaki} <br>
                    👩 <b>Perempuan:</b> {total_perempuan}
                </div>
                """,
                unsafe_allow_html=True
            )

        st.divider()

        # 🎨 Timeline Progress Visual
        
        st.divider()

        # ✅ Info Ringkas Program
        with st.expander("ℹ️ Maklumat Program"):
            st.markdown(
                """
                **📅 Tarikh Program:** 18 Jun 2025 — 20 Ogos 2025  
                **📍 Lokasi:** Wilayah Kuala Selangor  
                **🎯 Objektif Program:**  
                - Meningkatkan kesedaran kesihatan dalam komuniti.  
                - Membantu peserta capai berat badan ideal secara sihat.  
                - Memupuk gaya hidup aktif dan sihat.  
                """
            )

        # ✅ Milestone Progress
        st.subheader("🚩 Milestone Program")
        col1, col2, col3, col4 = st.columns(4)

        col1.success("✅ Pendaftaran")
        col2.info("🔄 Timbang 1")
        col3.warning("⏳ Timbang 2")
        col4.error("⏳ Penilaian Akhir")

        st.caption("Status milestone bergantung kepada tarikh dan sesi program.")

        st.divider()

        log_dev("Dashboard", "Buka Tab Info Program", "Success")




# ========================================
# ✅ Tab 2: Leaderboard
# ========================================
from app.helper_ranking import leaderboard_peserta, trend_penurunan_bulanan
from app.helper_data import load_rekod_berat_semua

with tab2:
    st.subheader("Leaderboard & Trend Berat Badan")

    col1, col2 = st.columns(2)

    # ==========================
    # 🎖️ Leaderboard Top 10
    # ==========================
    with col1:
        st.markdown("### 🏅 Top 10 Penurunan Berat (%)")

        leaderboard = leaderboard_peserta(data_peserta, top_n=10)

        if not leaderboard.empty:
            st.dataframe(
                leaderboard.set_index("Ranking").style.format({"% Penurunan": "{:.2f}%"}),
                use_container_width=True
            )
        else:
            st.info("⚠️ Tiada data leaderboard untuk dipaparkan.")

    # ==========================
    # 📊 Trend Berat Bulanan
    # ==========================
    with col2:
        st.markdown("### 📈 Trend Berat Purata Bulanan")

        df_rekod = load_rekod_berat_semua()

        fig = trend_penurunan_bulanan(df_rekod)

        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("⚠️ Tiada data trend untuk dipaparkan.")

    st.divider()

    log_dev("Dashboard", "Buka Tab Leaderboard + Trend", "Success")




# =====================================================================================
# TAB 3: Status Timbang
# =====================================================================================
with tab3:
    st.subheader("Status Timbangan Mengikut Sesi Bulanan")

    df_rekod = load_rekod_berat_semua()
    df_peserta = load_data_peserta()

    if df_rekod.empty:
        st.warning("❌ Tiada rekod timbang ditemui.")
        st.stop()

    jumlah_peserta = len(df_peserta)

    sesi_list = sorted(df_rekod["SesiBulan"].unique(), key=lambda x: pd.to_datetime(x))

    for sesi in sesi_list:
        st.subheader(f"📅 {sesi}")

        df_sesi = df_rekod[df_rekod["SesiBulan"] == sesi]
        nama_sudah = df_sesi["Nama"].unique().tolist()

        sudah_timbang = len(nama_sudah)
        belum_timbang = jumlah_peserta - sudah_timbang

        peratus_sudah = round(sudah_timbang / jumlah_peserta * 100, 1)
        peratus_belum = round(belum_timbang / jumlah_peserta * 100, 1)

        col1, col2, col3 = st.columns(3)
        col1.metric("👥 Jumlah Peserta", jumlah_peserta)
        col2.metric("✅ Sudah Timbang", f"{sudah_timbang} ({peratus_sudah}%)")
        col3.metric("❌ Belum Timbang", f"{belum_timbang} ({peratus_belum}%)")

        if peratus_sudah == 100:
            st.success(f"✅ Sesi timbang bulan {sesi} selesai 100%.")
        else:
            st.warning(f"⚠️ Sesi timbang bulan {sesi} belum lengkap.")

        df_belum = df_peserta[~df_peserta["Nama"].isin(nama_sudah)]

        if not df_belum.empty:
            with st.expander(f"📋 Senarai Peserta Belum Timbang {sesi}"):
                df_belum_view = df_belum[["Nama", "NoStaf", "Jabatan"]].reset_index(drop=True)
                df_belum_view.index = df_belum_view.index + 1
                st.dataframe(df_belum_view, use_container_width=True)

        st.divider()

    bulan_seterusnya = (pd.to_datetime('today') + pd.DateOffset(months=1)).strftime('%B %Y')
    st.info(f"🔔 Ingatan: Sesi timbang seterusnya adalah pada bulan **{bulan_seterusnya}**.")





# ========================================
# ✅ Tab 4: Analitik BMI
# ========================================
from app.styles import WARNA_KATEGORI_BMI

with tab4:
    st.subheader("📊 Analisis BMI Peserta")

    df_tapis = data_peserta.copy()

    if not df_tapis.empty:
        kategori_bmi_data = [
            ("Kurang Berat Badan", "Kurang Berat Badan", (df_tapis["Kategori"] == "Kurang Berat Badan").sum()),
            ("Normal", "Normal", (df_tapis["Kategori"] == "Normal").sum()),
            ("Lebih Berat Badan", "Lebih Berat Badan", (df_tapis["Kategori"] == "Lebih Berat Badan").sum()),
            ("Obesiti Tahap 1", "Obesiti Tahap 1", (df_tapis["Kategori"] == "Obesiti Tahap 1").sum()),
            ("Obesiti Tahap 2", "Obesiti Tahap 2", (df_tapis["Kategori"] == "Obesiti Tahap 2").sum()),
            ("Obesiti Morbid", "Obesiti Morbid", (df_tapis["Kategori"] == "Obesiti Morbid").sum()),
        ]

        cols = st.columns(6)

        for col, (label, kategori, value) in zip(cols, kategori_bmi_data):
            warna = WARNA_KATEGORI_BMI.get(kategori, "#DDDDDD")
            col.markdown(
                f"""
                <div style="background-color: {warna}; padding: 10px; border-radius: 10px; text-align: center;">
                    <div style="font-weight: bold; color: white;">{label}</div>
                    <div style="font-size: 24px; font-weight: bold; color: white;">{value}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        Kategori_df = df_tapis.groupby("Kategori").size().reset_index(name="Bilangan")

        fig = px.pie(
            Kategori_df,
            names="Kategori",
            values="Bilangan",
            title="Peratus Peserta Mengikut Tahap BMI",
            color="Kategori",
            color_discrete_map=WARNA_KATEGORI_BMI
        )

        fig.update_traces(textinfo='percent+label')

        st.plotly_chart(fig, use_container_width=True)

        with st.expander("📋 Lihat Senarai Peserta Mengikut Kategori BMI"):
            df_bmi_table = df_tapis[["NoStaf", "Nama", "BMI", "Kategori"]].sort_values("Kategori", na_position="last").reset_index(drop=True)
            df_bmi_table.index = df_bmi_table.index + 1
            st.dataframe(df_bmi_table, use_container_width=True)


        



# ========================================
# ✅ Footer
# ========================================
papar_footer(
    owner="MKR Dev Team",
    version="v3.3.0",
    last_update="2025-06-27",
    tagline="Empowering Data-Driven Decisions."
)
