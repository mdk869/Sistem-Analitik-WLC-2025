# helper_logic.py
import pandas as pd
from app.helper_utils import kategori_bmi_asia, kira_bmi


# === Tambah Kiraan BMI dan % Penurunan Berat ===
def tambah_kiraan_peserta(df):
    df = df.copy()

    # Pastikan kolum numeric
    df['Tinggi'] = pd.to_numeric(df['Tinggi'], errors='coerce')
    df['BeratAwal'] = pd.to_numeric(df['BeratAwal'], errors='coerce')
    df['BeratTerkini'] = pd.to_numeric(df['BeratTerkini'], errors='coerce')

    # Kiraan Penurunan
    df["PenurunanKg"] = (df["BeratAwal"] - df["BeratTerkini"]).round(2).fillna(0)
    df["% Penurunan"] = ((df["PenurunanKg"] / df["BeratAwal"]) * 100).round(2).fillna(0)

    # BMI dan kategori
    df["BMI"] = df.apply(lambda row: kira_bmi(row["BeratTerkini"], row["Tinggi"]), axis=1)
    df["KategoriBMI"] = df["BMI"].apply(kategori_bmi_asia)

    return df


# === Kiraan Status Berat (Naik/Turun/Kekal) ===
def kira_status_ranking(berat_awal, berat_terkini):
    try:
        if pd.isna(berat_terkini):
            return "Belum"
        if berat_terkini < berat_awal:
            return "Turun"
        elif berat_terkini > berat_awal:
            return "Naik"
        else:
            return "Kekal"
    except:
        return "Belum"


# === Export Fungsi ===
__all__ = [
    "tambah_kiraan_peserta",
    "kira_status_ranking"
]
