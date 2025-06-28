# pages/dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px

from datetime import datetime

# Import helper
from app.helper_data import load_data_peserta, load_data_cloud_or_local
from app.helper_ranking import leaderboard_dengan_status
from app.helper_log import log_dev
from app.helper_utils import check_header_consistency, proses_data_peserta
from app.styles import paparkan_tema, papar_header, papar_footer


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
data_rekod = load_data_cloud_or_local()

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
        total_peserta = len(data_peserta)
        avg_berat = data_peserta["BeratAwal"].mean()

        col1, col2 = st.columns(2)
        col1.metric("👥 Jumlah Peserta", total_peserta)
        col2.metric("⚖️ Berat Awal Purata (kg)", f"{avg_berat:.2f}")

        st.divider()

        st.subheader("📅 Senarai Pendaftaran")
        st.dataframe(
            data_peserta[["Nama", "NoStaf", "Jabatan", "TarikhDaftar"]].set_index(
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
    st.subheader("📉 Status Timbangan Peserta")

    # ✅ Load data peserta dari Google Sheet
    df = data_peserta.copy()

    # ✅ Pastikan kolum utama wujud
    wajib_kolum = ["Nama", "NoStaf", "Jabatan", "BeratTerkini", "TarikhTimbang"]
    if not set(wajib_kolum).issubset(df.columns):
        st.error("❌ Kolum tidak lengkap dalam Google Sheet. Sila pastikan kolum berikut wujud: " + ", ".join(wajib_kolum))
        st.stop()

    # ✅ Bersihkan data & kira status timbang
    df = proses_data_peserta(df)

    # ✅ Kira jumlah peserta
    total_peserta = len(df)

    # ✅ Kira status timbang
    sudah_timbang = (df["StatusTimbang"] == "Sudah Timbang").sum()
    belum_timbang = (df["StatusTimbang"] == "Belum Timbang").sum()

    # ✅ Kira peratus
    peratus_sudah = round(sudah_timbang / total_peserta * 100, 1) if total_peserta else 0
    peratus_belum = round(belum_timbang / total_peserta * 100, 1) if total_peserta else 0

    # ✅ Paparan metrik
    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Jumlah Peserta", total_peserta)
    col2.metric("✅ Sudah Timbang", f"{sudah_timbang} ({peratus_sudah}%)")
    col3.metric("❌ Belum Timbang", f"{belum_timbang} ({peratus_belum}%)")

    st.divider()

    # ✅ Pie Chart
    df_status = pd.DataFrame({
        "Status": ["Sudah Timbang", "Belum Timbang"],
        "Bilangan": [sudah_timbang, belum_timbang]
    })

    fig = px.pie(
        df_status,
        names="Status",
        values="Bilangan",
        title="Status Timbangan Peserta",
        color_discrete_sequence=["#00cc96", "#EF553B"],
        hole=0.4
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ✅ Senarai Belum Timbang
    st.subheader("📋 Senarai Peserta Belum Timbang")
    if belum_timbang == 0:
        st.success("✅ Semua peserta telah timbang.")
    else:
        df_belum = df[df["StatusTimbang"] == "Belum Timbang"]
        df_belum_timbang = df_belum[["Nama", "NoStaf", "Jabatan"]].reset_index(drop=True)
        df_belum_timbang.index = df_belum_timbang.index + 1

        st.dataframe(df_belum_timbang, use_container_width=True)

    log_dev("Dashboard", "Buka Tab Status Timbangan", "Success")

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

        with st.expander("📋 Lihat Senarai Nama Peserta Mengikut Kategori BMI"):
            df_bmi_table = df_tapis[["Nama", "BMI", "Kategori"]].sort_values("Kategori", na_position="last").reset_index(drop=True)
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
