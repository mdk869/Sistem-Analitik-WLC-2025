# app/helper_utils.py

from datetime import datetime
import pytz
import pandas as pd


# ============================================
# ✅ Tarikh & Masa Lokal Malaysia
# ============================================
def get_tarikh_masa():
    tz = pytz.timezone('Asia/Kuala_Lumpur')
    return datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')


def get_bulan_sekarang():
    tz = pytz.timezone('Asia/Kuala_Lumpur')
    return datetime.now(tz).strftime('%Y-%m')


def check_or_create_worksheet(sheet, name, header):
    try:
        ws = sheet.worksheet(name)
    except:
        ws = sheet.add_worksheet(title=name, rows="1000", cols=str(len(header)))
        ws.append_row(header)
    return ws


# ============================================
# ✅ Kiraan BMI
# ============================================
def kira_bmi(berat: float, tinggi_cm: float) -> float:
    tinggi_m = tinggi_cm / 100
    return round(berat / (tinggi_m ** 2), 1)


# ============================================
# ✅ Kategori BMI (Standard Asia)
# ============================================
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


# ============================================
# ✅ Kiraan Trend Naik/Turun
# ============================================
def kira_trend(ranking_semasa, ranking_sebelum):
    if ranking_sebelum is None or pd.isna(ranking_sebelum):
        return "🆕"
    elif ranking_semasa < ranking_sebelum:
        return "📈"
    elif ranking_semasa > ranking_sebelum:
        return "📉"
    else:
        return "➖"


# ============================================
# ✅ Label Medal 🥇🥈🥉
# ============================================
def tambah_medal(rank):
    if rank == 1:
        return "🥇"
    elif rank == 2:
        return "🥈"
    elif rank == 3:
        return "🥉"
    else:
        return str(rank)


def check_header_consistency(dataframe, expected_header, nama_sheet="Data"):
    """
    Semak samada header dataframe adalah sama seperti expected header.
    
    Args:
        dataframe (pd.DataFrame): Data yang dibaca dari Google Sheet
        expected_header (list): Senarai header yang sepatutnya
        nama_sheet (str): Nama sheet untuk paparan mesej

    Returns:
        bool: True jika sama, False jika tidak
    """
    df_header = list(dataframe.columns)
    missing = [h for h in expected_header if h not in df_header]
    extra = [h for h in df_header if h not in expected_header]

    if missing or extra:
        st.error(f"❌ {nama_sheet}: Struktur kolum tidak padan dengan template.")
        if missing:
            st.warning(f"🛑 Kolum **TIADA**: {missing}")
        if extra:
            st.info(f"ℹ️ Kolum **LEBIH**: {extra}")
        st.write("📑 Header dalam dataframe:", df_header)
        return False
    else:
        st.success(f"✅ {nama_sheet}: Struktur kolum adalah betul.")
        return True


# ============================================
# ✅ Export Fungsi
# ============================================
__all__ = [
    "get_tarikh_masa",
    "get_bulan_sekarang",
    "kira_bmi",
    "kategori_bmi_asia",
    "kira_trend",
    "tambah_medal",
]
