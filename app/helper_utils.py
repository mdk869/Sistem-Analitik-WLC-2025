from datetime import datetime
import pytz
import pandas as pd


# === Tarikh & Masa Lokal Malaysia ===
def get_tarikh_masa():
    tz = pytz.timezone('Asia/Kuala_Lumpur')
    return datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

def get_bulan_sekarang():
    tz = pytz.timezone('Asia/Kuala_Lumpur')
    return datetime.now(tz).strftime('%Y-%m')


# === Check atau Auto Create Worksheet ===
def check_or_create_worksheet(sheet, name, header):
    try:
        ws = sheet.worksheet(name)
    except:
        ws = sheet.add_worksheet(title=name, rows="1000", cols="20")
        ws.append_row(header)
    return ws


# === Kiraan BMI ===
def kira_bmi(berat: float, tinggi_cm: float) -> float:
    tinggi_m = tinggi_cm / 100
    return round(berat / (tinggi_m ** 2), 1)


# === Kategori BMI ===
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


# === Kiraan Trend Naik/Turun ===
def kira_trend(ranking_semasa, ranking_sebelum):
    if ranking_sebelum is None or pd.isna(ranking_sebelum):
        return "🆕"
    elif ranking_semasa < ranking_sebelum:
        return "📈"
    elif ranking_semasa > ranking_sebelum:
        return "📉"
    else:
        return "➖"


# === Label Medal 🥇🥈🥉 ===
def tambah_medal(rank):
    if rank == 1:
        return "🥇"
    elif rank == 2:
        return "🥈"
    elif rank == 3:
        return "🥉"
    else:
        return str(rank)


# === Kiraan % Penurunan Berat ===
def kira_peratus_turun(berat_awal, berat_semasa):
    try:
        return round(((berat_awal - berat_semasa) / berat_awal) * 100, 2)
    except:
        return 0


# === Export Fungsi ===
__all__ = [
    "get_tarikh_masa",
    "get_bulan_sekarang",
    "check_or_create_worksheet",
    "kira_bmi",
    "kategori_bmi_asia",
    "kira_trend",
    "tambah_medal",
    "kira_peratus_turun"
]
