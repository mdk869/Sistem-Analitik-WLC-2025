import pandas as pd
from datetime import datetime
import streamlit as st
from app.helper_connection import (
    load_worksheet_to_df,
    save_df_to_worksheet,
    append_row_to_worksheet,
    check_sheet_exist,
    create_sheet_with_header,
    get_all_sheet_names

)
from app.helper_logic import kira_bmi, kategori_bmi_asia

# ✅ Spreadsheet ID
SPREADSHEET_PESERTA = st.secrets["spreadsheet"]["data_peserta_id"]
SPREADSHEET_REKOD = st.secrets["spreadsheet"]["rekod_ranking"]


# ===============================================
# ✅ Nama Sheet Rekod Ikut Bulan
# ===============================================
def nama_sheet_rekod(tarikh):
    return f"rekod_berat_{tarikh.strftime('%b%Y')}"


# ===============================================
# ✅ Load Data Peserta (Dengan Auto Sync Berat)
# ===============================================
def load_data_peserta():
    df = load_worksheet_to_df(SPREADSHEET_PESERTA, "peserta")
    if df.empty:
        return pd.DataFrame(columns=[
            'Nama', 'NoStaf', 'Umur', 'Jantina', 'Jabatan',
            'Tinggi', 'BeratAwal', 'TarikhDaftar',
            'BeratTerkini', 'TarikhTimbang', 'BMI', 'Kategori'
        ])

    df = sync_berat_terkini(df)
    return df


# ===============================================
# ✅ Load Semua Rekod Berat Semua Bulan
# ===============================================
def load_rekod_berat_semua():
    sheet_list = get_all_sheet_names(SPREADSHEET_REKOD)
    rekod_sheets = [s for s in sheet_list if s.startswith("rekod_berat_")]

    df_list = []
    for sheet in rekod_sheets:
        df = load_worksheet_to_df(SPREADSHEET_REKOD, sheet)
        if not df.empty:
            df["SesiBulan"] = sheet.replace("rekod_berat_", "")
            df_list.append(df)

    if df_list:
        return pd.concat(df_list, ignore_index=True)
    return pd.DataFrame(columns=["Nama", "Tarikh", "Berat", "SesiBulan"])


# ===============================================
# ✅ Sync BeratTerkini & TarikhTimbang ke Peserta
# ===============================================
def sync_berat_terkini(data_peserta):
    df_rekod = load_rekod_berat_semua()

    if df_rekod.empty:
        return data_peserta

    df_rekod["Tarikh"] = pd.to_datetime(df_rekod["Tarikh"])
    latest_rekod = df_rekod.sort_values("Tarikh").groupby("Nama").last().reset_index()

    data_peserta = data_peserta.copy()
    data_peserta["BeratTerkini"] = data_peserta["Nama"].map(
        latest_rekod.set_index("Nama")["Berat"]
    )
    data_peserta["TarikhTimbang"] = data_peserta["Nama"].map(
        latest_rekod.set_index("Nama")["Tarikh"].dt.strftime("%Y-%m-%d")
    )

    # Auto kira BMI & kategori
    data_peserta["BMI"] = data_peserta.apply(
        lambda x: kira_bmi(x["BeratTerkini"], x["Tinggi"]) if pd.notna(x["BeratTerkini"]) else None,
        axis=1
    )
    data_peserta["Kategori"] = data_peserta["BMI"].apply(
        lambda x: kategori_bmi_asia(x) if pd.notna(x) else None
    )

    return data_peserta


# ===============================================
# ✅ Simpan Rekod Timbang
# ===============================================
def simpan_rekod_berat(data):
    """
    data = {
        "Nama": str,
        "NoStaf": str,
        "Tarikh": str (format YYYY-MM-DD),
        "Berat": float,
        "SesiBulan": str (format YYYY-MM)
    }
    """
    tarikh = datetime.strptime(data["Tarikh"], "%Y-%m-%d")
    sheet_nama = nama_sheet_rekod(tarikh)

    # Check & create sheet jika tiada
    if not check_sheet_exist(SPREADSHEET_REKOD, sheet_nama):
        create_sheet_with_header(SPREADSHEET_REKOD, sheet_nama, ["Nama", "Tarikh", "Berat"])

    # Simpan rekod
    append_row_to_worksheet(
        SPREADSHEET_REKOD,
        sheet_nama,
        {"Nama": data["Nama"], "Tarikh": data["Tarikh"], "Berat": data["Berat"]}
    )
    return True


# ===============================================
# ✅ Daftar Peserta Baru
# ===============================================
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

    append_row_to_worksheet(SPREADSHEET_PESERTA, "peserta", data)
    return True


# ===============================================
# ✅ Padam Peserta
# ===============================================
def padam_peserta_dari_sheet(nostaf):
    df = load_worksheet_to_df(SPREADSHEET_PESERTA, "peserta")
    df = df[df["NoStaf"] != nostaf]
    save_df_to_worksheet(SPREADSHEET_PESERTA, "peserta", df)
    return True


# ===============================================
# ✅ Update Data Peserta Berdasarkan NoStaf
# ===============================================
def update_data_peserta(nostaf, update_dict):
    df = load_worksheet_to_df(SPREADSHEET_PESERTA, "peserta")
    if df.empty:
        return False

    index = df[df["NoStaf"] == nostaf].index
    if not index.empty:
        idx = index[0]
        for col, value in update_dict.items():
            if col in df.columns:
                df.at[idx, col] = value
        save_df_to_worksheet(SPREADSHEET_PESERTA, "peserta", df)
        return True
    return False
