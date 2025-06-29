# pages/dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from datetime import datetime

# Import helper
from app.helper_data import load_data_peserta, load_rekod_berat_semua
from app.helper_ranking import leaderboard_dengan_status
from app.helper_log import log_dev
from app.helper_utils import check_header_consistency, proses_data_peserta
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
from app.helper_logic import kira_progress_program


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

        # ✅ Paparan jantina
        col4, col5 = st.columns(2)
        col4.metric("👨‍🦱 Lelaki", total_lelaki)
        col5.metric("👩 Perempuan", total_perempuan)

        st.divider()

        # 🎯 Progress Program
        progress = kira_progress_program()

        st.subheader("⏳ Progress Program WLC 2025")
        st.info(
            f"{progress['status']} — Hari ke-{progress['hari_berlalu']}.\n\n"
            f"📅 {progress['tarikh_mula'].strftime('%d %b %Y')} hingga {progress['tarikh_tamat'].strftime('%d %b %Y')}"
        )

        st.progress(progress['progress'] / 100)

        # 🎨 Timeline Visual dengan Plotly
        fig = go.Figure()

        # Bar utama
        fig.add_trace(go.Bar(
            x=[progress['progress']],
            y=["Progress Program"],
            orientation='h',
            marker=dict(color='green' if progress['progress'] >= 100 else 'orange'),
            width=0.4,
            name="Progress"
        ))

        # Bar latar belakang (100%)
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


        st.subheader("📅 Senarai Pendaftaran")
        st.dataframe(
            data_peserta[["Nama", "NoStaf", "TarikhDaftar"]].set_index(
                pd.Index(range(1, len(data_peserta) + 1), name="No.")
            ),
            use_container_width=True
        )

        log_dev("Dashboard", "Buka Tab Info Program", "Success")




# ========================================
# ✅ Tab 2: Leaderboard
# ========================================
with tab2:
    st.subheader("🏆 Leaderboard Berat Badan")

    # ✅ Load data & proses
    df = proses_data_peserta(data_peserta)

    # ✅ Load leaderboard
    leaderboard = leaderboard_dengan_status(df)

    if leaderboard is not None and not leaderboard.empty:
        # ✅ Paparan Leaderboard dengan hide index
        st.dataframe(
            leaderboard.set_index(
                pd.Index(range(1, len(leaderboard) + 1), name="No.")
            ),
            use_container_width=True
        )
    else:
        st.info("⚠️ Tiada data leaderboard untuk dipaparkan.")

    log_dev("Dashboard", "Buka Tab Leaderboard", "Success")

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
with tab4:
        st.subheader("📊 Analisis BMI Peserta")

        df_tapis = data_peserta.copy()

        if not df_tapis.empty:
            # 📊 Paparan metrik kategori BMI
            cols = st.columns(6)
            kategori_bmi_data = [
                ("Kurang Berat Badan", "kurang", (df_tapis["Kategori"] == "Kurang Berat Badan").sum()),
                ("Normal", "normal", (df_tapis["Kategori"] == "Normal").sum()),
                ("Lebih Berat Badan", "lebih", (df_tapis["Kategori"] == "Lebih Berat Badan").sum()),
                ("Obesiti Tahap 1", "obes1", (df_tapis["Kategori"] == "Obesiti Tahap 1").sum()),
                ("Obesiti Tahap 2", "obes2", (df_tapis["Kategori"] == "Obesiti Tahap 2").sum()),
                ("Obesiti Morbid", "morbid", (df_tapis["Kategori"] == "Obesiti Morbid").sum()),
            ]

        col1, col2, col3, col4, col5, col6 = st.columns(6)

        # Paparan metrik kategori BMI dengan gaya mengikut warna
        cols = st.columns(6)
        kategori_bmi_data = [
            ("Kurang Berat Badan", "kurang", (df_tapis["Kategori"] == "Kurang Berat Badan").sum()),
            ("Normal", "normal", (df_tapis["Kategori"] == "Normal").sum()),
            ("Lebih Berat Badan", "lebih", (df_tapis["Kategori"] == "Lebih Berat Badan").sum()),
            ("Obesiti Tahap 1", "obes1", (df_tapis["Kategori"] == "Obesiti Tahap 1").sum()),
            ("Obesiti Tahap 2", "obes2", (df_tapis["Kategori"] == "Obesiti Tahap 2").sum()),
            ("Obesiti Morbid", "morbid", (df_tapis["Kategori"] == "Obesiti Morbid").sum()),
        ]

        for col, (label, css_class, value) in zip(cols, kategori_bmi_data):
            col.markdown(f"""
            <div class="bmi-box {css_class}">
                <div class="bmi-title">{label}</div>
                <div class="bmi-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)

        Kategori_df = df_tapis.groupby("Kategori").size().reset_index(name="Bilangan")
        fig = px.pie(Kategori_df, names="Kategori", values="Bilangan", title="Peratus Peserta Mengikut Tahap BMI")
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("📋 Lihat Senarai Peserta Mengikut Kategori BMI"):
            df_bmi_table = df_tapis[["NoStaf", "BMI", "Kategori"]].sort_values("Kategori", na_position="last").reset_index(drop=True)
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
