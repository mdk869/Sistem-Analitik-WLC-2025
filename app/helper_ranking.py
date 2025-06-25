import pandas as pd
from datetime import datetime
from app.helper_logic import tambah_kiraan_peserta
from app.helper_data import gc  # Sambungan Google Sheets

# === Setup Sheet
SHEET_NAME = "data_peserta"
sheet = gc.open(SHEET_NAME)


# === Create Snapshot Ranking Bulanan ===
def create_ranking_snapshot(df_merge):
    df = tambah_kiraan_peserta(df_merge)

    df = df.sort_values("% Penurunan", ascending=False).reset_index(drop=True)
    df["Ranking"] = df.index + 1

    bulan_ini = datetime.now().strftime("%Y-%m")
    df["TarikhSnapshot"] = bulan_ini

    df_ranking = df[["Ranking", "Nama", "% Penurunan", "TarikhSnapshot"]]

    return df_ranking


# === Simpan Ranking ke Sheet 'ranking_history' ===
def save_ranking_to_sheet(df_ranking):
    try:
        ws = sheet.worksheet("ranking_history")
    except:
        ws = sheet.add_worksheet(title="ranking_history", rows="1000", cols="10")
        ws.append_row(["Ranking", "Nama", "% Penurunan", "TarikhSnapshot"])

    existing = ws.get_all_records()
    df_existing = pd.DataFrame(existing)

    df_combined = pd.concat([df_existing, df_ranking], ignore_index=True)

    # Kemaskini data secara batch
    ws.clear()
    ws.update(
        "A1",
        [df_combined.columns.values.tolist()] + df_combined.values.tolist()
    )

    return "✅ Ranking berjaya disimpan ke 'ranking_history'"


# === Load Ranking History ===
def load_ranking_history():
    try:
        ws = sheet.worksheet("ranking_history")
        data = ws.get_all_records()
        if not data:
            return pd.DataFrame()
        return pd.DataFrame(data)
    except:
        return pd.DataFrame()


# === Untuk import automatik dari modul ===
__all__ = [
    "create_ranking_snapshot",
    "save_ranking_to_sheet",
    "load_ranking_history"
]
