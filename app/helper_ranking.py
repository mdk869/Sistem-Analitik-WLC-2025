# helper_ranking.py

import pandas as pd
from datetime import datetime
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

from app.helper_data import load_data_peserta, get_berat_terkini
from app.helper_log import log_dev


# === Setup Google Sheet Rekod Ranking ===
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
credentials = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"], scopes=scope
)
gc = gspread.authorize(credentials)

# === Sambungan ke Spreadsheet Ranking
sheet_ranking = gc.open_by_key(st.secrets["gsheet"]["rekod_ranking"])

# === Check & Auto Create Worksheet
def check_or_create_worksheet(sheet, name, header):
    try:
        ws = sheet.worksheet(name)
    except:
        ws = sheet.add_worksheet(title=name, rows="1000", cols="20")
        ws.append_row(header)
    return ws


# === Fungsi: Kira Peratus Penurunan Berat
def kira_peratus_turun(berat_awal, berat_semasa):
    try:
        return round(((berat_awal - berat_semasa) / berat_awal) * 100, 2)
    except:
        return 0


# === Fungsi: Generate Leaderboard Semasa
def generate_leaderboard():
    try:
        df_peserta = load_data_peserta()
        df_berat = get_berat_terkini()

        if df_berat.empty:
            st.warning("❌ Rekod berat kosong.")
            return pd.DataFrame()

        df = pd.merge(df_peserta, df_berat, on="Nama", how="left")
        df["% Turun"] = df.apply(lambda x: kira_peratus_turun(x["BeratAwal"], x["Berat"]), axis=1)

        df = df.sort_values(by="% Turun", ascending=False).reset_index(drop=True)
        df["Ranking"] = df.index + 1

        df = df[["Ranking", "Nama", "Jabatan", "BeratAwal", "Berat", "% Turun", "Tarikh"]]

        log_dev("Generate Leaderboard", "Leaderboard semasa berjaya dijana")
        return df

    except Exception as e:
        st.error(f"Gagal jana leaderboard: {e}")
        log_dev("Generate Leaderboard", f"Gagal jana leaderboard: {e}")
        return pd.DataFrame()


# === Fungsi: Simpan Ranking Bulanan ke Spreadsheet Rekod Ranking
def simpan_ranking_bulanan(df_ranking):
    bulan_ini = datetime.now().strftime('%Y-%m')
    nama_sheet = f'Ranking_{bulan_ini}'

    try:
        # Delete jika sheet wujud
        try:
            ws_exist = sheet_ranking.worksheet(nama_sheet)
            sheet_ranking.del_worksheet(ws_exist)
        except:
            pass

        ws_new = sheet_ranking.add_worksheet(title=nama_sheet, rows=1000, cols=20)
        data = [df_ranking.columns.values.tolist()] + df_ranking.values.tolist()
        ws_new.update('A1', data)

        st.success(f'Ranking disimpan ke sheet "{nama_sheet}"')
        log_dev("Simpan Ranking", f'Ranking {nama_sheet} berjaya disimpan')

    except Exception as e:
        st.error(f"Gagal simpan ranking: {e}")
        log_dev("Simpan Ranking", f'Gagal simpan ranking {nama_sheet}: {e}')


# === Fungsi: Load Ranking Bulanan
def load_ranking_bulanan(bulan):
    nama_sheet = f'Ranking_{bulan}'

    try:
        ws = sheet_ranking.worksheet(nama_sheet)
        data = ws.get_all_records()
        df = pd.DataFrame(data)
        return df
    except Exception:
        st.warning(f'Sheet {nama_sheet} tidak dijumpai.')
        return None


# === List Semua Sheet Ranking
def list_ranking_sheets():
    worksheet_list = sheet_ranking.worksheets()
    ranking_sheets = [
        ws.title for ws in worksheet_list if ws.title.startswith('Ranking_')
    ]
    return ranking_sheets


# === Fungsi: Tambah Status Naik/Turun/Baru
def tambah_status_ranking(df_current, bulan_sebelum):
    df_previous = load_ranking_bulanan(bulan_sebelum)

    if df_previous is None or df_previous.empty:
        df_current["Status"] = "Baru"
        return df_current

    df_merge = pd.merge(
        df_current[["Nama", "Ranking"]],
        df_previous[["Nama", "Ranking"]],
        on="Nama",
        how="left",
        suffixes=("", "_Sebelum")
    )

    def kira_status(row):
        if pd.isna(row["Ranking_Sebelum"]):
            return "Baru"
        elif row["Ranking"] < row["Ranking_Sebelum"]:
            return "Naik"
        elif row["Ranking"] > row["Ranking_Sebelum"]:
            return "Turun"
        else:
            return "Mendatar"

    df_merge["Status"] = df_merge.apply(kira_status, axis=1)
    df_final = pd.merge(df_current, df_merge[["Nama", "Status"]], on="Nama", how="left")

    return df_final


# === Fungsi: Leaderboard Lengkap Dengan Status
def leaderboard_dengan_status():
    bulan_ini = datetime.now().strftime('%Y-%m')
    tahun, bulan = bulan_ini.split("-")

    # Kira bulan sebelum
    bulan_int = int(bulan) - 1
    if bulan_int == 0:
        bulan_int = 12
        tahun = str(int(tahun) - 1)

    bulan_sebelum = f"{tahun}-{bulan_int:02d}"

    df_current = generate_leaderboard()

    if df_current.empty:
        return pd.DataFrame()

    df_final = tambah_status_ranking(df_current, bulan_sebelum)

    return df_final


# === Fungsi: Sejarah Ranking Individu
def sejarah_ranking(nama):
    try:
        sheets = list_ranking_sheets()

        sejarah = []
        for sheet in sheets:
            bulan = sheet[-7:]  # Ambil tarikh dari nama sheet
            df = load_ranking_bulanan(bulan)
            if df is not None and not df.empty:
                df_nama = df[df["Nama"] == nama]
                if not df_nama.empty:
                    sejarah.append({
                        "Bulan": bulan,
                        "Ranking": int(df_nama["Ranking"].values[0]),
                        "% Turun": df_nama["% Turun"].values[0]
                    })

        df_sejarah = pd.DataFrame(sejarah)
        df_sejarah = df_sejarah.sort_values("Bulan")
        return df_sejarah

    except Exception as e:
        st.warning(f"Gagal dapatkan sejarah ranking: {e}")
        return pd.DataFrame()
