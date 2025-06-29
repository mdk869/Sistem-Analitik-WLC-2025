# app/helper_data.py

import streamlit as st
import pandas as pd
import datetime
from app.helper_connection import SPREADSHEET_PESERTA, get_spreadsheet_by_name
from app.helper_utils import save_dataframe_to_excel, kategori_bmi_asia, get_column_index
from app.helper_log import log_dev, log_error, log_info, log_warning
from app.helper_gsheet import get_worksheet



# ------------------------------------
# ✅ Fungsi Load Data Peserta
# ------------------------------------
def load_data_peserta():
    try:
        ws = get_worksheet(SPREADSHEET_PESERTA, "peserta")
        data = ws.get_all_records()
        df = pd.DataFrame(data)

        if df.empty:
            st.warning("🚫 Data peserta kosong.")
        return df

    except Exception as e:
        st.error(f"❌ Gagal load data peserta: {e}")
        return pd.DataFrame()
    
# ------------------------------------
# ✅ Simpan Dataframe ke Sheet Peserta
# ------------------------------------
def save_data_peserta(df):
    try:
        ws = get_worksheet(SPREADSHEET_PESERTA, "peserta")
        ws.clear()

        ws.update([df.columns.values.tolist()] + df.values.tolist())
        st.success("✅ Data peserta berjaya disimpan ke Google Sheet.")

    except Exception as e:
        st.error(f"❌ Gagal simpan data peserta: {e}")


# ------------------------------------
# ✅ Fungsi Backup Data Peserta ke Excel
# ------------------------------------
def backup_data_peserta(df):
    try:
        filename = f"backup_data_peserta_{datetime.datetime.now().strftime('%Y%m%d')}.xlsx"
        save_dataframe_to_excel(df, filename)
        st.info(f"📦 Backup data peserta disimpan: {filename}")
        return filename
    except Exception as e:
        st.error(f"❌ Gagal backup data: {e}")


# ------------------------------------
# ✅ Tambah Peserta Baru
# ------------------------------------
def tambah_peserta_google_sheet(nama, nostaf, umur, jantina, jabatan, tinggi, berat_awal, tarikh_daftar):
    df = load_data_peserta()

    berat_terkini = berat_awal
    bmi = round(berat_awal / ((tinggi / 100) ** 2), 2)
    kategori = kategori_bmi_asia(bmi)

    new_data = {
        "Nama": nama,
        "NoStaf": nostaf,
        "Umur": umur,
        "Jantina": jantina,
        "Jabatan": jabatan,
        "Tinggi": tinggi,
        "BeratAwal": berat_awal,
        "TarikhDaftar": str(tarikh_daftar),
        "BeratTerkini": berat_terkini,
        "TarikhTimbang": str(tarikh_daftar),
        "BMI": bmi,
        "Kategori": kategori,
    }

    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    save_data_peserta(df)


# ------------------------------------
# ✅ Kemaskini Berat Terkini Peserta
# ------------------------------------
def kemaskini_berat_peserta(nama, berat_baru, tarikh_baru):
    df = load_data_peserta()

    if nama in df['Nama'].values:
        idx = df[df['Nama'] == nama].index[0] 
        df.at[idx, 'BeratTerkini'] = berat_baru
        df.at[idx, 'TarikhTimbang'] = str(tarikh_baru)

        tinggi = df.at[idx, 'Tinggi']
        bmi = round(berat_baru / ((tinggi / 100) ** 2), 2)
        kategori = kategori_bmi_asia(bmi)

        df.at[idx, 'BMI'] = bmi
        df.at[idx, 'Kategori'] = kategori

        save_data_peserta(df)
    else:
        st.error("❌ Nama peserta tidak dijumpai.")


# ------------------------------------
# ✅ Padam Peserta dari Sheet
# ------------------------------------
def padam_peserta_dari_sheet(nama):
    df = load_data_peserta()

    if nama in df['Nama'].values:
        df = df[df['Nama'] != nama]
        save_data_peserta(df)
        return True
    else:
        st.warning("⚠️ Nama tidak dijumpai dalam senarai.")
        return False


# ------------------------------------
# ✅ Simpan Rekod Berat
# ------------------------------------
def simpan_rekod_berat(nama, tarikh, berat):
    """
    Simpan data ke rekod_berat_BulanTahun (auto create jika belum ada).
    Update juga kolum BeratTerkini dan TarikhTimbang dalam sheet peserta.
    """
    try:
        # Format bulan tahun
        bulan_tahun = pd.to_datetime(tarikh).strftime('%B%Y')
        sheet_nama = f"rekod_berat_{bulan_tahun}"

        # ✅ Semak sheet - create jika belum ada
        sh = get_spreadsheet_by_name(SPREADSHEET_PESERTA)
        sheet_list = [ws.title for ws in sh.worksheets()]

        if sheet_nama not in sheet_list:
            ws_new = sh.add_worksheet(title=sheet_nama, rows=1000, cols=5)
            ws_new.append_row(["Nama", "Tarikh", "Berat"])
            log_dev("Admin", f"Sheet {sheet_nama} berjaya dicipta", "Success")

        # ✅ Simpan ke rekod_berat bulan itu
        ws = get_worksheet(SPREADSHEET_PESERTA, sheet_nama)
        ws.append_row([nama, str(tarikh), berat])
        log_dev("Admin", f"Rekod berat {nama} pada {tarikh} disimpan ke {sheet_nama}", "Success")

        # ✅ Update ke sheet peserta (kolum BeratTerkini dan TarikhTimbang)
        ws_peserta = get_worksheet(SPREADSHEET_PESERTA, "peserta")
        data_peserta = ws_peserta.get_all_records()
        df = pd.DataFrame(data_peserta)

        if nama in df["Nama"].values:
            row_index = df[df["Nama"] == nama].index[0] + 2  # +2 kerana header +1-based index

            ws_peserta.update(f"H{row_index}", berat)  # BeratTerkini di kolum H
            ws_peserta.update(f"I{row_index}", str(tarikh))  # TarikhTimbang di kolum I

            log_dev("Admin", f"BeratTerkini dan TarikhTimbang untuk {nama} dikemaskini", "Success")

        return True

    except Exception as e:
        log_error(str(e))
        st.error(f"❌ Gagal simpan rekod berat: {e}")
        return False



# -----------------------------------------------
# ✅ Update Berat Terkini ke Sheet Peserta
# -----------------------------------------------
def update_berat_terkini_peserta(nama, tarikh, berat):
    """
    Update BeratTerkini dan TarikhTimbang pada worksheet peserta.
    """
    try:
        ws = get_worksheet(SPREADSHEET_PESERTA, "peserta")
        data = ws.get_all_records()

        # Cari index row peserta
        for idx, row in enumerate(data):
            if row["Nama"].strip() == nama.strip():
                ws.update_cell(idx + 2, get_column_index(ws, "BeratTerkini"), berat)
                ws.update_cell(idx + 2, get_column_index(ws, "TarikhTimbang"), tarikh)
                log_dev("Admin", f"Update berat terkini {nama} pada {tarikh}", "Success")
                return True

        st.warning(f"⚠️ Nama {nama} tidak ditemui dalam senarai peserta.")
        return False

    except Exception as e:
        st.error(f"❌ Gagal update berat terkini: {e}")
        log_error(str(e))
        return False


# =======================
# ✅ Load Data Rekod Berat
# =======================
def load_rekod_berat():
    try:
        ws = get_worksheet(SPREADSHEET_PESERTA, "peserta")
        data = ws.get_all_records()
        df = pd.DataFrame(data)
        if not df.empty:
            df["TarikhTimbang"] = pd.to_datetime(df["TarikhTimbang"], errors='coerce')
            df = df.rename(columns={
                "TarikhTimbang": "Tarikh"
            })
        return df
    
    except Exception as e:
        st.error(f"❌ Gagal load data rekod berat: {e}")
        return pd.DataFrame()

def load_berat_peserta_terkini():
    """
    Load data berat terkini dan tarikh timbang dari sheet 'data_peserta'
    """
    try:
        ws = get_worksheet(SPREADSHEET_PESERTA, "data_peserta")
        data = ws.get_all_records()

        if not data:
            st.warning("⚠️ Sheet 'data_peserta' kosong.")
            log_warning("Sheet 'data_peserta' kosong.")
            return pd.DataFrame()

        df = pd.DataFrame(data)

        # Normalize column names
        df.columns = df.columns.str.strip().str.title()

        required_columns = ["Beratt erkini", "Tarikhtimbang"]
        available_columns = df.columns.str.replace(" ", "").str.lower().tolist()

        # Map untuk pastikan nama kolum betul
        column_map = {
            "beratterkini": "BeratTerkini",
            "tarikhtimbang": "TarikhTimbang"
        }

        # Semak jika kolum diperlukan ada
        missing_columns = [
            name for name in column_map.keys() if name not in available_columns
        ]

        if missing_columns:
            st.warning(f"⚠️ Sheet 'data_peserta' tiada kolum: {', '.join(missing_columns)}")
            log_warning(f"Missing columns in data_peserta: {missing_columns}")
            return pd.DataFrame()

        # Rename kolum ikut map
        rename_dict = {}
        for col in df.columns:
            key = col.replace(" ", "").lower()
            if key in column_map:
                rename_dict[col] = column_map[key]

        df = df.rename(columns=rename_dict)

        # Convert TarikhTimbang ke datetime
        df["TarikhTimbang"] = pd.to_datetime(df["TarikhTimbang"], errors="coerce")

        # Filter NaT pada TarikhTimbang
        df = df.dropna(subset=["TarikhTimbang"])

        # Hanya ambil dua kolum utama + optional Nama/NoStaf jika nak
        selected_columns = ["BeratTerkini", "TarikhTimbang"]
        optional_columns = [col for col in ["Nama", "NoStaf"] if col in df.columns]
        final_columns = optional_columns + selected_columns

        df_final = df[final_columns].copy()

        log_info(f"✅ Berjaya load 'data_peserta' dengan {len(df_final)} rekod.")

        return df_final

    except Exception as e:
        log_error(f"❌ Error load_berat_peserta_terkini: {e}")
        st.error(f"❌ Gagal load data dari 'data_peserta': {e}")
        return pd.DataFrame()



