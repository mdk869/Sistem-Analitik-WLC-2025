# app/helper_logic.py

import pandas as pd
from app.helper_utils import kira_bmi, kategori_bmi_asia


# ===========================================
# ✅ Fungsi Tambah Kiraan Peserta
# ===========================================
def tambah_kiraan_peserta(df):
    if df.empty:
        return df

    df = df.copy()

    # Tukar kolum berat ke numeric, jika ada error atau kosong → NaN
    df["BeratAwal"] = pd.to_numeric(df["BeratAwal"], errors="coerce")
    df["BeratTerkini"] = pd.to_numeric(df["BeratTerkini"], errors="coerce")
    df["Tinggi"] = pd.to_numeric(df["Tinggi"], errors="coerce")

    # === Kiraan Penurunan KG ===
    df["PenurunanKg"] = (df["BeratAwal"] - df["BeratTerkini"]).round(2)

    # Jika BeratTerkini kosong → NaN Penurunan
    df.loc[df["BeratTerkini"].isna(), "PenurunanKg"] = 0

    # === Kiraan % Penurunan ===
    df["% Penurunan"] = (df["PenurunanKg"] / df["BeratAwal"] * 100).round(4)
    df.loc[df["BeratAwal"] == 0, "% Penurunan"] = 0
    df["% Penurunan"] = df["% Penurunan"].fillna(0)

    # === Kiraan BMI ===
    df["BMI"] = df.apply(
        lambda row: kira_bmi(row["BeratTerkini"], row["Tinggi"])
        if not pd.isna(row["BeratTerkini"]) else kira_bmi(row["BeratAwal"], row["Tinggi"]),
        axis=1
    )

    # === Kategori BMI ===
    df["KategoriBMI"] = df["BMI"].apply(kategori_bmi_asia)

    return df

# ===========================================
# ✅ Fungsi Penapis Data Sudah & Belum Timbang
# ===========================================
def tapis_sudah_timbang(df):
    return df[df["TarikhTimbang"].notna()]


def tapis_belum_timbang(df):
    return df[df["TarikhTimbang"].isna()]


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
    "tambah_kiraan_peserta",
    "kira_status_ranking"
]
