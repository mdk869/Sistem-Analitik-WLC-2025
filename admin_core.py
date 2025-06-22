# admin_core.py

from database import (
    baca_data,
    tambah_baris,
    simpan_semula,
    kemaskini_baris,
    padam_baris
)
from utils.bmi import kira_bmi, kategori_bmi
from datetime import datetime
import pandas as pd


# ========== 1. Tambah Peserta ==========

def proses_tambah_peserta(data: dict):
    """
    Proses tambah peserta ke sheet 'peserta'.
    Data input dalam format dict:
    {
        "Nama": "...",
        "No Staf": "...",
        "Jantina": "...",
        "Tinggi": ... (dalam cm),
        "Berat Awal": ... (kg)
    }
    """
    berat = data["Berat Awal"]
    tinggi = data["Tinggi"]
    
    bmi = kira_bmi(berat, tinggi)
    kategori = kategori_bmi(bmi)
    tarikh = datetime.today().strftime("%Y-%m-%d")

    peserta_baru = {
        "Nama": data["Nama"],
        "No Staf": data["No Staf"],
        "Jantina": data["Jantina"],
        "Tinggi": tinggi,
        "Berat Awal": berat,
        "BMI": bmi,
        "Kategori": kategori,
        "Tarikh Daftar": tarikh
    }

    tambah_baris("peserta", peserta_baru)
    return peserta_baru


# ========== 2. Dapatkan Senarai Peserta ==========

def dapatkan_senarai_peserta():
    return baca_data("peserta")


# ========== 3. Kemaskini Maklumat Peserta ==========

def proses_kemaskini_peserta(no_staf: str, data: dict):
    """
    Kemaskini maklumat peserta berdasarkan No Staf.
    data = {"Nama": "...", "Tinggi": ..., "Berat Awal": ..., "Jantina": "..."}
    """
    if "Berat Awal" in data and "Tinggi" in data:
        bmi = kira_bmi(data["Berat Awal"], data["Tinggi"])
        kategori = kategori_bmi(bmi)
        data["BMI"] = bmi
        data["Kategori"] = kategori

    berjaya = kemaskini_baris("peserta", "No Staf", no_staf, data)
    return berjaya


# ========== 4. Padam Peserta ==========

def proses_padam_peserta(no_staf: str):
    """
    Padam peserta dari Sheet berdasarkan No Staf
    """
    padam_baris("peserta", "No Staf", no_staf)
    return True

