# app/helper_ranking.py

import streamlit as st
import pandas as pd
from datetime import datetime

from app.helper_connection import SPREADSHEET_RANKING
from app.helper_gsheet import get_worksheet
from app.helper_utils import save_dataframe_to_excel
from app.helper_logic import tambah_kiraan_peserta
from app.helper_log import log_warning
import plotly.express as px


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


# ==========================================
# ✅ Leaderboard Berdasarkan % Penurunan
# ==========================================
def leaderboard_peserta(df, top_n=10):
    """
    Terima dataframe peserta, kira % penurunan berat dan susun ranking.
    Return top_n peserta dengan badge untuk no.1.
    """
    if df.empty:
        st.warning("🚫 Tiada data peserta.")
        log_warning("Leaderboard gagal: Data peserta kosong.")
        return pd.DataFrame()

    try:
        df_kiraan = tambah_kiraan_peserta(df)

        df_sorted = df_kiraan.sort_values(by="% Penurunan", ascending=False).reset_index(drop=True)
        df_sorted["Ranking"] = df_sorted.index + 1

        leaderboard = df_sorted[["Ranking", "Nama", "% Penurunan"]].head(top_n)

        # 🎖️ Tambah badge untuk ranking pertama
        leaderboard.loc[leaderboard["Ranking"] == 1, "Nama"] = (
            leaderboard.loc[leaderboard["Ranking"] == 1, "Nama"].values[0] + " 🏆"
        )

        return leaderboard

    except Exception as e:
        st.error(f"❌ Gagal jana leaderboard: {e}")
        log_warning(f"Leaderboard error: {e}")
        return pd.DataFrame()



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


# ==========================================
# ✅ Trend Line Penurunan Bulanan
# ==========================================
def trend_penurunan_bulanan(df_rekod):
    """
    Terima dataframe rekod timbang.
    Kira purata penurunan berat (%) setiap bulan.
    """
    if df_rekod.empty:
        st.warning("🚫 Tiada data rekod timbang.")
        return None

    try:
        df_rekod["SesiBulan"] = df_rekod["Tarikh"].dt.strftime('%B %Y')

        trend = (
            df_rekod.groupby("SesiBulan")["Berat"]
            .mean()
            .reset_index()
            .rename(columns={"Berat": "BeratPurata"})
        )

        fig = px.line(
            trend,
            x="SesiBulan",
            y="BeratPurata",
            markers=True,
            title="📈 Trend Berat Purata Bulanan",
            labels={"SesiBulan": "Bulan", "BeratPurata": "Berat Purata (kg)"}
        )
        fig.update_layout(xaxis=dict(tickangle=45))
        return fig

    except Exception as e:
        st.error(f"❌ Gagal jana graf trend: {e}")
        return None
