import pandas as pd
import streamlit as st
from datetime import datetime
from app.helper_logic import kira_bmi, kategori_bmi_asia
from app.helper_gsheet import (
    load_worksheet_to_df,
    save_df_to_worksheet,
    append_row_to_worksheet,
    update_baris_dalam_worksheet,
    delete_baris_dalam_worksheet
)
from app.helper_connection import connect_drive, connect_gspread

# =========================================
# ✅ Spreadsheet Settings
# =========================================
SPREADSHEET_PESERTA = st.secrets["spreadsheet"]["data_peserta_id"]

SHEET_PESERTA = "peserta"

# =========================================
# ✅ Load Data Peserta
# =========================================
def load_data_peserta():
    df = load_worksheet_to_df(SPREADSHEET_PESERTA, SHEET_PESERTA)
    df = sync_berat_dari_rekod(df)
    return df

# =========================================
# ✅ Load Semua Rekod Berat (semua sheet rekod_berat_*)
# =========================================
def load_rekod_berat_semua():
    sh = connect_gspread(SPREADSHEET_PESERTA)
    sheet_list = [ws.title for ws in sh.worksheets() if ws.title.startswith("rekod_berat_")]

    dfs = []
    for sheet in sheet_list:
        df = load_worksheet_to_df(SPREADSHEET_PESERTA, sheet)
        if not df.empty:
            df["Sheet"] = sheet
            dfs.append(df)

    if dfs:
        return pd.concat(dfs, ignore_index=True)
    else:
        return pd.DataFrame(columns=["Nama", "Tarikh", "Berat", "Sheet"])

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
# ✅ Simpan Rekod Berat (ke sheet rekod_berat_*)
# =========================================
def simpan_rekod_berat(data):
    # Tetapkan sheet nama ikut bulan contoh: rekod_berat_Jun2025
    tarikh_obj = pd.to_datetime(data["Tarikh"])
    sheet_bulan = f"rekod_berat_{tarikh_obj.strftime('%b%Y')}"

    # Buat sheet jika belum wujud
    try:
        sh = connect_gspread(SPREADSHEET_PESERTA)
        sheet_names = [ws.title for ws in sh.worksheets()]
        if sheet_bulan not in sheet_names:
            sh.add_worksheet(title=sheet_bulan, rows=1000, cols=10)
    except:
        pass

    # Simpan rekod timbang
    data_rekod = {
        "Nama": data["Nama"],
        "Tarikh": data["Tarikh"],
        "Berat": data["Berat"]
    }
    append_row_to_worksheet(SPREADSHEET_PESERTA, sheet_bulan, data_rekod)

    return True

# =========================================
# ✅ Padam Peserta
# =========================================
def padam_peserta_dari_sheet(nostaf):
    delete_baris_dalam_worksheet(SPREADSHEET_PESERTA, SHEET_PESERTA, "NoStaf", nostaf)

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
# ✅ Sync Berat Terkini & Tarikh Timbang
# =========================================
def sync_berat_dari_rekod(df_peserta):
    rekod = load_rekod_berat_semua()
    if rekod.empty:
        return df_peserta

    rekod["Tarikh"] = pd.to_datetime(rekod["Tarikh"], errors="coerce")
    rekod = rekod.dropna(subset=["Tarikh"])

    rekod_sorted = rekod.sort_values(by="Tarikh", ascending=False).drop_duplicates(subset=["Nama"])

    for _, row in rekod_sorted.iterrows():
        idx = df_peserta[df_peserta["Nama"].str.lower() == str(row["Nama"]).lower()].index
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
