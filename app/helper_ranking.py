# app/helper_ranking.py

import streamlit as st
import pandas as pd
from datetime import datetime

from app.helper_connection import SPREADSHEET_RANKING, get_worksheet
from app.helper_data import load_data_peserta
from app.helper_utils import save_dataframe_to_excel


# ====================================================
# ✅ Load Rekod Ranking
# ====================================================
def load_rekod_ranking():
    try:
        ws = get_worksheet(SPREADSHEET_RANKING, "rekod")
        data = ws.get_all_records()
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        st.error(f"❌ Gagal load rekod ranking: {e}")
        return pd.DataFrame()


# ====================================================
# ✅ Simpan Rekod Ranking
# ====================================================
def save_rekod_ranking(df):
    try:
        ws = get_worksheet(SPREADSHEET_RANKING, "rekod")
        ws.clear()
        ws.update([df.columns.values.tolist()] + df.values.tolist())
        st.success("✅ Rekod ranking berjaya disimpan.")
    except Exception as e:
        st.error(f"❌ Gagal simpan rekod ranking: {e}")


# ====================================================
# ✅ Kira Leaderboard Semasa
# ====================================================
def leaderboard_dengan_status(df):
    """
    Terima dataframe peserta dan kira % penurunan berat serta ranking.
    """
    if df.empty:
        st.warning("🚫 Tiada data peserta.")
        return pd.DataFrame()

    # ✅ Kira % perubahan berat
    df["%Perubahan"] = round(
        (df["BeratAwal"] - df["BeratTerkini"]) / df["BeratAwal"] * 100, 2
    )

    # ✅ Susun ikut %Perubahan tertinggi
    df = df.sort_values(by="%Perubahan", ascending=False).reset_index(drop=True)
    df["Ranking"] = df.index + 1

    return df[[
        "Ranking", "Nama", "BeratAwal", "BeratTerkini", "%Perubahan", "BMI", "Kategori"
    ]]


# ====================================================
# ✅ Backup Rekod Ranking ke Excel
# ====================================================
def backup_rekod_ranking(df):
    try:
        filename = f"backup_rekod_ranking_{datetime.now().strftime('%Y%m%d')}.xlsx"
        save_dataframe_to_excel(df, filename)
        st.info(f"📦 Backup rekod ranking disimpan: {filename}")
        return filename
    except Exception as e:
        st.error(f"❌ Gagal backup ranking: {e}")
