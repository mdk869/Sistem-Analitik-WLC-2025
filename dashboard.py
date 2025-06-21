import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime
import time

# Laluan changelog
FILE_CHANGELOG = os.path.join(os.path.dirname(__file__), "changelog_wlc2025.html")

# ==== Laluan Fail Excel Secara Relatif Berdasarkan Lokasi Fail Ini ====
DIR_SEMASA = os.path.dirname(os.path.abspath(__file__))
FILE_EXCEL = os.path.join(DIR_SEMASA, "peserta.xlsx")
FILE_REKOD = os.path.join(DIR_SEMASA, "rekod_ranking_semasa.xlsx")
FILE_REKOD_BERAT = os.path.join(DIR_SEMASA, "rekod_berat.xlsx")

# ==== Setup Page ====
st.set_page_config(page_title="Dashboard WLC 2025", layout="wide")
st.title("📊 Dashboard Weight Loss Challenge 2025")

# ==== Auto Refresh Manual ====
if st.button("🔄 Refresh Data"):
    st.experimental_rerun()

# ==== Masa Kemaskini Terakhir ====
st.caption(f"⏱️ Kemaskini terakhir: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

# ==== Cipta Fail Sejarah Berat jika belum ada ====
if not os.path.exists(FILE_REKOD_BERAT):
    df_dummy = pd.DataFrame({"Nama": [], "Tarikh": [], "Berat": [], "BMI": []})
    df_dummy.to_excel(FILE_REKOD_BERAT, index=False)

# ==== Semak Kewujudan Fail Excel ====
if os.path.exists(FILE_EXCEL):
    df = pd.read_excel(FILE_EXCEL)

    df["PenurunanKg"] = df["BeratAwal"] - df["BeratTerkini"]
    df["% Penurunan"] = (df["PenurunanKg"] / df["BeratAwal"] * 100).round(2)

    def kira_bmi(berat, tinggi):
        try:
            return round(berat / ((tinggi / 100) ** 2), 1)
        except:
            return None

    df["BMI"] = df.apply(lambda row: kira_bmi(row["BeratTerkini"], row["Tinggi"]) if pd.notna(row["BeratTerkini"]) and pd.notna(row["Tinggi"]) else None, axis=1)

    def kategori_bmi_asia(bmi):
        if pd.isna(bmi):
            return None
        elif bmi < 18.5:
            return "Kurang Berat Badan"
        elif 18.5 <= bmi <= 24.9:
            return "Normal"
        elif 25 <= bmi <= 29.9:
            return "Lebih Berat Badan"
        elif 30 <= bmi <= 34.9:
            return "Obesiti Tahap 1"
        elif 35 <= bmi <= 39.9:
            return "Obesiti Tahap 2"
        else:
            return "Obesiti Morbid"

    df["KategoriBMI"] = df["BMI"].apply(kategori_bmi_asia)

    Kategori = st.sidebar.multiselect("Pilih Kategori", options=df["Kategori"].dropna().unique(), default=df["Kategori"].dropna().unique())
    jantina = st.sidebar.multiselect("Pilih Jantina", options=df["Jantina"].dropna().unique(), default=df["Jantina"].dropna().unique())

    df_tapis = df[(df["Kategori"].isin(Kategori)) & (df["Jantina"].isin(jantina))]

    total_peserta = df_tapis.shape[0]
    purata_bmi = df_tapis["BMI"].mean().round(1)
    purata_penurunan = df_tapis["% Penurunan"].mean().round(2)
    purata_kg = df_tapis["PenurunanKg"].mean().round(2)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Jumlah Peserta", total_peserta)
    col2.metric("Purata BMI", purata_bmi)
    col3.metric("Purata % Penurunan", f"{purata_penurunan}%")
    col4.metric("Purata Penurunan Berat", f"{purata_kg}kg")

    tab1, tab2, tab3 = st.tabs(["📉 Penurunan Berat", "🏆 Leaderboard", "🧍‍♂️ BMI"])

    with tab1:
        st.subheader("Perbandingan Berat Setiap Peserta")
        df_plot = df_tapis.sort_values("PenurunanKg", ascending=False)
        fig = px.bar(df_plot,
                     x="Nama",
                     y=["BeratAwal", "BeratTerkini"],
                     barmode="group",
                     title="Perbandingan Berat Awal dan Terkini Setiap Peserta",
                     labels={"value": "Berat (kg)", "variable": "Kategori Berat"})
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("🏆 Leaderboard: % Penurunan Berat")
        df_leaderboard = df_tapis.sort_values("% Penurunan", ascending=False).reset_index(drop=True)
        df_leaderboard["Ranking"] = df_leaderboard.index + 1

        if os.path.exists(FILE_REKOD):
            rekod_lama = pd.read_excel(FILE_REKOD)
            df_leaderboard = df_leaderboard.merge(rekod_lama, on="Nama", how="left", suffixes=("", "_Lama"))

            def kira_status(row):
                if pd.isna(row["Ranking_Lama"]):
                    return "🆕 Baru"
                if row["Ranking"] < row["Ranking_Lama"]:
                    return "🔺 Naik"
                elif row["Ranking"] > row["Ranking_Lama"]:
                    return "🔻 Turun"
                else:
                    return "⏸️ Kekal"

            df_leaderboard["Status"] = df_leaderboard.apply(kira_status, axis=1)
        else:
            df_leaderboard["Status"] = "-"

        st.dataframe(df_leaderboard[["Ranking", "Nama", "% Penurunan", "BeratAwal", "BeratTerkini", "Status"]], use_container_width=True, hide_index=True)

        if st.button("💾 Simpan Ranking Semasa"):
            rekod_df = df_leaderboard[["Nama", "Ranking"]]
            rekod_df.to_excel(FILE_REKOD, index=False)
            st.success(f"Ranking telah disimpan ke fail: {FILE_REKOD}")

        with st.expander("🔐 Akses Maklumat Individu"):
            nama_pilihan = st.selectbox("📌 Pilih Nama Peserta:", df_leaderboard["Nama"])
            peserta_info = df[df["Nama"] == nama_pilihan].iloc[0]

            st.markdown(f"### 🧾 Maklumat Peserta: {nama_pilihan}")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"- **Tinggi:** {peserta_info['Tinggi']} cm")
                st.write(f"- **Berat Awal:** {peserta_info['BeratAwal']} kg")
            with col2:
                st.write(f"- **Berat Terkini:** {peserta_info['BeratTerkini']} kg")
                st.write(f"- **BMI Semasa:** {peserta_info['BMI']}")

            if os.path.exists(FILE_REKOD_BERAT):
                df_rekod = pd.read_excel(FILE_REKOD_BERAT)
                df_sejarah = df_rekod[df_rekod["Nama"] == nama_pilihan]

                if not df_sejarah.empty:
                    st.markdown("### 📈 Sejarah Berat & BMI")
                    fig = px.line(df_sejarah, x="Tarikh", y=["Berat", "BMI"], markers=True)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Tiada rekod sejarah berat untuk peserta ini.")

    with tab3:
        st.subheader("📊 Analisis BMI Peserta")

        col1, col2, col3, col4, col5, col6 = st.columns(6)
        col1.metric("Kurang Berat Badan", (df_tapis["KategoriBMI"] == "Kurang Berat Badan").sum())
        col2.metric("Normal", (df_tapis["KategoriBMI"] == "Normal").sum())
        col3.metric("Lebih Berat Badan", (df_tapis["KategoriBMI"] == "Lebih Berat Badan").sum())
        col4.metric("Obesiti Tahap 1", (df_tapis["KategoriBMI"] == "Obesiti Tahap 1").sum())
        col5.metric("Obesiti Tahap 2", (df_tapis["KategoriBMI"] == "Obesiti Tahap 2").sum())
        col6.metric("Obesiti Morbid", (df_tapis["KategoriBMI"] == "Obesiti Morbid").sum())

        Kategori_df = df_tapis.groupby("KategoriBMI").size().reset_index(name="Bilangan")
        fig = px.pie(Kategori_df, names="KategoriBMI", values="Bilangan", title="Peratus Peserta Mengikut Tahap BMI")
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("📋 Lihat Senarai Nama Peserta Mengikut Kategori BMI"):
            df_bmi_table = df_tapis[["Nama", "BMI", "KategoriBMI"]].sort_values("KategoriBMI", na_position="last").reset_index(drop=True)
            df_bmi_table.index = df_bmi_table.index + 1
            st.dataframe(df_bmi_table, use_container_width=True)

    # ==== Footer / Copyright ====
# Garis pemisah
st.markdown("---")

# Gaya footer responsif
footer_col1, footer_col2 = st.columns([0.7, 0.3])

with footer_col1:
    st.markdown("""
    <div style='font-size:15px;'>
        <strong>📊 Sistem Analitik WLC 2025</strong> <br>
        Versi: <code>v1.0</code> | Dibangunkan oleh <strong>Mr.K</strong> <br>
        &copy; 2025 Semua Hak Cipta Terpelihara
    </div>
    """, unsafe_allow_html=True)

with footer_col2:
    if st.button("📄 Lihat Log Perubahan"):
        if os.path.exists(FILE_CHANGELOG):
            with open(FILE_CHANGELOG, "r", encoding="utf-8") as f:
                changelog_html = f.read()
            st.components.v1.html(changelog_html, height=800, scrolling=True)
        else:
            st.warning("❗ Fail changelog tidak dijumpai.")

# Optional: Tarikh dan masa paparan terakhir
st.markdown(f"<p style='text-align:right;font-size:12px;color:gray;'>📅 Dikemaskini pada: {datetime.datetime.now().strftime('%d %B %Y, %I:%M %p')}</p>", unsafe_allow_html=True)
