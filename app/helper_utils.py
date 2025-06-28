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
    if bmi < 18.5:
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

