# ========================================
# 📊 Dashboard Analitik WLC 2025
# ========================================
import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# ===== Import Helper =====
from app.helper_data import load_data_peserta, load_rekod_berat_semua, dataframe_status_berat
from app.helper_utils import check_header_consistency, tambah_sesi_bulan
from app.helper_logic import tambah_kiraan_peserta, kira_progress_program
from app.helper_ranking import leaderboard_peserta, trend_penurunan_bulanan
from app.styles import paparkan_tema, papar_header, papar_footer, warna_mapping, apply_css

# ===== Layout & Tema =====
paparkan_tema()
apply_css()
papar_header("Dashboard | WLC 2025")

st.title("📊 Dashboard Analitik WLC 2025")

# =========================================
# ✅ Load Data
# =========================================
data_peserta = load_data_peserta()
df_kiraan = tambah_kiraan_peserta(data_peserta)

data_rekod = load_rekod_berat_semua()
df_rekod = tambah_sesi_bulan(data_rekod)

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

# ========================================
# ✅ Tab 2: Leaderboard
# ========================================
with tab2:
    st.subheader("Leaderboard & Trend Berat")

    col1, col2 = st.columns(2)

    # ========================================
# ✅ Leaderboard Penurunan Berat
# ========================================
with col1:
    st.markdown("### 🏅 Top 10 Penurunan Berat (%)")

    leaderboard = leaderboard_peserta(data_peserta, top_n=10)

    if not leaderboard.empty:
        # ✅ Masukkan Icon 🏆 ke dalam kolum Ranking
        leaderboard = leaderboard.copy()
        leaderboard["Ranking"] = leaderboard.apply(
            lambda row: f"🏆 {row['Ranking']}" if row["% Penurunan"] > 0 else f"{row['Ranking']}",
            axis=1
        )

        st.dataframe(
            leaderboard.set_index("Ranking")
            .style.format({"% Penurunan": "{:.2f}%"}),
            use_container_width=True
        )
    else:
        st.info("⚠️ Tiada data leaderboard untuk dipaparkan.")


    # ========================================
    # ✅ Trend Berat Purata Bulanan
    # ========================================
    with col2:
        st.markdown("### 📈 Trend Berat Purata Bulanan")

        df_rekod = load_rekod_berat_semua()
        fig = trend_penurunan_bulanan(df_rekod)

        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("⚠️ Tiada data trend untuk dipaparkan.")


# ========================================
# ✅ Tab 3: Status Timbang
# ========================================
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

# =========================================
# ✅ Tab 4: Analitik BMI
# =========================================
with tab4:
    st.subheader("📊 Analisis BMI Peserta")

    # =========================================
    # ✅ Pilihan Filter Jantina
    # =========================================
    filter_jantina = st.selectbox(
        "Pilih Jantina untuk Analisis:",
        ["Semua", "Lelaki", "Perempuan"]
    )

    # =========================================
    # ✅ Apply Filter
    # =========================================
    if filter_jantina == "Lelaki":
        df_filter = data_peserta[data_peserta["Jantina"].str.lower() == "lelaki"]
    elif filter_jantina == "Perempuan":
        df_filter = data_peserta[data_peserta["Jantina"].str.lower() == "perempuan"]
    else:
        df_filter = data_peserta.copy()

    df_filter = tambah_kiraan_peserta(df_filter)

    # =========================================
    # ✅ Metrik BMI
    # =========================================
    cols = st.columns(6)
    kategori_bmi_data = [
        ("Kurang Berat Badan", "kurang", (df_filter["Kategori"] == "Kurang Berat Badan").sum()),
        ("Normal", "normal", (df_filter["Kategori"] == "Normal").sum()),
        ("Lebih Berat Badan", "lebih", (df_filter["Kategori"] == "Lebih Berat Badan").sum()),
        ("Obesiti Tahap 1", "obes1", (df_filter["Kategori"] == "Obesiti Tahap 1").sum()),
        ("Obesiti Tahap 2", "obes2", (df_filter["Kategori"] == "Obesiti Tahap 2").sum()),
        ("Obesiti Morbid", "morbid", (df_filter["Kategori"] == "Obesiti Morbid", "Lebih 40.0").sum()),
    ]

    for col, (label, css_class, value) in zip(cols, kategori_bmi_data):
        col.markdown(f"""
        <div class="bmi-box {css_class}">
            <div class="bmi-title">{label}</div>
            <div class="bmi-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

    # =========================================
    # ✅ Pie Chart Ikut Filter
    # =========================================
    st.markdown(f"### Peratus BMI ({filter_jantina})")
    kategori_bmi = df_filter.groupby("Kategori").size().reset_index(name="Bilangan")

    fig = px.pie(
        kategori_bmi,
        names="Kategori",
        values="Bilangan",
        title=f"Peratus Peserta ({filter_jantina}) Mengikut Tahap BMI",
        color="Kategori",
        color_discrete_map=warna_mapping
    )
    st.plotly_chart(fig, use_container_width=True)

    # =========================================
    # ✅ Dual Pie Chart: Lelaki vs Perempuan
    # =========================================
    st.markdown("### Perbandingan BMI Lelaki & Perempuan")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 👨 Lelaki")
        df_male = data_peserta[data_peserta["Jantina"].str.lower() == "lelaki"]
        df_male = tambah_kiraan_peserta(df_male)

        kategori_male = df_male.groupby("Kategori").size().reset_index(name="Bilangan")
        fig_male = px.pie(
            kategori_male,
            names="Kategori",
            values="Bilangan",
            title="BMI Lelaki",
            color="Kategori",
            color_discrete_map=warna_mapping
        )
        st.plotly_chart(fig_male, use_container_width=True)

    with col2:
        st.markdown("#### 👩 Perempuan")
        df_female = data_peserta[data_peserta["Jantina"].str.lower() == "perempuan"]
        df_female = tambah_kiraan_peserta(df_female)

        kategori_female = df_female.groupby("Kategori").size().reset_index(name="Bilangan")
        fig_female = px.pie(
            kategori_female,
            names="Kategori",
            values="Bilangan",
            title="BMI Perempuan",
            color="Kategori",
            color_discrete_map=warna_mapping
        )
        st.plotly_chart(fig_female, use_container_width=True)


    with st.expander("🎯 Status Berat, Target Realistik & Ideal"):
        df_status = dataframe_status_berat(data_peserta)
        df_status.index = range(1, len(df_status) + 1)
        st.dataframe(df_status, use_container_width=True)   

    # =========================================
    # ✅ Senarai Data Mengikut Filter
    # =========================================
    with st.expander(f"📋 Lihat Senarai Peserta ({filter_jantina}) Mengikut Kategori BMI"):
        df_bmi = df_filter[["Nama", "NoStaf", "BMI", "Kategori"]].sort_values("Kategori")
        df_bmi.index = df_bmi.index + 1
        st.dataframe(df_bmi, use_container_width=True)





# ========================================
# ✅ Footer
# ========================================
papar_footer(
    owner="MKR Dev Team",
    version="v3.3.1",
    last_update="2025-06-29",
    tagline="Empowering Data-Driven Decisions."
)
