# helper_ranking.py

import pandas as pd
from app.helper_logic import kira_status_ranking
from app.helper_data import load_data_cloud_or_local


# === Leaderboard dengan Status Ranking ===
def leaderboard_dengan_status():
    df = load_data_cloud_or_local()

    if df.empty:
        return pd.DataFrame()

    # Pastikan kolum numeric
    df['Tinggi'] = pd.to_numeric(df['Tinggi'], errors='coerce')
    df['BeratAwal'] = pd.to_numeric(df['BeratAwal'], errors='coerce')
    df['BeratTerkini'] = pd.to_numeric(df['BeratTerkini'], errors='coerce')

    # Kiraan Penurunan
    df["PenurunanKg"] = (df["BeratAwal"] - df["BeratTerkini"]).round(2).fillna(0)
    df["% Penurunan"] = ((df["PenurunanKg"] / df["BeratAwal"]) * 100).round(4).fillna(0)

    # Kiraan Status Naik/Turun/Kekal
    df["Ranking_Trend"] = df.apply(
        lambda row: kira_status_ranking(row["BeratAwal"], row["BeratTerkini"]),
        axis=1
    )

    # Susun ikut % Penurunan
    df = df.sort_values(by='% Penurunan', ascending=False).reset_index(drop=True)

    # Beri ranking
    df["Ranking"] = df.index + 1

    # Tambah Medal pada Top 3
    medal_map = {1: "🥇", 2: "🥈", 3: "🥉"}
    df["Ranking_Trend"] = [
        f"{medal_map.get(rank, rank)} {trend}"
        for rank, trend in zip(df["Ranking"], df["Ranking_Trend"])
    ]

    return df


# === Simpan Rekod Ranking Bulanan ===
def simpan_ranking_bulanan(sheet_name="rekod_ranking_semasa"):
    df = leaderboard_dengan_status()

    if df.empty:
        return False

    try:
        from app.helper_data import connect_gsheet

        sh = connect_gsheet()
        now = pd.Timestamp.now().strftime('%Y-%m-%d')

        worksheet = sh.worksheet(sheet_name)

        data = df[["Nama", "NoStaf", "% Penurunan", "Ranking", "Ranking_Trend"]]
        data["Tarikh"] = now

        existing = worksheet.get_all_values()
        existing_rows = len(existing)

        worksheet.update(f"A{existing_rows + 1}", [data.columns.tolist()])
        worksheet.update(f"A{existing_rows + 2}", data.values.tolist())

        return True

    except Exception as e:
        print(f"❌ Gagal simpan ranking bulanan: {e}")
        return False


# === Sejarah Ranking (baca dari sheet) ===
def sejarah_ranking(sheet_name="rekod_ranking_semasa"):
    try:
        from app.helper_data import connect_gsheet

        sh = connect_gsheet()
        worksheet = sh.worksheet(sheet_name)

        df = pd.DataFrame(worksheet.get_all_records())

        if df.empty:
            return pd.DataFrame()

        df["% Penurunan"] = pd.to_numeric(df["% Penurunan"], errors='coerce').fillna(0)
        df["Ranking"] = pd.to_numeric(df["Ranking"], errors='coerce').fillna(0).astype(int)

        return df

    except Exception as e:
        print(f"❌ Gagal load sejarah ranking: {e}")
        return pd.DataFrame()


# === Export Fungsi ===
__all__ = [
    "leaderboard_dengan_status",
    "simpan_ranking_bulanan",
    "sejarah_ranking"
]
