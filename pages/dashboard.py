# dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime
import pytz
import gspread
from google.oauth2.service_account import Credentials

from app.styles import paparkan_tema, papar_footer, papar_header
from app.helper_data import load_data_cloud_or_local as load_data
from app.helper_logic import tambah_kiraan_peserta

# === Streamlit page setup ===
st.set_page_config(page_title="Dashboard WLC 2025", layout="wide")
local_tz = pytz.timezone("Asia/Kuala_Lumpur")

# === Google Sheets connection for Tab 1 ===
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"], scopes=scope)
client = gspread.authorize(creds)
sh = client.open("data_peserta")

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
            <div class="wlc-title">👥 Jumlah Peserta</div>
            <div class="wlc-value">{total_peserta}</div>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="wlc-box">
            <div class="wlc-title">📉 Purata BMI</div>
            <div class="wlc-value">{purata_bmi}</div>
        </div>""", unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="wlc-box">
            <div class="wlc-title">🏆 % Penurunan</div>
            <div class="wlc-value">{purata_penurunan}%</div>
        </div>""", unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="wlc-box">
            <div class="wlc-title">⚖️ Berat Turun (kg)</div>
            <div class="wlc-value">{purata_kg} kg</div>
        </div>""", unsafe_allow_html=True)

    # Tabs
    tab1, tab2, tab3 = st.tabs(["📉 Penurunan Berat", "🏆 Leaderboard", "🧍‍♂️ BMI"])

    # ================== TAB 1: Trend Program ==================
    with tab1:
        st.subheader("📈 Prestasi Keseluruhan Program WLC 2025")
    
        # === Tarik data dari sheet 'rekod_berat' ===
        sheet_rekod = sh.worksheet("rekod_berat")
        df_rekod = pd.DataFrame(sheet_rekod.get_all_records())

        # Pastikan jenis data betul
        if 'Timestamp' in df_rekod.columns:
            df_rekod['Timestamp'] = pd.to_datetime(df_rekod['Timestamp'])
        else:
            df_rekod['Timestamp'] = pd.to_datetime(df_rekod['Tarikh Rekod'])

        df_rekod['Tarikh Rekod'] = pd.to_datetime(df_rekod['Tarikh Rekod']).dt.date

        # Jika tiada kolum 'Sesi', jana semula (fallback)
        if 'Sesi' not in df_rekod.columns:
            def label_sesi(tarikh):
                bulan = pd.to_datetime(tarikh).month
                if bulan == 6:
                    return "Jun"
                elif bulan == 7:
                    return "Julai"
                elif bulan == 8:
                    return "Ogos"
                else:
                    return "Luar Program"
            df_rekod['Sesi'] = df_rekod['Tarikh Rekod'].apply(label_sesi)

        # === Statistik Kehadiran Timbang ===
        st.markdown("### 🗓️ Statistik Kehadiran Timbang")
        kira_hadir = df_rekod.groupby("Sesi")["No.Staf"].nunique().reset_index(name="Bilangan Peserta Timbang")
        st.dataframe(kira_hadir, use_container_width=True)

        # === Purata % Penurunan Berat setiap bulan ===
        st.markdown("### 📉 Purata % Penurunan Berat Mengikut Sesi")
        df_sorted = df_rekod.sort_values(by=['No.Staf', 'Tarikh Rekod'])

        # Ambil berat pertama dan terakhir peserta
        berat_awal = df_sorted.groupby('No.Staf').first().reset_index()
        berat_akhir = df_sorted.groupby('No.Staf').last().reset_index()
        gabung = berat_awal[['No.Staf', 'Berat (kg)']].merge(
            berat_akhir[['No.Staf', 'Berat (kg)']], on='No.Staf', suffixes=('_awal', '_terkini')
        )
        gabung['% Penurunan'] = ((gabung['Berat (kg)_awal'] - gabung['Berat (kg)_terkini']) / gabung['Berat (kg)_awal']) * 100
        gabung['% Penurunan'] = gabung['% Penurunan'].round(2)

        # Dapatkan purata penurunan ikut sesi akhir peserta
        sesi_terkini = df_sorted.groupby('No.Staf').last().reset_index()[['No.Staf', 'Sesi']]
        gabung = gabung.merge(sesi_terkini, on='No.Staf', how='left')
        purata_sesi = gabung.groupby('Sesi')['% Penurunan'].mean().reset_index()
        purata_sesi = purata_sesi.sort_values(by='Sesi')

        fig1 = px.line(purata_sesi, x='Sesi', y='% Penurunan', markers=True,
                        title="Purata % Penurunan Berat Mengikut Sesi",
                        labels={'% Penurunan': 'Purata % Penurunan'})
        st.plotly_chart(fig1, use_container_width=True)

        # === Taburan Tahap Penurunan Individu ===
        st.markdown("### 🧮 Taburan Tahap Penurunan Individu")

        def tahap(pct):
            if pct >= 10:
                return ">10% (Cemerlang)"
            elif pct >= 5:
                return "5–9.9% (Baik)"
            elif pct >= 1:
                return "1–4.9% (Sederhana)"
            else:
                return "<1% atau Naik (Perlu Sokongan)"

        gabung['Tahap'] = gabung['% Penurunan'].apply(tahap)
        tabur_tahap = gabung['Tahap'].value_counts().reset_index()
        tabur_tahap.columns = ['Tahap Penurunan', 'Bilangan Peserta']

        fig2 = px.bar(tabur_tahap, x='Tahap Penurunan', y='Bilangan Peserta',
                        color='Tahap Penurunan', title="Bilangan Peserta Mengikut Tahap Penurunan")
        st.plotly_chart(fig2, use_container_width=True)

        st.info("Paparan ini menunjukkan prestasi keseluruhan program secara agregat, tanpa memaparkan data berat sebenar.")


    with tab2:
        st.subheader("Leaderboard")
        df_rank = df_tapis.sort_values("% Penurunan", ascending=False).reset_index(drop=True)
        df_rank["Ranking"] = df_rank.index + 1
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