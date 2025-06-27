import pandas as pd
import numpy as np
from datetime import datetime
import streamlit as st

from app.helper_data import load_data_peserta, get_berat_terkini, load_ranking_bulanan
from app.helper_log import log_dev


# === Fungsi: Kira Peratus Penurunan Berat ===
def kira_peratus_turun(berat_awal, berat_semasa):
    try:
        return round(((berat_awal - berat_semasa) / berat_awal) * 100, 2)
    except:
        return 0


# === Fungsi: Generate Leaderboard Semasa ===
def generate_leaderboard():
    try:
        df_peserta = load_data_peserta()
        df_berat = get_berat_terkini()

        if df_berat.empty:
            st.warning("Rekod berat kosong.")
            return pd.DataFrame()

        df = pd.merge(df_peserta, df_berat, on="Nama", how="left")
        df["% Turun"] = df.apply(lambda x: kira_peratus_turun(x["BeratAwal"], x["Berat"]), axis=1)

        df = df.sort_values(by="% Turun", ascending=False).reset_index(drop=True)
        df["Ranking"] = df.index + 1

        df = df[["Ranking", "Nama", "Jabatan", "BeratAwal", "Berat", "% Turun", "Tarikh"]]
        log_dev("Generate Leaderboard", "Leaderboard semasa berjaya dijana")
        return df

    except Exception as e:
        st.error(f"Gagal jana leaderboard: {e}")
        log_dev("Generate Leaderboard", f"Gagal jana leaderboard: {e}")
        return pd.DataFrame()


# === Fungsi: Banding Ranking Dengan Bulan Sebelum ===
def tambah_status_ranking(df_current, bulan_sebelum):
    df_previous = load_ranking_bulanan(bulan_sebelum)

    if df_previous is None or df_previous.empty:
        df_current["Status"] = "Baru"
        return df_current

    df_merge = pd.merge(
        df_current[["Nama", "Ranking"]],
        df_previous[["Nama", "Ranking"]],
        on="Nama",
        how="left",
        suffixes=("", "_Sebelum")
    )

    def kira_status(row):
        if pd.isna(row["Ranking_Sebelum"]):
            return "Baru"
        elif row["Ranking"] < row["Ranking_Sebelum"]:
            return "Naik"
        elif row["Ranking"] > row["Ranking_Sebelum"]:
            return "Turun"
        else:
            return "Mendatar"

    df_merge["Status"] = df_merge.apply(kira_status, axis=1)
    df_final = pd.merge(df_current, df_merge[["Nama", "Status"]], on="Nama", how="left")

    return df_final


# === Fungsi: Papar Leaderboard Lengkap Dengan Status ===
def leaderboard_dengan_status():
    bulan_ini = datetime.now().strftime('%Y-%m')
    tahun, bulan = bulan_ini.split("-")

    # Kira bulan sebelum
    bulan_int = int(bulan) - 1
    if bulan_int == 0:
        bulan_int = 12
        tahun = str(int(tahun) - 1)

    bulan_sebelum = f"{tahun}-{bulan_int:02d}"

    df_current = generate_leaderboard()
    if df_current.empty:
        return pd.DataFrame()

    df_final = tambah_status_ranking(df_current, bulan_sebelum)

    return df_final


# === Fungsi: Papar Sejarah Ranking Individu ===
def sejarah_ranking(nama):
    try:
        sheets = st.session_state.get("ranking_sheets", [])
        if not sheets:
            sheets = []

        sejarah = []
        for sheet in sheets:
            df = load_ranking_bulanan(sheet[-7:])
            if df is not None and not df.empty:
                df_nama = df[df["Nama"] == nama]
                if not df_nama.empty:
                    sejarah.append({
                        "Bulan": sheet[-7:],
                        "Ranking": int(df_nama["Ranking"].values[0]),
                        "% Turun": df_nama["% Turun"].values[0]
                    })

        df_sejarah = pd.DataFrame(sejarah)
        df_sejarah = df_sejarah.sort_values("Bulan")
        return df_sejarah

    except Exception as e:
        st.warning(f"Gagal dapatkan sejarah ranking: {e}")
        return pd.DataFrame()
