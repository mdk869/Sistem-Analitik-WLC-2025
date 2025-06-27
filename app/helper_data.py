# app/helper_data.py
import pandas as pd
import streamlit as st
from app.helper_connection import SHEET_PESERTA
from app.helper_log import log_dev

from app.helper_utils import (
    kira_bmi,
    kategori_bmi_asia,
    check_or_create_worksheet
)

# ============================================
# ✅ Load Data Peserta
# ============================================
def load_data_peserta():
    try:
        ws = SHEET_PESERTA.worksheet("data_peserta")
        data = ws.get_all_records()

        if not data:
            st.warning("⚠️ Data peserta kosong!")
            return pd.DataFrame()

        df = pd.DataFrame(data)

        log_dev("Load Data", "Data peserta berjaya dimuat naik")

        return df

    except Exception as e:
        st.error(f"❌ Gagal load data peserta: {e}")
        return pd.DataFrame()

# ============================================
# ✅ Load Berat Terkini
# ============================================
def get_berat_terkini():
    try:
        ws = SHEET_PESERTA.worksheet("rekod_berat")
        data = ws.get_all_records()

        if not data:
            st.warning("⚠️ Data rekod berat kosong!")
            return pd.DataFrame()

        df = pd.DataFrame(data)

        return df

    except Exception as e:
        st.error(f"❌ Gagal load rekod berat: {e}")
        return pd.DataFrame()

# =============================
# ✅ Load Data Cloud or Local
# =============================
def load_data_cloud_or_local():
    df = load_data_peserta()

    if df.empty:
        st.warning("⚠️ Gagal load dari Google Sheet. Cuba load dari backup Excel...")
        try:
            df = pd.read_excel("data_peserta_backup.xlsx")
            st.info("✅ Data dimuat dari backup Excel.")
        except Exception as e:
            st.error(f"❌ Backup Excel tidak ditemui atau gagal dibaca: {e}")
            return pd.DataFrame()

    return df


# =============================
# ✅ Save Backup Excel
# =============================
def save_backup_excel(df):
    try:
        df.to_excel("data_peserta_backup.xlsx", index=False)
        st.success("✅ Backup Excel berjaya disimpan.")
    except Exception as e:
        st.error(f"❌ Gagal simpan backup Excel: {e}")


# =============================
# ✅ Save to Google Sheet
# =============================
def save_data_to_gsheet(df):
    try:
        worksheet = sheet.worksheet("peserta")
        worksheet.clear()

        # Tulis header + data
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())

        st.success("✅ Data berjaya disimpan ke Google Sheet.")

    except Exception as e:
        st.error(f"❌ Gagal simpan ke Google Sheet: {e}")


# =============================
# ✅ Tambah Peserta
# =============================
def tambah_peserta_google_sheet(nama, nostaf, umur, jantina, jabatan, tinggi, berat_awal, tarikh_daftar):
    try:
        berat_terkini = berat_awal
        tarikh_timbang = tarikh_daftar
        bmi = kira_bmi(berat_awal, tinggi)
        kategori = kategori_bmi_asia(bmi)

        data_baru = [
            nama, nostaf, umur, jantina, jabatan, tinggi,
            berat_awal, str(tarikh_daftar), berat_terkini,
            str(tarikh_timbang), bmi, kategori
        ]

        ws_peserta.append_row(data_baru)
        ws_rekod.append_row([nama, str(tarikh_timbang), berat_terkini])

        st.success(f"✅ Peserta {nama} berjaya ditambah.")
    except Exception as e:
        st.error(f"Gagal tambah peserta: {e}")


# =============================
# ✅ Kemaskini Berat
# =============================
def kemaskini_berat_peserta(nama, berat_baru, tarikh_baru):
    try:
        data = ws_peserta.get_all_records()

        for idx, row in enumerate(data):
            if row["Nama"] == nama:
                bmi_baru = kira_bmi(berat_baru, row["Tinggi"])
                kategori_baru = kategori_bmi_asia(bmi_baru)

                ws_peserta.update(f"I{idx+2}", berat_baru)         # BeratTerkini
                ws_peserta.update(f"J{idx+2}", str(tarikh_baru))   # TarikhTimbang
                ws_peserta.update(f"K{idx+2}", bmi_baru)           # BMI
                ws_peserta.update(f"L{idx+2}", kategori_baru)      # Kategori
                break

        ws_rekod.append_row([nama, str(tarikh_baru), berat_baru])

        st.success(f"✅ Berat {nama} berjaya dikemaskini.")
    except Exception as e:
        st.error(f"Gagal kemaskini berat: {e}")


# =============================
# ✅ Padam Peserta
# =============================
def padam_peserta_dari_sheet(nama):
    try:
        data = ws_peserta.get_all_records()

        for idx, row in enumerate(data):
            if row["Nama"] == nama:
                ws_peserta.delete_rows(idx + 2)
                st.success(f"✅ Peserta {nama} berjaya dipadam.")
                return True

        st.warning(f"❌ Peserta {nama} tidak ditemui.")
        return False
    except Exception as e:
        st.error(f"Gagal padam peserta: {e}")
        return False


# =============================
# ✅ Get Berat Terkini
# =============================
def get_berat_terkini():
    try:
        df_rekod = load_rekod_berat()
        if df_rekod.empty:
            return pd.DataFrame(columns=["Nama", "Berat", "Tarikh"])

        df_rekod["Tarikh"] = pd.to_datetime(df_rekod["Tarikh"], errors="coerce")

        df_latest = (
            df_rekod.sort_values('Tarikh', ascending=False)
            .drop_duplicates('Nama')
            .reset_index(drop=True)
        )

        return df_latest[["Nama", "Berat", "Tarikh"]]
    except Exception as e:
        st.error(f"Gagal dapatkan berat terkini: {e}")
        return pd.DataFrame(columns=["Nama", "Berat", "Tarikh"])


# =============================
# ✅ Sejarah Berat Individu
# =============================
def sejarah_berat(nama):
    try:
        rekod = load_rekod_berat()

        if rekod.empty or "Tarikh" not in rekod.columns:
            return pd.DataFrame()

        rekod["Tarikh"] = pd.to_datetime(rekod["Tarikh"], errors="coerce")
        rekod = rekod.dropna(subset=["Tarikh"])

        return rekod[rekod["Nama"] == nama].sort_values("Tarikh")
    except Exception as e:
        st.error(f"Gagal load sejarah berat: {e}")
        return pd.DataFrame()

# ============================================
# ✅ Export
# ============================================
__all__ = ["load_data_peserta", "get_berat_terkini"]