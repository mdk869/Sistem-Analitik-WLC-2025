import pandas as pd
import streamlit as st
from datetime import datetime

from app.helper_logic import kira_bmi, kategori_bmi_asia, kira_berat_ideal, kira_berat_target, kira_target_realistik
from app.helper_gsheet import (
    load_worksheet_to_df,
    save_df_to_worksheet,
    append_row_to_worksheet,
    update_baris_dalam_worksheet,
    delete_baris_dalam_worksheet,
    check_or_create_sheet,
    load_multiple_sheets_by_prefix
)

# =========================================
# ✅ Spreadsheet Settings
# =========================================
SPREADSHEET_PESERTA = st.secrets["gsheet"]["data_peserta_id"]

SHEET_PESERTA = "peserta"
SHEET_PREFIX_REKOD = "rekod_berat_"

HEADER_PESERTA = [
    'Nama', 'NoStaf', 'Umur', 'Jantina', 'Jabatan',
    'Tinggi', 'BeratAwal', 'TarikhDaftar',
    'BeratTerkini', 'TarikhTimbang', 'BMI', 'Kategori'
]

HEADER_REKOD = ['Nama', 'NoStaf', 'Tarikh', 'Berat', 'SesiBulan']


# =========================================
# ✅ Load Data Peserta
# =========================================
def load_data_peserta():
    df = load_worksheet_to_df(SPREADSHEET_PESERTA, SHEET_PESERTA)
    if df.empty:
        df = pd.DataFrame(columns=HEADER_PESERTA)
    else:
        df = sync_berat_dari_rekod(df)
    return df


# =========================================
# ✅ Load Semua Rekod Berat
# =========================================
def load_rekod_berat_semua():
    df = load_multiple_sheets_by_prefix(SPREADSHEET_PESERTA, SHEET_PREFIX_REKOD)
    if df.empty:
        df = pd.DataFrame(columns=HEADER_REKOD)
    return df


# =========================================
# ✅ Daftar Peserta Baru
# =========================================
def daftar_peserta(nama, nostaf, umur, jantina, jabatan, tinggi, berat_awal, tarikh_daftar):
    bmi = kira_bmi(berat_awal, tinggi)
    kategori = kategori_bmi_asia(bmi)

    data = {
        "Nama": nama,
        "NoStaf": nostaf,
        "Umur": umur,
        "Jantina": jantina,
        "Jabatan": jabatan,
        "Tinggi": tinggi,
        "BeratAwal": berat_awal,
        "TarikhDaftar": str(tarikh_daftar),
        "BeratTerkini": berat_awal,
        "TarikhTimbang": str(tarikh_daftar),
        "BMI": bmi,
        "Kategori": kategori
    }

    append_row_to_worksheet(SPREADSHEET_PESERTA, SHEET_PESERTA, data)


# =========================================
# ✅ Simpan Rekod Timbang ke Sheet Bulanan
# =========================================
def simpan_rekod_berat(data):
    """
    Simpan rekod timbang ke sheet bulanan.
    Sheet format: rekod_berat_Jun2025
    """
    tarikh_obj = pd.to_datetime(data["Tarikh"], errors="coerce")
    sesi_bulan = tarikh_obj.strftime('%b%Y')  # Cth: Jun2025
    sheet_bulan = f"{SHEET_PREFIX_REKOD}{sesi_bulan}"

    check_or_create_sheet(SPREADSHEET_PESERTA, sheet_bulan, HEADER_REKOD)

    data_rekod = {
        "Nama": data["Nama"],
        "NoStaf": data["NoStaf"],
        "Tarikh": data["Tarikh"],
        "Berat": data["Berat"],
        "SesiBulan": sesi_bulan
    }

    append_row_to_worksheet(SPREADSHEET_PESERTA, sheet_bulan, data_rekod)

    # ✅ Sync ke data peserta selepas timbang
    sync_berat_terkini(
        nostaf=data["NoStaf"],
        berat=data["Berat"],
        tarikh=data["Tarikh"]
    )

    return True


# =========================================
# ✅ Padam Peserta
# =========================================
def padam_peserta_dari_sheet(nostaf):
    return delete_baris_dalam_worksheet(
        SPREADSHEET_PESERTA, SHEET_PESERTA,
        key_column="NoStaf", key_value=nostaf
    )


# =========================================
# ✅ Update Data Peserta
# =========================================
def update_data_peserta(nostaf, update):
    return update_baris_dalam_worksheet(
        SPREADSHEET_PESERTA, SHEET_PESERTA,
        key_column="NoStaf", key_value=nostaf,
        update_dict=update
    )


# =========================================
# ✅ Sync Berat Terkini & Tarikh Timbang dari Rekod
# =========================================
def sync_berat_dari_rekod(df_peserta):
    rekod = load_rekod_berat_semua()
    if rekod.empty:
        return df_peserta

    rekod["Tarikh"] = pd.to_datetime(rekod["Tarikh"], errors="coerce")
    rekod = rekod.dropna(subset=["Tarikh"])

    rekod_sorted = (
        rekod.sort_values(by="Tarikh", ascending=False)
        .drop_duplicates(subset=["NoStaf"])
    )

    for _, row in rekod_sorted.iterrows():
        idx = df_peserta[df_peserta["NoStaf"] == row["NoStaf"]].index
        if not idx.empty:
            peserta_idx = idx[0]
            df_peserta.at[peserta_idx, "BeratTerkini"] = row["Berat"]
            df_peserta.at[peserta_idx, "TarikhTimbang"] = row["Tarikh"].strftime("%Y-%m-%d")

            tinggi = df_peserta.at[peserta_idx, "Tinggi"]
            bmi = kira_bmi(row["Berat"], tinggi)
            df_peserta.at[peserta_idx, "BMI"] = bmi
            df_peserta.at[peserta_idx, "Kategori"] = kategori_bmi_asia(bmi)

    return df_peserta


# =========================================
# ✅ Sync Berat Semasa (Instant)
# =========================================
def sync_berat_terkini(nostaf, berat, tarikh):
    df = load_data_peserta()
    idx = df[df["NoStaf"] == nostaf].index
    if not idx.empty:
        peserta_idx = idx[0]
        df.at[peserta_idx, "BeratTerkini"] = berat
        df.at[peserta_idx, "TarikhTimbang"] = tarikh

        tinggi = df.at[peserta_idx, "Tinggi"]
        bmi = kira_bmi(berat, tinggi)
        df.at[peserta_idx, "BMI"] = bmi
        df.at[peserta_idx, "Kategori"] = kategori_bmi_asia(bmi)

        save_df_to_worksheet(SPREADSHEET_PESERTA, SHEET_PESERTA, df)


def dataframe_target_penurunan(df):
    data = []

    for _, row in df.iterrows():
        tinggi = row["Tinggi"]
        berat = row["BeratTerkini"]
        nama = row["Nama"]
        kategori = row["Kategori"]

        berat_target = kira_berat_target(tinggi, 24.9)  # Target overweight max
        perlu_turun = max(0, round(berat - berat_target, 2))

        data.append({
            "Nama": nama,
            "Kategori Sekarang": kategori,
            "Berat Sekarang (kg)": berat,
            "Berat Maks (Overweight) (kg)": berat_target,
            "Perlu Turun (kg)": perlu_turun
        })

    df_target = pd.DataFrame(data)
    return df_target.sort_values(by="Perlu Turun (kg)", ascending=False)


def dataframe_status_berat(df):
    data = []

    for _, row in df.iterrows():
        tinggi = row["Tinggi"]
        berat = row["BeratTerkini"]
        nama = row["Nama"]
        kategori = row["Kategori"]

        berat_overweight = kira_berat_target(tinggi, 24.9)
        berat_ideal = kira_berat_ideal(tinggi)

        target_realistik = kira_target_realistik(berat, tinggi)

        perlu_turun_ideal = max(0, round(berat - berat_ideal, 2))
        perlu_turun_realistik = max(0, round(berat - target_realistik, 2))

        data.append({
            "Nama": nama,
            "Kategori Sekarang": kategori,
            "Berat Sekarang (kg)": berat,
            "Target Realistik (kg)": target_realistik,
            "Perlu Turun (Realistik) (kg)": perlu_turun_realistik,
            "Berat Ideal (kg)": berat_ideal,
            "Perlu Turun (Ideal) (kg)": perlu_turun_ideal
        })

    df_status = pd.DataFrame(data)
    return df_status.sort_values(by="Perlu Turun (Realistik) (kg)", ascending=False)
