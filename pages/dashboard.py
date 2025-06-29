# ========================================
# 📊 Dashboard Analitik WLC 2025
# ========================================
import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# ===== Import Helper =====
from app.helper_data import load_data_peserta, load_rekod_berat_semua
from app.helper_log import log_dev
from app.helper_utils import check_header_consistency
from app.helper_logic import tambah_kiraan_peserta, kira_progress_program
from app.helper_ranking import leaderboard_peserta, trend_penurunan_bulanan
from app.styles import paparkan_tema, papar_header, papar_footer

# ===== Layout & Tema =====
paparkan_tema()
papar_header("Dashboard | WLC 2025")

st.title("📊 Dashboard Analitik WLC 2025")

# ===== Load Data =====
data_peserta = load_data_peserta()

HEADER_PESERTA = [
    'Nama', 'NoStaf', 'Umur', 'Jantina', 'Jabatan',
    'Tinggi', 'BeratAwal', 'TarikhDaftar',
    'BeratTerkini', 'TarikhTimbang', 'BMI', 'Kategori'
]

# ===== Tabs =====
tab1, tab2, tab3, tab4 = st.tabs([
    "📜 Info Program", "🏆 Leaderboard",
    "📉 Status Timbang", "📊 Analitik BMI"
])

# ========================================
# ✅ Tab 1: Info Program
# ========================================
with tab1:
    st.subheader("📜 KPI & Progress Program")

    if check_header_consistency(data_peserta, HEADER_PESERTA, "Data Peserta"):
        df_kiraan = tambah_kiraan_peserta(data_peserta)

        # Kiraan KPI
        total_peserta = len(df_kiraan)
        avg_bmi = df_kiraan["BMI"].mean().round(2)
        avg_penurunan = df_kiraan["% Penurunan"].mean().round(2)

        total_lelaki = len(df_kiraan[df_kiraan["Jantina"].str.lower() == "lelaki"])
        total_perempuan = len(df_kiraan[df_kiraan["Jantina"].str.lower() == "perempuan"])

        col1, col2, col3 = st.columns(3)
        col1.metric("👥 Jumlah Peserta", total_peserta)
        col2.metric("⚖️ BMI Purata", f"{avg_bmi:.2f}")
        col3.metric("📉 Penurunan Berat Purata (%)", f"{avg_penurunan:.2f}%")

        with col1:
            st.markdown(f"""
            <div style='text-align: left'>
                👨‍🦱 <b>Lelaki:</b> {total_lelaki}<br>
                👩 <b>Perempuan:</b> {total_perempuan}
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # Progress Program
        progress = kira_progress_program()

        st.subheader("⏳ Progress Program WLC 2025")
        st.info(
            f"{progress['status']} — Hari ke-{progress['hari_berlalu']}.\n\n"
            f"📅 {progress['tarikh_mula'].strftime('%d %b %Y')} hingga {progress['tarikh_tamat'].strftime('%d %b %Y')}"
        )
        st.progress(progress['progress'] / 100)

        # Timeline Plot
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=[progress['progress']],
            y=["Progress Program"],
            orientation='h',
            marker=dict(color='green' if progress['progress'] >= 100 else 'orange'),
            width=0.4,
            name="Progress"
        ))

        fig.add_trace(go.Bar(
            x=[100 - progress['progress']],
            y=["Progress Program"],
            orientation='h',
            marker=dict(color='lightgray'),
            width=0.4,
            name="Remaining"
        ))

        fig.update_layout(
            barmode='stack',
            xaxis=dict(range=[0, 100], title="Peratus (%)"),
            yaxis=dict(showticklabels=False),
            height=150,
            showlegend=False,
            margin=dict(l=20, r=20, t=20, b=20)
        )

        st.plotly_chart(fig, use_container_width=True)

        log_dev("Dashboard", "Buka Tab Info Program", "Success")

# ========================================
# ✅ Tab 2: Leaderboard
# ========================================
with tab2:
    st.subheader("Leaderboard & Trend Berat")

    col1, col2 = st.columns(2)

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

    with col2:
        st.markdown("### 📈 Trend Berat Purata Bulanan")
        df_rekod = load_rekod_berat_semua()

        fig = trend_penurunan_bulanan(df_rekod)

        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("⚠️ Tiada data trend untuk dipaparkan.")

    log_dev("Dashboard", "Buka Tab Leaderboard + Trend", "Success")

# ========================================
# ✅ Tab 3: Status Timbang
# ========================================
from app.helper_data import load_rekod_berat_semua

with tab3:
    st.subheader("Status Timbangan Mengikut Sesi Bulanan")

    df_rekod = load_rekod_berat_semua()
    df_peserta = data_peserta

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

# ========================================
# ✅ Tab 4: Analitik BMI
# ========================================
from app.styles import warna_mapping

with tab4:
    st.subheader("📊 Analisis BMI Peserta")

    df_kiraan = tambah_kiraan_peserta(data_peserta)

    kategori_bmi = df_kiraan.groupby("Kategori").size().reset_index(name="Bilangan")
    fig = px.pie(
        kategori_bmi, names="Kategori", values="Bilangan",
        color="Kategori", color_discrete_map=warna_mapping,
        title="Peratus Peserta Mengikut Tahap BMI"
    )
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📋 Lihat Senarai Peserta Mengikut Kategori BMI"):
        df_bmi = df_kiraan[["Nama", "NoStaf", "BMI", "Kategori"]].sort_values("Kategori")
        df_bmi.index = df_bmi.index + 1
        st.dataframe(df_bmi, use_container_width=True)

# ========================================
# ✅ Footer
# ========================================
papar_footer(
    owner="MKR Dev Team",
    version="v3.3.0",
    last_update="2025-06-29",
    tagline="Empowering Data-Driven Decisions."
)
