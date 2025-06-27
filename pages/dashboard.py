import streamlit as st
import pandas as pd
import plotly.express as px
import pytz
from datetime import datetime

from app.helper_auth import check_login
from app.styles import paparkan_tema, papar_footer
from app.helper_data import load_data_cloud_or_local as load_data
from app.helper_logic import tambah_kiraan_peserta
from app.helper_ranking import leaderboard_dengan_status
from app.helper_log import log_dev

# === Setup Paparan ===
st.set_page_config(page_title="Dashboard WLC 2025", layout="wide")
local_tz = pytz.timezone("Asia/Kuala_Lumpur")

# ✅ Login check
is_admin = check_login()

# === Tema & Header ===
st.title("📊 Dashboard Weight Loss Challenge 2025")
paparkan_tema()

# === Load Data ===
df = load_data()

if df.empty:
    st.error("❌ Tiada data peserta untuk dipaparkan.")
    st.stop()

# === Kiraan ===
df = tambah_kiraan_peserta(df)

# === Filter Sidebar ===
Kategori = st.sidebar.multiselect(
    "Pilih Kategori",
    options=df["Kategori"].dropna().unique(),
    default=df["Kategori"].dropna().unique(),
)

jantina = st.sidebar.multiselect(
    "Pilih Jantina",
    options=df["Jantina"].dropna().unique(),
    default=df["Jantina"].dropna().unique(),
)

# === Tapis Data ===
df_tapis = df[(df["Kategori"].isin(Kategori)) & (df["Jantina"].isin(jantina))]
df_sudah = df_tapis[df_tapis["BeratTerkini"].notna()]
df_belum = df_tapis[df_tapis["BeratTerkini"].isna()]

total_peserta = df_tapis.shape[0]
sudah_timbang = df_sudah.shape[0]
belum_timbang = df_belum.shape[0]

peratus_sudah = round((sudah_timbang / total_peserta * 100), 1) if total_peserta else 0
peratus_belum = round((belum_timbang / total_peserta * 100), 1) if total_peserta else 0

# === KPI Utama ===
purata_bmi = df_sudah["BMI"].mean().round(1) if sudah_timbang else 0
purata_penurunan = df_sudah["% Penurunan"].mean().round(2) if sudah_timbang else 0
purata_kg = df_sudah["PenurunanKg"].mean().round(2) if sudah_timbang else 0

# === Paparan Metrik ===
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("👥 Jumlah Peserta", total_peserta)
with col2:
    st.metric("📉 Purata BMI", purata_bmi)
with col3:
    st.metric("🏆 % Penurunan", f"{purata_penurunan}%")
with col4:
    st.metric("⚖️ Berat Turun (kg)", f"{purata_kg} kg")

# === Tabs ===
tab1, tab2, tab3 = st.tabs(["📊 Info Program", "🏆 Leaderboard", "🧍‍♂️ BMI"])

# =====================================================================================
# TAB 1: Info Program
# =====================================================================================
with tab1:
    st.subheader("Info Program & Perkembangan Peserta")

    col1, col2, col3 = st.columns(3)
    col1.metric("Jumlah Peserta", total_peserta)
    col2.metric("Tarikh Mula", "18 Mei 2025")
    col3.metric("Timbang Seterusnya", "20 Julai 2025")

    st.warning("📅 Sila bersedia untuk sesi timbangan seterusnya pada **20 Julai 2025.**")

    st.divider()

    # === Statistik Timbang ===
    st.subheader("📈 Statistik Progres Timbang Peserta")

    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Jumlah Peserta", total_peserta)
    col2.metric("✅ Sudah Timbang", f"{sudah_timbang} ({peratus_sudah}%)")
    col3.metric("❌ Belum Timbang", f"{belum_timbang} ({peratus_belum}%)")

    st.divider()

    # === Pie Chart ===
    df_status = pd.DataFrame({
        "Status": ["Sudah Timbang", "Belum Timbang"],
        "Bilangan": [sudah_timbang, belum_timbang]
    })

    fig = px.pie(df_status, names="Status", values="Bilangan",
                 title="Status Timbangan Peserta",
                 color_discrete_sequence=["#00cc96", "#EF553B"],
                 hole=0.4)

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # === Senarai Belum Timbang ===
    st.subheader("📋 Senarai Peserta Belum Timbang")
    if belum_timbang == 0:
        st.success("✅ Semua peserta telah timbang.")
    else:
        df_belum_timbang = df_belum[["Nama", "NoStaf", "Jabatan"]].reset_index(drop=True)
        df_belum_timbang.index = df_belum_timbang.index + 1
        st.dataframe(df_belum_timbang, use_container_width=True)

    st.divider()

    # === Trend Penurunan Berat ===
    st.subheader("📉 Trend Penurunan Berat Peserta")
    fig = px.bar(
        df_sudah.sort_values("PenurunanKg", ascending=False),
        x="Nama",
        y="PenurunanKg",
        title="Jumlah Penurunan Berat Setakat Ini",
        labels={"PenurunanKg": "Penurunan (kg)"},
        color="PenurunanKg",
        color_continuous_scale="Tealgrn"
    )
    st.plotly_chart(fig, use_container_width=True)

    log_dev("Dashboard", "Tab Info Program dibuka")

# =====================================================================================
# TAB 2: Leaderboard
# =====================================================================================
with tab2:
    st.subheader("Leaderboard Penurunan Berat (%)")

    df_leaderboard = leaderboard_dengan_status()

    if df_leaderboard.empty:
        st.warning("❌ Tiada data untuk leaderboard.")
    else:
        df_display = df_leaderboard.copy()

        # Format % Penurunan
        df_display["% Penurunan"] = df_display["% Penurunan"].fillna(0).round(2)

        # Ranking ke depan
        df_display = df_display.rename(columns={"Ranking_Trend": "Ranking"})
        cols = df_display.columns.tolist()
        cols.insert(0, cols.pop(cols.index("Ranking")))
        cols.insert(1, cols.pop(cols.index("Nama")))
        df_display = df_display[cols]

        # Top 10
        df_display = df_display.sort_values(by="% Penurunan", ascending=False).head(10).reset_index(drop=True)

        st.dataframe(df_display, hide_index=True, use_container_width=True)

        # Bar Chart
        fig = px.bar(
            df_leaderboard.sort_values("% Penurunan", ascending=False),
            x="Nama",
            y="% Penurunan",
            color="Jantina",
            text="Ranking_Trend",
            title="Leaderboard Berdasarkan % Penurunan Berat"
        )
        fig.update_layout(
            xaxis={'categoryorder': 'total descending'},
            legend_title="Jantina"
        )
        st.plotly_chart(fig, use_container_width=True)

        log_dev("Leaderboard", "Paparan leaderboard semasa")

# =====================================================================================
# TAB 3: BMI
# =====================================================================================
with tab3:
    st.subheader("📊 Analisis BMI Peserta")

    kategori_bmi_data = [
        ("Kurang Berat Badan", (df_sudah["KategoriBMI"] == "Kurang Berat Badan").sum()),
        ("Normal", (df_sudah["KategoriBMI"] == "Normal").sum()),
        ("Lebih Berat Badan", (df_sudah["KategoriBMI"] == "Lebih Berat Badan").sum()),
        ("Obesiti Tahap 1", (df_sudah["KategoriBMI"] == "Obesiti Tahap 1").sum()),
        ("Obesiti Tahap 2", (df_sudah["KategoriBMI"] == "Obesiti Tahap 2").sum()),
        ("Obesiti Morbid", (df_sudah["KategoriBMI"] == "Obesiti Morbid").sum()),
    ]

    cols = st.columns(6)
    for col, (label, value) in zip(cols, kategori_bmi_data):
        col.metric(label, value)

    Kategori_df = df_sudah.groupby("KategoriBMI").size().reset_index(name="Bilangan")
    fig = px.pie(Kategori_df, names="KategoriBMI", values="Bilangan",
                 title="Peratus Peserta Mengikut Tahap BMI")
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📋 Lihat Senarai Peserta Mengikut Kategori BMI"):
        df_bmi_table = df_sudah[["NoStaf", "BMI", "KategoriBMI"]].sort_values(
            "KategoriBMI", na_position="last"
        ).reset_index(drop=True)
        df_bmi_table.index = df_bmi_table.index + 1
        st.dataframe(df_bmi_table, use_container_width=True)

    log_dev("Dashboard", "Tab BMI dibuka")

# =====================================================================================
# Footer
# =====================================================================================
papar_footer(
    owner="MKR Dev Team",
    version="v3.2.5",
    last_update="2025-06-27",
    tagline="Empowering Data-Driven Decisions."
)
