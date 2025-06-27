# app/helper_ranking.py

import pandas as pd
from datetime import datetime
from app.helper_utils import kira_bmi, kategori_bmi_asia
from app.helper_data import (
    load_data_peserta,
    get_berat_terkini,
    load_data_ranking_bulanan,
    simpan_data_ranking_bulanan,
    check_or_create_worksheet
)
from app.helper_log import log_dev


# === Generate Leaderboard Semasa ===
def generate_leaderboard():
    df_peserta = load_data_peserta()
    df_berat = get_berat_terkini()

    if df_berat.empty:
        return pd.DataFrame()

    df = pd.merge(df_peserta, df_berat, on="Nama", how="left")
    df["% Penurunan"] = df.apply(
        lambda x: round(((x["BeratAwal"] - x["BeratTerkini"]) / x["BeratAwal"]) * 100, 2)
        if x["BeratTerkini"] > 0 else 0,
        axis=1
    )

    df = df.sort_values(by="% Penurunan", ascending=False).reset_index(drop=True)
    df["Ranking"] = df.index + 1

    df = df[["Ranking", "Nama", "Jabatan", "BeratAwal", "BeratTerkini", "% Penurunan", "TarikhTimbang"]]
    log_dev("Generate Leaderboard", "Leaderboard semasa berjaya dijana")
    return df


# === Leaderboard Dengan Status (Naik/Turun/Baru) ===
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

    df_previous = load_ranking_bulan(bulan_sebelum)

    if df_previous is not None and not df_previous.empty:
        df_merge = pd.merge(
            df_current[["Nama", "Ranking"]],
            df_previous[["Nama", "Ranking"]],
            on="Nama",
            how="left",
            suffixes=("", "_Sebelum")
        )

        df_merge["Trend"] = df_merge.apply(
            lambda x: kira_trend(x["Ranking"], x["Ranking_Sebelum"]), axis=1
        )
    else:
        df_merge = df_current.copy()
        df_merge["Trend"] = "🆕"

    df_merge["Ranking_Label"] = df_merge["Ranking"].apply(tambah_medal)
    df_merge["Ranking_Trend"] = df_merge["Ranking_Label"] + " " + df_merge["Trend"]

    df_final = pd.merge(df_current, df_merge[["Nama", "Ranking_Trend"]], on="Nama", how="left")

    return df_final


# === Simpan Ranking Bulanan ===
def simpan_ranking_bulanan(df_ranking):
    bulan_ini = datetime.now().strftime('%Y-%m')
    df_simpan = df_ranking[["Nama", "Ranking"]].copy()
    df_simpan["Bulan"] = bulan_ini

    df_ranking_bulanan = load_data_ranking_bulanan()

    if df_ranking_bulanan is not None:
        df_ranking_bulanan = pd.concat([df_ranking_bulanan, df_simpan], ignore_index=True)
    else:
        df_ranking_bulanan = df_simpan

    simpan_data_ranking_bulanan(df_ranking_bulanan)
    log_dev("Simpan Ranking", f'Ranking bulan {bulan_ini} berjaya disimpan')


# === Load Ranking Bulan Tertentu ===
def load_ranking_bulan(bulan):
    df_ranking = load_data_ranking_bulanan()

    if df_ranking is not None and bulan in df_ranking["Bulan"].values:
        df_bulan = df_ranking[df_ranking["Bulan"] == bulan].copy()
        return df_bulan[["Nama", "Ranking"]].reset_index(drop=True)
    else:
        return None


# === Load Ranking Bulan Terakhir ===
def load_ranking_terakhir():
    df_ranking = load_data_ranking_bulanan()

    if df_ranking is not None and not df_ranking.empty:
        bulan_terakhir = sorted(df_ranking["Bulan"].unique())[-1]
        return load_ranking_bulan(bulan_terakhir)
    else:
        return None


# === Sejarah Ranking Individu ===
def sejarah_ranking(nama):
    df_ranking = load_data_ranking_bulanan()

    if df_ranking is None or df_ranking.empty:
        return pd.DataFrame()

    df_nama = df_ranking[df_ranking["Nama"] == nama][["Bulan", "Ranking"]]
    df_nama = df_nama.sort_values("Bulan")
    return df_nama.reset_index(drop=True)


# === Kiraan Trend Naik/Turun untuk Leaderboard ===
def kira_trend(ranking_semasa, ranking_sebelum):
    if pd.isna(ranking_sebelum):
        return "🆕"
    elif ranking_semasa < ranking_sebelum:
        return "📈"
    elif ranking_semasa > ranking_sebelum:
        return "📉"
    else:
        return "➖"


# === Medal 🥇🥈🥉 ===
def tambah_medal(rank):
    if rank == 1:
        return "🥇"
    elif rank == 2:
        return "🥈"
    elif rank == 3:
        return "🥉"
    else:
        return str(rank)



# === Export Fungsi ===
__all__ = [
    "generate_leaderboard",
    "leaderboard_dengan_status",
    "simpan_ranking_bulanan",
    "load_ranking_bulan",
    "load_ranking_terakhir",
    "sejarah_ranking",
]
