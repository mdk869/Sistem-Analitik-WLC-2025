# helper_logic.py
import pandas as pd

def kira_bmi(berat, tinggi):
    try:
        return round(berat / ((tinggi / 100) ** 2), 1)
    except:
        return None

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

def tambah_kiraan_peserta(df):
    df["PenurunanKg"] = df["BeratAwal"] - df["BeratTerkini"]
    df["% Penurunan"] = (df["PenurunanKg"] / df["BeratAwal"] * 100).round(2)
    df["BMI"] = df.apply(lambda row: kira_bmi(row["BeratTerkini"], row["Tinggi"]) 
                        if pd.notna(row["BeratTerkini"]) and pd.notna(row["Tinggi"]) else None, axis=1)
    df["KategoriBMI"] = df["BMI"].apply(kategori_bmi_asia)
    return df
