# app/helper_logic.py

import pandas as pd


# === Kiraan BMI ===
def kira_bmi(berat: float, tinggi_cm: float) -> float:
    tinggi_m = tinggi_cm / 100
    return round(berat / (tinggi_m ** 2), 1)


# === Kategori BMI Mengikut Asia ===
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


# === Tambah Kiraan BMI dan % Penurunan Berat ===
def tambah_kiraan_peserta(df):
    df["PenurunanKg"] = (df["BeratAwal"] - df["BeratTerkini"]).round(2)
    df["% Penurunan"] = ((df["PenurunanKg"] / df["BeratAwal"]) * 100).round(2)
    df["BMI"] = df.apply(lambda row: kira_bmi(row["BeratTerkini"], row["Tinggi"]), axis=1)
    df["KategoriBMI"] = df["BMI"].apply(kategori_bmi_asia)
    return df


# === Kiraan Status Berat (Naik/Turun/Kekal) ===
def kira_status_ranking(berat_awal, berat_terkini):
    if berat_terkini < berat_awal:
        return "Turun"
    elif berat_terkini > berat_awal:
        return "Naik"
    else:
        return "Kekal"


# === Kiraan Trend Naik/Turun Ranking ===
def kira_trend(ranking_semasa, ranking_sebelum):
    if pd.isna(ranking_sebelum):
        return "🆕"
    elif ranking_semasa < ranking_sebelum:
        return "📈"
    elif ranking_semasa > ranking_sebelum:
        return "📉"
    else:
        return "➖"


# === Tambah Label Medal 🥇🥈🥉 ===
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
    "kira_bmi",
    "kategori_bmi_asia",
    "tambah_kiraan_peserta",
    "kira_status_ranking",
    "kira_trend",
    "tambah_medal"
]
