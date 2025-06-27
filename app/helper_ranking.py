# app/helper_ranking.py

import pandas as pd
from datetime import datetime
from app.helper_utils import kira_bmi, kategori_bmi_asia, kira_trend, tambah_medal
from app.helper_data import (
    load_data_peserta,
    get_berat_terkini,
    save_data_to_gsheet,
)
from app.helper_ranking_db import(
    load_data_ranking_bulanan,
    simpan_data_ranking_bulanan
)
from app.helper_log import log_dev


# === Generate Leaderboard Semasa ===
def generate_leaderboard():
    df_peserta = load_data_peserta()
    df_berat = get_berat_terkini()

    if df_berat.empty:
        return pd.DataFrame()

    df = pd.merge(df_peserta, df_berat, on="Nama", how="left")
    df["% Penurunan"] = df.apply(
        lambda x: round(((x["BeratAwal"] - x["BeratTerkini"]) / x["BeratAwal"]) * 100, 2)
        if x["BeratTerkini"] > 0 else 0,
        axis=1
    )

    df = df.sort_values(by="% Penurunan", ascending=False).reset_index(drop=True)
    df["Ranking"] = df.index + 1

    df = df[["Ranking", "Nama", "Jabatan", "BeratAwal", "BeratTerkini", "% Penurunan", "TarikhTimbang"]]
    log_dev("Generate Leaderboard", "Leaderboard semasa berjaya dijana")
    return df


# ===========================================
# ✅ Fungsi Leaderboard dengan Status Trend
# ===========================================
def leaderboard_dengan_status():
    try:
        sh = connect_gsheet()
        worksheet = sh.worksheet("data_peserta")
        df = pd.DataFrame(worksheet.get_all_records())

        if df.empty:
            return pd.DataFrame()

        df = tambah_kiraan_peserta(df)

        # Kiraan Ranking berdasarkan % Penurunan
        df = df.copy()
        df["Ranking"] = df["% Penurunan"].rank(method='min', ascending=False).astype(int)

        # Susun ikut ranking
        df = df.sort_values(by='Ranking')

        # Tentukan trend
        df["Ranking_Trend"] = df["Ranking"].apply(tambah_medal)

        return df

    except Exception as e:
        st.warning(f"❌ Gagal jana leaderboard: {e}")
        return pd.DataFrame()


# ===========================================
# ✅ Fungsi Simpan Ranking Bulanan ke Google Sheet
# ===========================================
def simpan_ranking_bulanan(df_ranking):
    try:
        if df_ranking.empty:
            st.warning("❌ Data ranking kosong, tidak dapat disimpan.")
            return

        local_tz = pytz.timezone("Asia/Kuala_Lumpur")
        tarikh = datetime.now(local_tz).strftime("%Y-%m-%d")

        df_simpan = df_ranking.copy()
        df_simpan["Tarikh"] = tarikh

        sh = connect_gsheet()
        worksheet = sh.worksheet("rekod_ranking")

        # Load rekod semasa
        rekod = pd.DataFrame(worksheet.get_all_records())

        # Combine
        df_final = pd.concat([rekod, df_simpan], ignore_index=True)

        # Overwrite balik ke Google Sheet
        worksheet.update(
            [df_final.columns.values.tolist()] + df_final.values.tolist()
        )

        st.success("✅ Ranking berjaya disimpan ke Google Sheet.")

    except Exception as e:
        st.warning(f"❌ Gagal simpan ranking: {e}")

# === Load Ranking Bulan Tertentu ===
def load_ranking_bulan(bulan):
    df_ranking = load_data_ranking_bulanan()

    if df_ranking is not None and bulan in df_ranking["Bulan"].values:
        df_bulan = df_ranking[df_ranking["Bulan"] == bulan].copy()
        return df_bulan[["Nama", "Ranking"]].reset_index(drop=True)
    else:
        return None


# === Load Ranking Bulan Terakhir ===
def load_ranking_terakhir():
    df_ranking = load_data_ranking_bulanan()

    if df_ranking is not None and not df_ranking.empty:
        bulan_terakhir = sorted(df_ranking["Bulan"].unique())[-1]
        return load_ranking_bulan(bulan_terakhir)
    else:
        return None


# ===========================================
# ✅ Fungsi Sejarah Ranking
# ===========================================
def sejarah_ranking():
    try:
        sh = connect_gsheet()
        worksheet = sh.worksheet("rekod_ranking")
        df = pd.DataFrame(worksheet.get_all_records())

        if df.empty:
            return pd.DataFrame()

        return df

    except Exception as e:
        st.warning(f"❌ Gagal load sejarah ranking: {e}")
        return pd.DataFrame()

# ===========================================
# ✅ Fungsi Backup Ranking ke Google Drive (Excel)
# ===========================================
def backup_ranking_to_drive(df_ranking):
    try:
        if df_ranking.empty:
            st.warning("❌ Data ranking kosong untuk backup.")
            return

        local_tz = pytz.timezone("Asia/Kuala_Lumpur")
        tarikh = datetime.now(local_tz).strftime("%Y-%m-%d")

        nama_fail = f"rekod_ranking_{tarikh}.xlsx"

        save_to_gdrive(df_ranking, nama_fail, folder_id=st.secrets["gdrive_folder_id"])

        st.success(f"✅ Backup Ranking disimpan ke Google Drive sebagai {nama_fail}")

    except Exception as e:
        st.warning(f"❌ Gagal backup ranking ke Google Drive: {e}")

# === Export Fungsi ===
__all__ = [
    "generate_leaderboard",
    "leaderboard_dengan_status",
    "simpan_ranking_bulanan",
    "load_ranking_bulan",
    "load_ranking_terakhir",
    "sejarah_ranking",
]
