# app/helper_utils.py

import streamlit as st
import pandas as pd
import os


# =====================================================
# ✅ Semak Header DataFrame Konsisten
# =====================================================
def check_header_consistency(df: pd.DataFrame, expected_header: list, label: str = "Data") -> bool:
    df_header = list(df.columns)

    missing = [h for h in expected_header if h not in df_header]
    extra = [h for h in df_header if h not in expected_header]

    if missing or extra:
        st.error(f"❌ {label}: Struktur kolum tidak padan dengan template.")
        if missing:
            st.warning(f"🛑 Kolum **TIADA**: {missing}")
        if extra:
            st.warning(f"⚠️ Kolum **TERLEBIH**: {extra}")
        return False

    return True


# =====================================================
# ✅ Simpan DataFrame ke Excel (Backup Local)
# =====================================================
def save_dataframe_to_excel(df: pd.DataFrame, filename: str):
    try:
        df.to_excel(filename, index=False)
        st.success(f"✅ Berjaya simpan fail ke {filename}")
    except Exception as e:
        st.error(f"❌ Gagal simpan fail ke {filename}: {e}")


# =====================================================
# ✅ Semak & Buat Folder
# =====================================================
def check_or_create_folder(folder_name: str):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


# =====================================================
# ✅ Simpan Fail dalam Folder
# =====================================================
def save_file_in_folder(folder_name: str, filename: str, df: pd.DataFrame) -> str:
    check_or_create_folder(folder_name)
    filepath = os.path.join(folder_name, filename)
    save_dataframe_to_excel(df, filepath)
    return filepath


# =====================================================
# ✅ Format Nama Fail Gambar Timbang
# =====================================================
def format_nama_fail_gambar(nama: str, tarikh: str, berat: float) -> str:
    tarikh_str = pd.to_datetime(tarikh).strftime('%Y-%m-%d')
    nama_bersih = nama.replace(" ", "_")
    fail = f"{nama_bersih}_{tarikh_str}_{berat}kg.jpg"
    return fail


# =====================================================
# ✅ Label Status BMI (Untuk UI)
# =====================================================
def kategori_bmi_asia(bmi: float) -> str:
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
    elif 30.0 <= bmi <= 34.9:
        return "Obesiti Tahap 2"
    else:
        return "Obesiti Morbid"


def kira_bmi(berat: float, tinggi: float) -> float:
    if berat is None or tinggi is None or tinggi == 0:
        return None
    tinggi_meter = tinggi / 100
    bmi = berat / (tinggi_meter ** 2)
    return round(bmi, 1)


# =====================================================
# ✅ Bersihkan Data — Whitespace
# =====================================================
def bersihkan_whitespace(df: pd.DataFrame) -> pd.DataFrame:
    return df.applymap(lambda x: x.strip() if isinstance(x, str) else x)


# =====================================================
# ✅ Tukar Kolum kepada Numerik
# =====================================================
def bersihkan_numerik(df: pd.DataFrame, kolum_list: list) -> pd.DataFrame:
    for kolum in kolum_list:
        if kolum in df.columns:
            df[kolum] = pd.to_numeric(df[kolum], errors="coerce")
    return df


# =====================================================
# ✅ Semak Status Timbangan
# =====================================================
def check_sudah_timbang(row) -> str:
    return (
        "Sudah Timbang"
        if all([
            pd.notnull(row.get("BeratTerkini")),
            str(row.get("BeratTerkini")).strip() != "",
            pd.notnull(row.get("TarikhTimbang")),
            str(row.get("TarikhTimbang")).strip() != ""
        ])
        else "Belum Timbang"
    )


# =====================================================
# ✅ Pipeline Bersihkan dan Semak Status Timbangan
# =====================================================
def proses_data_peserta(df: pd.DataFrame) -> pd.DataFrame:
    df = bersihkan_whitespace(df)
    df = bersihkan_numerik(df, ["Tinggi", "BeratAwal", "BeratTerkini"])
    df["StatusTimbang"] = df.apply(check_sudah_timbang, axis=1)
    return df


# =====================================================
# ✅ Fungsi Carian Nama dengan Auto Suggestion
# =====================================================
def carian_nama_suggestion(df: pd.DataFrame, label: str = "Cari Nama", key: str = "") -> str:
    nama_list = df["Nama"].dropna().tolist()

    nama_input = st.text_input(f"🔍 {label}", key=f"input_{key}").strip()

    suggestion = [nama for nama in nama_list if nama_input.lower() in nama.lower()] if nama_input else []

    if nama_input and suggestion:
        nama_pilih = st.selectbox("✔️ Pilih dari cadangan", suggestion, key=f"select_{key}")
        return nama_pilih
    elif nama_input and not suggestion:
        st.warning("❌ Tiada padanan nama ditemui.")
        return None
    else:
        return None
<<<<<<< HEAD
=======

>>>>>>> parent of 95b04d2 (update utils dan get_worksheet)
