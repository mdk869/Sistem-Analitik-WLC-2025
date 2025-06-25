import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import streamlit as st
import pytz

# Import logik tambahan (bmi, ranking)
from app.helper_logic import kira_bmi, kategori_bmi_asia


# === Setup sambungan Google Sheet
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
credentials = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"], scopes=scope
)
gc = gspread.authorize(credentials)

sheet = gc.open(st.secrets["gsheet"]["spreadsheet"])
ws_peserta = sheet.worksheet("peserta")
ws_rekod = sheet.worksheet("rekod_berat")


def load_data_cloud_or_local():
    try:
        df = load_data_peserta()
    except Exception as e:
        st.warning(f"⚠️ Gagal load dari Google Sheet: {e}")
        # Cuba load dari fail Excel lokal sebagai backup
        df = pd.read_excel("data_peserta_backup.xlsx")
        st.info("Data dimuat dari fail lokal sebagai backup")
    return df


# === Fungsi: Load Data Peserta
def load_data_peserta():
    return pd.DataFrame(ws_peserta.get_all_records())


# === Fungsi: Load Rekod Berat
def load_rekod_berat():
    return pd.DataFrame(ws_rekod.get_all_records())


# === Fungsi: Tambah Peserta Baru
def tambah_peserta_google_sheet(nama, nostaf, umur, jantina, jabatan, tinggi, berat_awal, tarikh_daftar):
    berat_terkini = berat_awal
    tarikh_timbang = tarikh_daftar
    bmi = kira_bmi(berat_awal, tinggi)
    kategori = kategori_bmi_asia(bmi)

    data_baru = [
        nama, nostaf, umur, jantina, jabatan, tinggi,
        berat_awal, str(tarikh_daftar), berat_terkini,
        str(tarikh_timbang), bmi, kategori
    ]

    ws_peserta.append_row(data_baru)
    ws_rekod.append_row([nama, str(tarikh_timbang), berat_terkini])


# === Fungsi: Kemaskini Berat Peserta + Simpan ke Rekod
def kemaskini_berat_peserta(nama, berat_baru, tarikh_baru):
    data = ws_peserta.get_all_records()

    for idx, row in enumerate(data):
        if row["Nama"] == nama:
            bmi_baru = kira_bmi(berat_baru, row["Tinggi"])
            kategori_baru = kategori_bmi_asia(bmi_baru)
            ws_peserta.update(f"I{idx+2}", berat_baru)  # BeratTerkini
            ws_peserta.update(f"J{idx+2}", str(tarikh_baru))  # TarikhTimbang
            ws_peserta.update(f"K{idx+2}", bmi_baru)  # BMI
            ws_peserta.update(f"L{idx+2}", kategori_baru)  # Kategori
            break

    ws_rekod.append_row([nama, str(tarikh_baru), berat_baru])


# === Fungsi: Sejarah Berat Individu
def sejarah_berat(nama):
    rekod = pd.DataFrame(ws_rekod.get_all_records())
    rekod.columns = [str(col).strip() for col in rekod.columns]

    if rekod.empty or "Tarikh" not in rekod.columns:
        return pd.DataFrame()
    rekod["Tarikh"] = pd.to_datetime(rekod["Tarikh"], format="mixed", errors="coerce")
    rekod = rekod.dropna(subset=["Tarikh"])
    return rekod[rekod["Nama"] == nama].sort_values("Tarikh")


# === Fungsi: Padam Peserta
def padam_peserta_dari_sheet(nama):
    data = ws_peserta.get_all_records()

    for idx, row in enumerate(data):
        if row["Nama"] == nama:
            ws_peserta.delete_rows(idx + 2)
            return True
    return False


# === Fungsi: Dapatkan Berat Terkini Semua Peserta
def get_berat_terkini():
    df_rekod = load_rekod_berat()
    if df_rekod.empty:
        return pd.DataFrame(columns=["Nama", "Berat", "Tarikh"])

    df_rekod["Tarikh"] = pd.to_datetime(df_rekod["Tarikh"], errors="coerce")

    df_latest = (
        df_rekod.sort_values('Tarikh', ascending=False)
        .drop_duplicates('Nama')
        .reset_index(drop=True)
    )

    return df_latest[["Nama", "Berat", "Tarikh"]]


# === FUNGSI: RANKING HISTORY (MENGIKUT BULAN) ===

# Simpan Ranking History ke Sheet Mengikut Bulan
def simpan_ranking_bulanan(df_ranking):
    bulan_ini = datetime.now().strftime('%Y-%m')
    nama_sheet = f'Ranking_{bulan_ini}'

    try:
        try:
            ws_exist = sheet.worksheet(nama_sheet)
            sheet.del_worksheet(ws_exist)
        except:
            pass  # Sheet belum wujud

        ws_new = sheet.add_worksheet(title=nama_sheet, rows=1000, cols=10)
        data = [df_ranking.columns.values.tolist()] + df_ranking.values.tolist()
        ws_new.update('A1', data)

        st.success(f'Ranking disimpan ke sheet "{nama_sheet}"')
    except Exception as e:
        st.error(f"Gagal simpan ranking: {e}")


# Load Ranking History berdasarkan bulan
def load_ranking_bulanan(bulan):
    nama_sheet = f'Ranking_{bulan}'

    try:
        ws = sheet.worksheet(nama_sheet)
        data = ws.get_all_records()
        df = pd.DataFrame(data)
        return df
    except Exception:
        st.warning(f'Sheet {nama_sheet} tidak dijumpai.')
        return None


# Senarai Sheet Ranking History
def list_ranking_sheets():
    worksheet_list = sheet.worksheets()
    ranking_sheets = [
        ws.title for ws in worksheet_list if ws.title.startswith('Ranking_')
    ]
    return ranking_sheets
