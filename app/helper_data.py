import pandas as pd
import streamlit as st
from datetime import datetime
from app.helper_gsheet import (
    load_worksheet_to_df,
    save_df_to_worksheet,
    append_row_to_worksheet,
    create_worksheet_if_not_exist
)
from app.helper_logic import kira_bmi, kategori_bmi_asia
from app.helper_utils import bulan_tahun_nice

# =========================================
# ✅ Konfigurasi Spreadsheet & Sheet
# =========================================
SPREADSHEET_ID = st.secrets["data_peserta_id"]

SHEET_PESERTA = "peserta"

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
    df = load_worksheet_to_df(SPREADSHEET_ID, SHEET_PESERTA)

    if df.empty:
        df = pd.DataFrame(columns=HEADER_PESERTA)

    # Sync BeratTerkini & TarikhTimbang dari rekod timbang
    df = sync_berat_terkini(df)

    return df


# =========================================
# ✅ Simpan Rekod Timbangan
# =========================================
def simpan_rekod_berat(data):
    """
    Simpan rekod timbang ke sheet ikut bulan.
    Contoh sheet: rekod_berat_Jun2025
    """
    sesi = bulan_tahun_nice(datetime.strptime(data["Tarikh"], "%Y-%m-%d"))
    sheet_name = f"rekod_berat_{sesi}"

    # Auto create sheet jika belum ada
    create_worksheet_if_not_exist(SPREADSHEET_ID, sheet_name, HEADER_REKOD)

    row = {
        "Nama": data["Nama"],
        "NoStaf": data["NoStaf"],
        "Tarikh": data["Tarikh"],
        "Berat": data["Berat"]
    }

    append_row_to_worksheet(SPREADSHEET_ID, sheet_name, row)
    return True


# =========================================
# ✅ Load Semua Rekod Timbangan
# =========================================
def load_rekod_berat_semua():
    from app.helper_gsheet import list_worksheets

    sheet_list = list_worksheets(SPREADSHEET_ID)
    rekod_sheets = [s for s in sheet_list if s.startswith("rekod_berat_")]

    df_list = []

    for sheet in rekod_sheets:
        df = load_worksheet_to_df(SPREADSHEET_ID, sheet)
        if not df.empty:
            df["SesiBulan"] = sheet.replace("rekod_berat_", "")
            df_list.append(df)

    if df_list:
        return pd.concat(df_list, ignore_index=True)
    else:
        return pd.DataFrame(columns=HEADER_REKOD + ["SesiBulan"])


# =========================================
# ✅ Sync BeratTerkini & TarikhTimbang ke Sheet Peserta
# =========================================
def sync_berat_terkini(df_peserta):
    df_rekod = load_rekod_berat_semua()

    if df_rekod.empty:
        return df_peserta

    df_rekod["Tarikh"] = pd.to_datetime(df_rekod["Tarikh"])

    rekod_terkini = (
        df_rekod.sort_values("Tarikh")
        .groupby("NoStaf")
        .last()
        .reset_index()
    )

    for idx, row in df_peserta.iterrows():
        no_staf = row["NoStaf"]

        rekod = rekod_terkini[rekod_terkini["NoStaf"] == no_staf]

        if not rekod.empty:
            berat = rekod.iloc[0]["Berat"]
            tarikh = rekod.iloc[0]["Tarikh"]

            bmi = kira_bmi(berat, row["Tinggi"])
            kategori = kategori_bmi_asia(bmi)

            df_peserta.at[idx, "BeratTerkini"] = berat
            df_peserta.at[idx, "TarikhTimbang"] = tarikh.strftime("%Y-%m-%d")
            df_peserta.at[idx, "BMI"] = bmi
            df_peserta.at[idx, "Kategori"] = kategori

    save_df_to_worksheet(SPREADSHEET_ID, SHEET_PESERTA, df_peserta)

    return df_peserta


# =========================================
# ✅ Daftar Peserta Baru
# =========================================
def daftar_peserta(nama, nostaf, umur, jantina, jabatan, tinggi, berat_awal, tarikh):
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
        "TarikhDaftar": str(tarikh),
        "BeratTerkini": berat_awal,
        "TarikhTimbang": str(tarikh),
        "BMI": bmi,
        "Kategori": kategori
    }

    append_row_to_worksheet(SPREADSHEET_ID, SHEET_PESERTA, data)
    return True


# =========================================
# ✅ Update Data Peserta Berdasarkan NoStaf
# =========================================
def update_data_peserta(nostaf, update):
    from app.helper_gsheet import update_baris_dalam_worksheet

    return update_baris_dalam_worksheet(
        SPREADSHEET_ID, SHEET_PESERTA,
        key_column="NoStaf", key_value=nostaf,
        update_dict=update
    )


# =========================================
# ✅ Padam Peserta
# =========================================
def padam_peserta_dari_sheet(nostaf):
    from app.helper_gsheet import padam_baris_dalam_worksheet

    return padam_baris_dalam_worksheet(
        SPREADSHEET_ID, SHEET_PESERTA,
        key_column="NoStaf", key_value=nostaf
    )
