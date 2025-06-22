# app/helper_logic.py
import pandas as pd

def kira_bmi(berat: float, tinggi_cm: float) -> float:
    tinggi_m = tinggi_cm / 100
    return round(berat / (tinggi_m ** 2), 1)

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

def tambah_kiraan_peserta(df):
    """Tambah kolum pengiraan BMI dan penurunan berat ke dalam DataFrame."""
    df["PenurunanKg"] = df["BeratAwal"] - df["BeratTerkini"]
    df["% Penurunan"] = (df["PenurunanKg"] / df["BeratAwal"] * 100).round(2)
    df["BMI"] = df.apply(lambda row: kira_bmi(row["BeratTerkini"], row["Tinggi"]), axis=1)
    df["KategoriBMI"] = df["BMI"].apply(kategori_bmi_asia)
    return df


# Untuk import automatik dari modul
__all__ = [
    "kira_bmi",
    "kategori_bmi_asia",
    "tambah_kiraan_peserta"
]