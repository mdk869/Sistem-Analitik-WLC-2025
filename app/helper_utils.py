# app/helper_utils.py

import streamlit as st
import pandas as pd
import os


# =====================================================
# ✅ Semak Header DataFrame Konsisten
# =====================================================
def check_header_consistency(df, expected_header, nama_sheet):
    df_header = list(df.columns)

    missing = [h for h in expected_header if h not in df_header]
    extra = [h for h in df_header if h not in expected_header]

    if missing or extra:
        st.error(f"❌ {nama_sheet}: Struktur kolum tidak padan dengan template.")
        if missing:
            st.warning(f"🛑 Kolum **TIADA**: {missing}")
        if extra:
            st.warning(f"⚠️ Kolum **TERLEBIH**: {extra}")
        return False
    return True


# =====================================================
# ✅ Simpan DataFrame ke Excel (Local Backup)
# =====================================================
def save_dataframe_to_excel(df, filename):
    df.to_excel(filename, index=False)


# =====================================================
# ✅ Semak & Buat Folder
# =====================================================
def check_or_create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


# =====================================================
# ✅ Simpan Fail dalam Folder
# =====================================================
def save_file_in_folder(folder_name, filename, df):
    check_or_create_folder(folder_name)
    filepath = os.path.join(folder_name, filename)
    df.to_excel(filepath, index=False)
    return filepath


# =====================================================
# ✅ Format Nama Fail Gambar Timbang
# =====================================================
def format_nama_fail_gambar(nama, tarikh, berat):
    tarikh_str = pd.to_datetime(tarikh).strftime('%Y-%m-%d')
    nama_bersih = nama.replace(" ", "_")
    fail = f"{nama_bersih}_{tarikh_str}_{berat}kg.jpg"
    return fail


# =====================================================
# ✅ Label Status BMI (Extra untuk UI)
# =====================================================
def kategori_bmi_asia(bmi):
    if bmi is None:
        return "Tidak Sah"
    elif bmi < 18.5:
        return "Kurang Berat Badan"
    elif 18.5 <= bmi <= 22.9:
        return "Normal"
    elif 23.0 <= bmi <= 24.9:
        return "Lebih Berat Badan"
    elif 25.0 <= bmi <= 29.9:
        return "Obesiti Tahap 1"
    elif 35 <= bmi <= 39.9:
        return "Obesiti Tahap 2"
    else:
        return "Obesiti Morbid"

def kira_bmi(berat, tinggi):
    if berat is None or tinggi is None or tinggi == 0:
        return None
    tinggi_meter = tinggi / 100
    bmi = berat / (tinggi_meter ** 2)
    return round(bmi, 1)

# ===========================================================
# ✅ Bersihkan Data — Semua Whitespace
# ===========================================================
def bersihkan_whitespace(df: pd.DataFrame) -> pd.DataFrame:
    """
    Buang whitespace di semua nilai string dalam dataframe.
    """
    return df.applymap(lambda x: x.strip() if isinstance(x, str) else x)


# ===========================================================
# ✅ Tukar Kolum kepada Numerik (Contoh: Berat, Tinggi)
# ===========================================================
def bersihkan_numerik(df: pd.DataFrame, kolum_list: list) -> pd.DataFrame:
    """
    Tukar kolum kepada format numerik. Jika error, tukar jadi NaN.
    """
    for kolum in kolum_list:
        if kolum in df.columns:
            df[kolum] = pd.to_numeric(df[kolum], errors="coerce")
    return df


# ===========================================================
# ✅ Semak Status Timbangan
# ===========================================================
def check_sudah_timbang(row) -> str:
    """
    Return 'Sudah Timbang' jika BeratTerkini dan TarikhTimbang tidak kosong.
    """
    return (
        "Sudah Timbang"
        if all([
            pd.notnull(row["BeratTerkini"]),
            str(row["BeratTerkini"]).strip() != "",
            pd.notnull(row["TarikhTimbang"]),
            str(row["TarikhTimbang"]).strip() != ""
        ])
        else "Belum Timbang"
    )


# ===========================================================
# ✅ Pipeline Bersihkan dan Semak Status Timbangan
# ===========================================================
def proses_data_peserta(df: pd.DataFrame) -> pd.DataFrame:
    """
    Bersihkan whitespace, tukar berat/tinggi ke numerik, dan kira status timbang.
    """
    df = bersihkan_whitespace(df)
    df = bersihkan_numerik(df, ["Tinggi", "BeratAwal", "BeratTerkini"])

    # Tambah kolum StatusTimbang
    df["StatusTimbang"] = df.apply(check_sudah_timbang, axis=1)

    return df


# ===========================================================
# ✅ Semak Header
# ===========================================================
def check_header_consistency(df: pd.DataFrame, header_list: list, label: str = "Data") -> bool:
    """
    Pastikan header dataframe sama seperti yang dijangka.
    """
    df_header = list(df.columns)
    if all(col in df_header for col in header_list):
        return True
    else:
        print(f"❌ {label}: Header tidak konsisten. Sila semak header Google Sheet.")
        print(f"Expected: {header_list}")
        print(f"Found: {df_header}")
        return False
