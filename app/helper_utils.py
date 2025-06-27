# app/helper_utils.py

from datetime import datetime
import pytz


# === Tarikh & Masa Lokal Malaysia ===
def get_tarikh_masa():
    tz = pytz.timezone('Asia/Kuala_Lumpur')
    return datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

def get_bulan_sekarang():
    tz = pytz.timezone('Asia/Kuala_Lumpur')
    return datetime.now(tz).strftime('%Y-%m')


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


# === Kiraan % Penurunan Berat ===
def kira_peratus_turun(berat_awal, berat_semasa):
    try:
        return round(((berat_awal - berat_semasa) / berat_awal) * 100, 2)
    except:
        return 0


# === Untuk import automatik ===
__all__ = [
    "get_tarikh_masa",
    "get_bulan_sekarang",
    "kira_bmi",
    "kategori_bmi_asia",
    "kira_peratus_turun"
]
