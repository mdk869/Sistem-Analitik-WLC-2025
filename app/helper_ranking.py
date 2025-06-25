import pandas as pd
from datetime import datetime
from app.helper_logic import tambah_kiraan_peserta
from app.helper_data import gc  # Guna sambungan Google Sheets yang sama

# === Setup Sheet untuk Ranking History
SHEET_NAME = "data_peserta"
sheet = gc.open(SHEET_NAME)

# === Fungsi: Create Ranking DataFrame (Snapshot Bulanan)
def create_ranking_snapshot(df_merge):
    df = tambah_kiraan_peserta(df_merge)

    df = df.sort_values("% Penurunan", ascending=False).reset_index(drop=True)
    df["Ranking"] = df.index + 1

    bulan_ini = datetime.now().strftime("%Y-%m")
    df["TarikhSnapshot"] = bulan_ini

    df_ranking = df[["Ranking", "Nama", "% Penurunan", "TarikhSnapshot"]]

    return df_ranking

# === Fungsi: Simpan Ranking ke Google Sheet (Sheet: 'ranking_history')
def save_ranking_to_sheet(df_ranking):
    try:
        ws_ranking = sheet.worksheet("ranking_history")
    except:
        # Kalau tak wujud, cipta baru
        ws_ranking = sheet.add_worksheet(title="ranking_history", rows="1000", cols="10")
        ws_ranking.append_row(["Ranking", "Nama", "% Penurunan", "TarikhSnapshot"])

    existing_data = ws_ranking.get_all_records()
    df_existing = pd.DataFrame(existing_data)

    df_new = pd.concat([df_existing, df_ranking], ignore_index=True)
    ws_ranking.clear()
    ws_ranking.append_row(list(df_new.columns))

    for row in df_new.values.tolist():
        ws_ranking.append_row(row)

    return "Ranking berjaya disimpan!"

# === Fungsi: Load Ranking History
def load_ranking_history():
    try:
        ws_ranking = sheet.worksheet("ranking_history")
        data = ws_ranking.get_all_records()
        if not data:
            return pd.DataFrame()
        return pd.DataFrame(data)
    except:
        return pd.DataFrame()
