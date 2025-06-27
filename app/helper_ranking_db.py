import os
import tempfile
from datetime import datetime

import pandas as pd
import streamlit as st
from app.helper_log import log_dev
from app.helper_utils import get_tarikh_masa
from app.helper_data import connect_drive
from app.helper_ranking_db import load_data_ranking_bulanan, simpan_data_ranking_bulanan


# =============================================
# ✅ Backup Ranking ke Google Drive
# =============================================
def backup_ranking_to_drive():
    try:
        df = load_data_ranking_bulanan()
        if df.empty:
            st.warning("⚠️ Data ranking kosong. Tiada data untuk backup.")
            return

        drive = connect_drive()
        folder_id = st.secrets['gdrive']['backup_folder_id']
        filename = f"ranking_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmpfile:
            df.to_excel(tmpfile.name, index=False)

            file_drive = drive.CreateFile({
                'title': filename,
                'parents': [{'id': folder_id}]
            })
            file_drive.SetContentFile(tmpfile.name)
            file_drive.Upload()

            st.success(f"✅ Backup ranking berjaya ke Google Drive sebagai {filename}")
            log_dev("Backup Ranking", f"Backup ke Google Drive: {filename}")

        os.remove(tmpfile.name)

    except Exception as e:
        st.error(f"❌ Gagal backup ranking ke Google Drive: {e}")
        log_dev("Backup Ranking", "Gagal backup ranking", "Gagal", str(e))


# =============================================
# ✅ Restore Ranking dari Google Drive
# =============================================
def restore_ranking_from_drive():
    try:
        drive = connect_drive()
        folder_id = st.secrets['gdrive']['backup_folder_id']

        file_list = drive.ListFile({
            'q': f"'{folder_id}' in parents and trashed=false"
        }).GetList()

        if not file_list:
            st.warning("❌ Tiada file backup ditemui di Google Drive.")
            return

        # Cari file terbaru
        file_list_sorted = sorted(
            file_list,
            key=lambda x: x['title'],
            reverse=True
        )
        latest_file = file_list_sorted[0]

        st.info(f"📥 Memuat turun file {latest_file['title']} untuk restore...")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmpfile:
            latest_file.GetContentFile(tmpfile.name)
            df = pd.read_excel(tmpfile.name)

            if not df.empty:
                simpan_data_ranking_bulanan(df)
                st.success("✅ Restore data ranking dari backup berjaya.")
                log_dev("Restore Ranking", f"Restore dari file {latest_file['title']}")
            else:
                st.warning("❌ Data backup kosong. Restore gagal.")

        os.remove(tmpfile.name)

    except Exception as e:
        st.error(f"❌ Gagal restore ranking dari Google Drive: {e}")
        log_dev("Restore Ranking", "Gagal restore ranking", "Gagal", str(e))


# =============================================
# ✅ Auto Cleanup Backup Lama
# =============================================
def cleanup_backup_files(max_days=7):
    try:
        drive = connect_drive()
        folder_id = st.secrets['gdrive']['backup_folder_id']

        file_list = drive.ListFile({
            'q': f"'{folder_id}' in parents and trashed=false"
        }).GetList()

        now = datetime.now()
        deleted_count = 0

        for file in file_list:
            created_str = file['createdDate']
            created_date = datetime.strptime(created_str[:10], '%Y-%m-%d')
            age = (now - created_date).days

            if age > max_days:
                file.Delete()
                deleted_count += 1
                log_dev("Cleanup Backup", f"Padam {file['title']} (Umur: {age} hari)")

        if deleted_count > 0:
            st.success(f"✅ Cleanup selesai. {deleted_count} file lama dipadam.")
        else:
            st.info("ℹ️ Tiada file lama untuk dipadam.")

    except Exception as e:
        st.error(f"❌ Gagal cleanup backup di Google Drive: {e}")
        log_dev("Cleanup Backup", "Gagal cleanup backup", "Gagal", str(e))


# =============================================
# ✅ Export Fungsi
# =============================================
__all__ = [
    "backup_ranking_to_drive",
    "restore_ranking_from_drive",
    "cleanup_backup_files"
]
