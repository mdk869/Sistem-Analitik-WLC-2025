# app/helper_logic.py
import pandas as pd

def kira_bmi(berat, tinggi):
    """Kira BMI berdasarkan berat dan tinggi (dalam cm)."""
    try:
        return round(berat / ((tinggi / 100) ** 2), 1)
    except:
        return None

def kategori_bmi_asia(bmi):
    """Pulangkan kategori BMI mengikut piawaian Asia."""
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

def kira_status_ranking(row):
    """Tentukan status ranking peserta: Naik, Turun, Kekal atau Baru."""
    if pd.isna(row["Ranking_Lama"]):
        return "🆕 Baru"
    elif row["Ranking"] < row["Ranking_Lama"]:
        return "🔺 Naik"
    elif row["Ranking"] > row["Ranking_Lama"]:
        return "🔻 Turun"
    else:
        return "⏸️ Kekal"

# Untuk import automatik dari modul
__all__ = [
    "kira_bmi",
    "kategori_bmi_asia",
    "kira_status_ranking"
]
