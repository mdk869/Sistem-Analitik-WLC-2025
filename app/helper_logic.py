# app/helper_logic.py

import pandas as pd
from app.helper_utils import kira_bmi, kategori_bmi_asia

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

# === Export Fungsi ===
__all__ = [
    "kira_bmi",
    "kategori_bmi_asia",
    "tambah_kiraan_peserta",
    "kira_status_ranking",
    "kira_trend",
    "tambah_medal"
]
