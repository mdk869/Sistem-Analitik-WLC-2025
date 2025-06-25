import pandas as pd


# === Kiraan BMI ===
def kira_bmi(berat: float, tinggi_cm: float) -> float:
    tinggi_m = tinggi_cm / 100
    return round(berat / (tinggi_m ** 2), 1)


# === Kategori BMI Asia ===
def kategori_bmi_asia(bmi: float) -> str:
    if bmi < 18.5:
        return "Kurang Berat Badan"
    elif 18.5 <= bmi <= 22.9:
        return "Normal"
    elif 23 <= bmi <= 27.4:
        return "Lebih Berat Badan"
    elif 27.5 <= bmi <= 34.9:
        return "Obesiti Tahap 1"
    elif 35 <= bmi <= 39.9:
        return "Obesiti Tahap 2"
    else:
        return "Obesiti Morbid"


# === Kiraan % Penurunan Berat dan BMI ===
def tambah_kiraan_peserta(df):
    df = df.copy()

    # Isi BeratTerkini kosong dengan BeratAwal (jika peserta tiada rekod baru)
    df["BeratTerkini"] = df["BeratTerkini"].fillna(df["BeratAwal"])

    # Kiraan
    df["PenurunanKg"] = df["BeratAwal"] - df["BeratTerkini"]
    df["% Penurunan"] = (df["PenurunanKg"] / df["BeratAwal"] * 100).round(2)

    df["BMI"] = df.apply(
        lambda row: kira_bmi(row["BeratTerkini"], row["Tinggi"]),
        axis=1
    )
    df["KategoriBMI"] = df["BMI"].apply(kategori_bmi_asia)

    return df



# === Kiraan Status Timbang (Naik, Turun, Kekal) ===
def kira_status_ranking(berat_awal, berat_terkini):
    if berat_terkini < berat_awal:
        return "Turun"
    elif berat_terkini > berat_awal:
        return "Naik"
    else:
        return "Kekal"


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


# === Leaderboard Utama ===
def proses_leaderboard(df_tapis, df_ranking_sebelum=None):
    """
    Proses dataframe leaderboard berdasarkan % penurunan.
    Tambah ranking dan trend naik/turun.
    """
    df_rank = df_tapis.sort_values("% Penurunan", ascending=False).reset_index(drop=True)
    df_rank["Ranking"] = df_rank.index + 1

    if df_ranking_sebelum is not None:
        df_merge = df_rank.merge(
            df_ranking_sebelum[["Nama", "Ranking"]],
            on="Nama",
            how="left",
            suffixes=('', '_Sebelum')
        )
        df_merge["Trend"] = df_merge.apply(
            lambda x: kira_trend(x["Ranking"], x["Ranking_Sebelum"]), axis=1
        )
    else:
        df_merge = df_rank.copy()
        df_merge["Trend"] = "🆕"

    df_merge["Ranking_Label"] = df_merge["Ranking"].apply(tambah_medal)
    df_merge["Ranking_Trend"] = df_merge["Ranking_Label"] + " " + df_merge["Trend"]

    return df_merge


# === Untuk import automatik dari modul ===
__all__ = [
    "kira_bmi",
    "kategori_bmi_asia",
    "tambah_kiraan_peserta",
    "kira_status_ranking",
    "kira_trend",
    "tambah_medal",
    "proses_leaderboard"
]
