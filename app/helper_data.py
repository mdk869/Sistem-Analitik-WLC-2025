# app/helper_data.py

import streamlit as st
import pandas as pd
import datetime
from app.helper_connection import SPREADSHEET_PESERTA, get_worksheet
from app.helper_utils import save_dataframe_to_excel, kategori_bmi_asia, get_column_index
from app.helper_log import log_dev, log_error


# ------------------------------------
# ✅ Fungsi Load Data Peserta
# ------------------------------------
def load_data_peserta():
    try:
        ws = get_worksheet(SPREADSHEET_PESERTA, "peserta")
        data = ws.get_all_records()
        df = pd.DataFrame(data)

        if df.empty:
            st.warning("🚫 Data peserta kosong.")
        return df

    except Exception as e:
        st.error(f"❌ Gagal load data peserta: {e}")
        return pd.DataFrame()

def load_data_cloud_or_local():
    try:
        ws = get_worksheet(SPREADSHEET_PESERTA, "peserta")
        data = ws.get_all_records()
        df = pd.DataFrame(data)

        if df.empty:
            st.warning("🚫 Data peserta kosong.")
        return df

    except Exception as e:
        st.error(f"❌ Gagal load data peserta: {e}")
        return pd.DataFrame()
    
# ------------------------------------
# ✅ Simpan Dataframe ke Sheet Peserta
# ------------------------------------
def save_data_peserta(df):
    try:
        ws = get_worksheet(SPREADSHEET_PESERTA, "peserta")
        ws.clear()

        ws.update([df.columns.values.tolist()] + df.values.tolist())
        st.success("✅ Data peserta berjaya disimpan ke Google Sheet.")

    except Exception as e:
        st.error(f"❌ Gagal simpan data peserta: {e}")


# ------------------------------------
# ✅ Fungsi Backup Data Peserta ke Excel
# ------------------------------------
def backup_data_peserta(df):
    try:
        filename = f"backup_data_peserta_{datetime.datetime.now().strftime('%Y%m%d')}.xlsx"
        save_dataframe_to_excel(df, filename)
        st.info(f"📦 Backup data peserta disimpan: {filename}")
        return filename
    except Exception as e:
        st.error(f"❌ Gagal backup data: {e}")


# ------------------------------------
# ✅ Tambah Peserta Baru
# ------------------------------------
def tambah_peserta_google_sheet(nama, nostaf, umur, jantina, jabatan, tinggi, berat_awal, tarikh_daftar):
    df = load_data_peserta()

    berat_terkini = berat_awal
    bmi = round(berat_awal / ((tinggi / 100) ** 2), 2)
    kategori = kategori_bmi_asia(bmi)

    new_data = {
        "Nama": nama,
        "NoStaf": nostaf,
        "Umur": umur,
        "Jantina": jantina,
        "Jabatan": jabatan,
        "Tinggi": tinggi,
        "BeratAwal": berat_awal,
        "TarikhDaftar": str(tarikh_daftar),
        "BeratTerkini": berat_terkini,
        "TarikhTimbang": str(tarikh_daftar),
        "BMI": bmi,
        "Kategori": kategori,
    }

    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    save_data_peserta(df)


# ------------------------------------
# ✅ Kemaskini Berat Terkini Peserta
# ------------------------------------
def kemaskini_berat_peserta(nama, berat_baru, tarikh_baru):
    df = load_data_peserta()

    if nama in df['Nama'].values:
        idx = df[df['Nama'] == nama].index[0] 
        df.at[idx, 'BeratTerkini'] = berat_baru
        df.at[idx, 'TarikhTimbang'] = str(tarikh_baru)

        tinggi = df.at[idx, 'Tinggi']
        bmi = round(berat_baru / ((tinggi / 100) ** 2), 2)
        kategori = kategori_bmi_asia(bmi)

        df.at[idx, 'BMI'] = bmi
        df.at[idx, 'Kategori'] = kategori

        save_data_peserta(df)
    else:
        st.error("❌ Nama peserta tidak dijumpai.")


# ------------------------------------
# ✅ Padam Peserta dari Sheet
# ------------------------------------
def padam_peserta_dari_sheet(nama):
    df = load_data_peserta()

    if nama in df['Nama'].values:
        df = df[df['Nama'] != nama]
        save_data_peserta(df)
        return True
    else:
        st.warning("⚠️ Nama tidak dijumpai dalam senarai.")
        return False


# ------------------------------------
# ✅ Simpan Rekod Berat
# ------------------------------------
def simpan_rekod_berat(nama, tarikh, berat):
    """
    Simpan data ke worksheet 'rekod_berat' (append row).
    """
    try:
        ws = get_worksheet(SPREADSHEET_PESERTA, "rekod_berat")
        ws.append_row([nama, tarikh, berat])
        log_dev("Admin", f"Rekod berat {nama} pada {tarikh} disimpan", "Success")
        return True
    except Exception as e:
        st.error(f"❌ Gagal simpan rekod berat: {e}")
        log_error(str(e))
        return False


# -----------------------------------------------
# ✅ Update Berat Terkini ke Sheet Peserta
# -----------------------------------------------
def update_berat_terkini_peserta(nama, tarikh, berat):
    """
    Update BeratTerkini dan TarikhTimbang pada worksheet peserta.
    """
    try:
        ws = get_worksheet(SPREADSHEET_PESERTA, "peserta")
        data = ws.get_all_records()

        # Cari index row peserta
        for idx, row in enumerate(data):
            if row["Nama"].strip() == nama.strip():
                ws.update_cell(idx + 2, get_column_index(ws, "BeratTerkini"), berat)
                ws.update_cell(idx + 2, get_column_index(ws, "TarikhTimbang"), tarikh)
                log_dev("Admin", f"Update berat terkini {nama} pada {tarikh}", "Success")
                return True

        st.warning(f"⚠️ Nama {nama} tidak ditemui dalam senarai peserta.")
        return False

    except Exception as e:
        st.error(f"❌ Gagal update berat terkini: {e}")
        log_error(str(e))
        return False

