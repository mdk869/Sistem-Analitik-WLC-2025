# app/helper_utils.py

from datetime import datetime
from typing import Optional
import pytz
import pandas as pd


# ============================================
# ✅ Tarikh & Masa Lokal Malaysia
# ============================================
def get_tarikh_masa() -> str:
    tz = pytz.timezone('Asia/Kuala_Lumpur')
    return datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')


def get_bulan_sekarang() -> str:
    tz = pytz.timezone('Asia/Kuala_Lumpur')
    return datetime.now(tz).strftime('%Y-%m')


# ============================================
# ✅ Check atau Auto Create Worksheet
# ============================================
def check_or_create_worksheet(sheet, name, header):
    try:
        ws = sheet.worksheet(name)
    except:
        ws = sheet.add_worksheet(title=name, rows="1000", cols="20")
        ws.append_row(header)
    return ws


# ============================================
# ✅ Kiraan BMI
# ============================================
def kira_bmi(berat: Optional[float], tinggi: Optional[float]) -> Optional[float]:
    if berat is None or tinggi is None or tinggi <= 0:
        return None
    tinggi_meter = tinggi / 100
    bmi = berat / (tinggi_meter ** 2)
    return round(bmi, 2)


# ============================================
# ✅ Kategori BMI (Standard Asia)
# ============================================
def kategori_bmi_asia(bmi: Optional[float]) -> str:
    if bmi is None:
        return "Tiada Data"
    if bmi < 18.5:
        return "Kurang Berat Badan"
    elif 18.5 <= bmi <= 22.9:
        return "Normal"
    elif 23 <= bmi <= 24.9:
        return "Lebih Berat Badan"
    elif 25 <= bmi <= 29.9:
        return "Obesiti Tahap 1"
    elif 30 <= bmi <= 39.9:
        return "Obesiti Tahap 2"
    else:
        return "Obesiti Morbid"


# ============================================
# ✅ Tambah Medal
# ============================================
def tambah_medal(rank: int) -> str:
    if rank == 1:
        return "🥇"
    elif rank == 2:
        return "🥈"
    elif rank == 3:
        return "🥉"
    else:
        return str(rank)


# ============================================
# ✅ Kira Trend Ranking
# ============================================
def kira_trend(ranking_now: Optional[int], ranking_before: Optional[float]) -> str:
    if ranking_before is None or pd.isna(ranking_before):
        return "🆕"
    elif ranking_now < ranking_before:
        return "🔼"
    elif ranking_now > ranking_before:
        return "🔽"
    else:
        return "➡️"


# ============================================
# ✅ Label Ranking dengan Medal + Trend
# ============================================
def label_ranking(rank: int, trend: str) -> str:
    return f"{tambah_medal(rank)} {trend}"


# ============================================
# ✅ Kira % Penurunan Berat
# ============================================
def kira_peratus_turun(berat_awal: float, berat_semasa: float) -> float:
    if berat_awal == 0 or berat_semasa is None:
        return 0
    return round(((berat_awal - berat_semasa) / berat_awal) * 100, 2)


# ============================================
# ✅ Export Fungsi
# ============================================
__all__ = [
    "get_tarikh_masa",
    "get_bulan_sekarang",
    "check_or_create_worksheet",
    "kira_bmi",
    "kategori_bmi_asia",
    "tambah_medal",
    "kira_trend",
    "label_ranking",
    "kira_peratus_turun"
]
