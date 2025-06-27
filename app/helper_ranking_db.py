import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from datetime import datetime, timedelta
import tempfile
import os
import streamlit as st
from app.helper_utils import get_tarikh_masa
from app.helper_log import log_dev

# === Setup sambungan Google Sheet dan Google Drive
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
credentials = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"], scopes=scope
)
gc = gspread.authorize(credentials)

# === Sambung Google Drive
gauth = GoogleAuth()
gauth.credentials = credentials
drive = GoogleDrive(gauth)

# === Sambungan ke Spreadsheet Ranking
sheet_ranking = gc.open_by_key(st.secrets["gsheet"]["data_peserta_id"])

# === Worksheet ranking
def check_or_create_ranking_sheet():
    try:
        ws = sheet_ranking.worksheet("ranking_bulanan")
    except:
        ws = sheet_ranking.add_worksheet(title="ranking_bulanan", rows="1000", cols="10")
        ws.append_row(["Nama", "Ranking", "Bulan", "TarikhSimpan"])
    return ws

ws_ranking = check_or_create_ranking_sheet()


# === Load Data Ranking Bulanan
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


# === Simpan Data Ranking Bulanan
def simpan_data_ranking_bulanan(df):
    try:
        ws_ranking.clear()
        ws_ranking.append_row(["Nama", "Ranking", "Bulan", "TarikhSimpan"])
        records = df.values.tolist()
        ws_ranking.append_rows(records)
        log_dev("Simpan Ranking DB", f"Data ranking berjaya disimpan ke worksheet")
    except Exception as e:
        st.error(f"❌ Gagal simpan data ranking: {e}")


# === Backup Ranking ke Google Drive
def backup_ranking_to_drive():
    try:
        df = load_data_ranking_bulanan()
        if df.empty:
            st.warning("⚠️ Data ranking kosong, tiada data untuk backup.")
            return

        filename = f"ranking_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmpfile:
            df.to_excel(tmpfile.name, index=False)

            file_drive = drive.CreateFile({
                'title': filename,
                'parents': [{'id': st.secrets['gdrive']['backup_folder_id']}]
            })
            file_drive.SetContentFile(tmpfile.name)
            file_drive.Upload()

            st.success(f"✅ Backup ranking berjaya ke Google Drive sebagai {filename}")
            log_dev("Backup Ranking", f"Backup ke Google Drive sebagai {filename}")

        os.remove(tmpfile.name)

    except Exception as e:
        st.error(f"❌ Gagal backup ranking ke Google Drive: {e}")


# === Simpan Ranking Bulanan dengan Auto Backup
def simpan_ranking_bulanan(df_ranking):
    try:
        bulan_ini = datetime.now().strftime('%Y-%m')
        tarikh_simpan = get_tarikh_masa()

        df_simpan = df_ranking[["Nama", "Ranking"]].copy()
        df_simpan["Bulan"] = bulan_ini
        df_simpan["TarikhSimpan"] = tarikh_simpan

        df_ranking_bulanan = load_data_ranking_bulanan()

        if df_ranking_bulanan is not None and not df_ranking_bulanan.empty:
            df_ranking_bulanan = pd.concat([df_ranking_bulanan, df_simpan], ignore_index=True)
        else:
            df_ranking_bulanan = df_simpan

        simpan_data_ranking_bulanan(df_ranking_bulanan)

        st.success(f"✅ Ranking bulan {bulan_ini} berjaya disimpan.")
        log_dev("Simpan Ranking", f'Ranking bulan {bulan_ini} berjaya disimpan')

        backup_ranking_to_drive()

    except Exception as e:
        st.error(f"❌ Gagal simpan ranking bulanan: {e}")


# === ✅ Fungsi Tambahan: Restore Ranking dari Google Drive
def restore_ranking_from_drive():
    try:
        folder_id = st.secrets['gdrive']['backup_folder_id']
        file_list = drive.ListFile({
            'q': f"'{folder_id}' in parents and trashed=false"
        }).GetList()

        if not file_list:
            st.warning("❌ Tiada file backup ditemui di Google Drive.")
            return

        # Cari file terbaru berdasarkan nama
        file_list_sorted = sorted(
            file_list,
            key=lambda x: x['title'],
            reverse=True
        )
        latest_file = file_list_sorted[0]

        st.info(f"📥 Muat turun file {latest_file['title']} untuk restore...")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmpfile:
            latest_file.GetContentFile(tmpfile.name)
            df = pd.read_excel(tmpfile.name)

            if not df.empty:
                simpan_data_ranking_bulanan(df)
                st.success("✅ Restore data ranking dari backup berjaya.")
                log_dev("Restore Ranking", f"Restore ranking dari file {latest_file['title']} berjaya.")
            else:
                st.warning("❌ Data backup kosong, restore gagal.")

        os.remove(tmpfile.name)

    except Exception as e:
        st.error(f"❌ Gagal restore ranking dari Google Drive: {e}")


# === ✅ Fungsi Tambahan: Auto Cleanup Backup Lama di Google Drive
def cleanup_backup_files(max_days=7):
    try:
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
                log_dev("Cleanup Backup", f"Deleted {file['title']} (Age: {age} days)")

        st.success(f"✅ Cleanup siap. {deleted_count} file lama dipadam dari Google Drive.")
        if deleted_count == 0:
            st.info("Tiada file lama untuk dipadam.")

    except Exception as e:
        st.error(f"❌ Gagal cleanup backup: {e}")
