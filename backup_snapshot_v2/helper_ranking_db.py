# app/helper_ranking_db.py

import pandas as pd
import streamlit as st
from datetime import datetime
import tempfile
import os

from app.helper_connection import rekod_ranking, DRIVE, get_secret_id
from app.helper_utils import get_tarikh_masa
from app.helper_log import log_dev


# ============================================
# ✅ Worksheet Ranking
# ============================================
try:
    ws_ranking = rekod_ranking.worksheet("ranking_bulanan")
except:
    ws_ranking = rekod_ranking.add_worksheet(title="ranking_bulanan", rows="1000", cols="10")
    ws_ranking.append_row(["Nama", "Ranking", "Bulan", "TarikhSimpan"])


# ============================================
# ✅ Load Data Ranking Bulanan
# ============================================
def load_data_ranking_bulanan():
    try:
        data = ws_ranking.get_all_records()
        if not data:
            return pd.DataFrame(columns=["Nama", "Ranking", "Bulan", "TarikhSimpan"])
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        st.error(f"❌ Gagal load data ranking: {e}")
        return pd.DataFrame(columns=["Nama", "Ranking", "Bulan", "TarikhSimpan"])


# ============================================
# ✅ Simpan Data Ranking Bulanan
# ============================================
def simpan_data_ranking_bulanan(df):
    try:
        ws_ranking.clear()
        ws_ranking.append_row(["Nama", "Ranking", "Bulan", "TarikhSimpan"])
        records = df.values.tolist()
        ws_ranking.append_rows(records)
        log_dev("Simpan Ranking DB", f"Data ranking berjaya disimpan")
    except Exception as e:
        st.error(f"❌ Gagal simpan data ranking: {e}")


# ============================================
# ✅ Backup Ranking ke Google Drive
# ============================================
def backup_ranking_to_drive():
    try:
        df = load_data_ranking_bulanan()
        if df.empty:
            st.warning("⚠️ Data ranking kosong, tiada untuk backup.")
            return

        filename = f"ranking_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmpfile:
            df.to_excel(tmpfile.name, index=False)

            file_drive = DRIVE.CreateFile({
                'title': filename,
                'parents': [{'id': get_secret_id("drive", "folder_id")}]
            })
            file_drive.SetContentFile(tmpfile.name)
            file_drive.Upload()

            st.success(f"✅ Backup ranking berjaya ke Google Drive sebagai {filename}")
            log_dev("Backup Ranking", f"Backup sebagai {filename}")

        os.remove(tmpfile.name)

    except Exception as e:
        st.error(f"❌ Gagal backup ranking: {e}")


# ============================================
# ✅ Simpan Ranking Bulanan dengan Backup
# ============================================
def simpan_ranking_bulanan(df_ranking):
    try:
        bulan_ini = datetime.now().strftime('%Y-%m')
        tarikh_simpan = get_tarikh_masa()

        df_simpan = df_ranking[["Nama", "Ranking"]].copy()
        df_simpan["Bulan"] = bulan_ini
        df_simpan["TarikhSimpan"] = tarikh_simpan

        df_ranking_bulanan = load_data_ranking_bulanan()

        if not df_ranking_bulanan.empty:
            df_ranking_bulanan = pd.concat([df_ranking_bulanan, df_simpan], ignore_index=True)
        else:
            df_ranking_bulanan = df_simpan

        simpan_data_ranking_bulanan(df_ranking_bulanan)

        st.success(f"✅ Ranking bulan {bulan_ini} berjaya disimpan.")
        log_dev("Simpan Ranking", f'Ranking bulan {bulan_ini} berjaya disimpan')

        backup_ranking_to_drive()

    except Exception as e:
        st.error(f"❌ Gagal simpan ranking: {e}")


# ============================================
# ✅ Export
# ============================================
__all__ = [
    "load_data_ranking_bulanan",
    "simpan_data_ranking_bulanan",
    "backup_ranking_to_drive",
    "simpan_ranking_bulanan"
]
