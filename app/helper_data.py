import pandas as pd
import streamlit as st
from datetime import datetime

from app.helper_logic import kira_bmi, kategori_bmi_asia
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

HEADER_REKOD = ['Nama', 'NoStaf', 'Tarikh', 'Berat']


# =========================================
# ✅ Load Data Peserta
# =========================================
def load_data_peserta():
    df = load_worksheet_to_df(SPREADSHEET_PESERTA, SHEET_PESERTA)
    if not df.empty:
        df = sync_berat_dari_rekod(df)
    return df


# =========================================
# ✅ Load Semua Rekod Berat
# =========================================
def load_rekod_berat_semua():
    df = load_multiple_sheets_by_prefix(SPREADSHEET_PESERTA, SHEET_PREFIX_REKOD)
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
    tarikh_obj = pd.to_datetime(data["Tarikh"])
    sheet_bulan = f"{SHEET_PREFIX_REKOD}{tarikh_obj.strftime('%B%Y')}"

    # Check or create sheet
    check_or_create_sheet(SPREADSHEET_PESERTA, sheet_bulan, HEADER_REKOD)

    # Simpan rekod
    data_rekod = {
        "Nama": data["Nama"],
        "NoStaf": data["NoStaf"],
        "Tarikh": data["Tarikh"],
        "Berat": data["Berat"]
    }

    append_row_to_worksheet(SPREADSHEET_PESERTA, sheet_bulan, data_rekod)

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

    # Convert Tarikh
    rekod["Tarikh"] = pd.to_datetime(rekod["Tarikh"], errors="coerce")
    rekod = rekod.dropna(subset=["Tarikh"])

    # Ambil rekod timbang paling terkini ikut NoStaf
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

            # Auto update BMI & Kategori
            tinggi = df_peserta.at[peserta_idx, "Tinggi"]
            bmi = kira_bmi(row["Berat"], tinggi)
            df_peserta.at[peserta_idx, "BMI"] = bmi
            df_peserta.at[peserta_idx, "Kategori"] = kategori_bmi_asia(bmi)

    return df_peserta
