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
    result = {'rekod_berat': False, 'update_peserta': False}

    try:
        # 📅 Tentukan nama sheet
        bulan_tahun = pd.to_datetime(tarikh).strftime('%B%Y')
        sheet_nama = f"rekod_berat_{bulan_tahun}"

        sh = get_spreadsheet_by_name(SPREADSHEET_PESERTA)
        sheet_list = [ws.title for ws in sh.worksheets()]

        # ✅ Create sheet jika belum ada
        if sheet_nama not in sheet_list:
            ws_new = sh.add_worksheet(title=sheet_nama, rows=1000, cols=5)
            ws_new.append_row(["Nama", "Tarikh", "Berat"])
            log_dev("Admin", f"Sheet {sheet_nama} dicipta", "Success")

        # ✅ Simpan data
        ws_rekod = get_worksheet(SPREADSHEET_PESERTA, sheet_nama)
        ws_rekod.append_row([nama, str(tarikh), berat])  # 🚫 Jangan check response!
        log_dev("Admin", f"Rekod berat {nama} pada {tarikh} disimpan ke {sheet_nama}", "Success")
        result['rekod_berat'] = True

    except Exception as e:
        log_error(f"❌ Error simpan ke {sheet_nama}: {e}")
        st.error(f"❌ Error simpan ke {sheet_nama}: {e}")
        result['rekod_berat'] = False


    try:
        # ✅ Update ke sheet peserta
        ws_peserta = get_worksheet(SPREADSHEET_PESERTA, "peserta")

        header = ws_peserta.row_values(1)
        header = [h.strip().replace(" ", "").lower() for h in header]

        def cari_kolum(nama_kolum):
            nama_kolum = nama_kolum.strip().replace(" ", "").lower()
            try:
                return header.index(nama_kolum) + 1
            except ValueError:
                return None

        col_berat = cari_kolum("BeratTerkini")
        col_tarikh = cari_kolum("TarikhTimbang")

        if None in [col_berat, col_tarikh]:
            st.error("❌ Kolum BeratTerkini atau TarikhTimbang tidak ditemui.")
            log_error("❌ Kolum BeratTerkini atau TarikhTimbang tidak ditemui.")
            return result

        data_peserta = ws_peserta.get_all_records()
        df = pd.DataFrame(data_peserta)

        if nama not in df["Nama"].values:
            st.warning(f"⚠️ Nama '{nama}' tidak ditemui dalam sheet peserta.")
            log_warning(f"Nama '{nama}' tidak ditemui dalam sheet peserta.")
            return result

        row_index = df[df["Nama"] == nama].index[0] + 2  # +2 sebab header +1-based

        def colnum_string(n):
            string = ""
            while n > 0:
                n, remainder = divmod(n - 1, 26)
                string = chr(65 + remainder) + string
            return string

        cell_berat = f"{colnum_string(col_berat)}{row_index}"
        cell_tarikh = f"{colnum_string(col_tarikh)}{row_index}"

        ws_peserta.update_acell(cell_berat, float(berat))
        ws_peserta.update_acell(cell_tarikh, str(tarikh))

        log_dev("Admin", f"Update BeratTerkini & TarikhTimbang untuk {nama} di peserta.", "Success")
        result['update_peserta'] = True

    except Exception as e:
        log_error(f"❌ Error update peserta: {e}")
        st.error(f"❌ Error update peserta: {e}")
        result['update_peserta'] = False

    return result



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

def load_rekod_berat_semua():
    """
    Load semua rekod berat dari semua sheet yang bermula dengan 'rekod_berat_*'
    """
    try:
        sh = SPREADSHEET_PESERTA
        sheet_list = [ws.title for ws in sh.worksheets()]
        rekod_list = [s for s in sheet_list if s.lower().startswith("rekod_berat_")]

        if not rekod_list:
            st.warning("⚠️ Tiada sheet bermula dengan 'rekod_berat_'.")
            return pd.DataFrame()

        df_list = []

        for sheet in rekod_list:
            try:
                ws = get_worksheet(SPREADSHEET_PESERTA, sheet)
                data = ws.get_all_records()

                if not data:
                    st.warning(f"⚠️ Sheet '{sheet}' kosong.")
                    continue

                df = pd.DataFrame(data)

                df.columns = df.columns.str.strip().str.title()

                if "Tarikh" not in df.columns:
                    st.warning(f"⚠️ Sheet '{sheet}' tiada kolum 'Tarikh'. Diabaikan.")
                    continue

                df["Tarikh"] = pd.to_datetime(df["Tarikh"], errors='coerce')
                df = df.dropna(subset=["Tarikh"])

                if df.empty:
                    st.warning(f"⚠️ Sheet '{sheet}' tiada data tarikh sah. Diabaikan.")
                    continue

                df["SesiBulan"] = df["Tarikh"].dt.strftime('%B %Y')
                df["Sheet"] = sheet  # Untuk tracking dari sheet mana

                df_list.append(df)

                log_info(f"✅ Berjaya load sheet '{sheet}' ({len(df)} rekod).")

            except Exception as e_sheet:
                log_error(f"❌ Error pada sheet '{sheet}': {e_sheet}")
                st.warning(f"❌ Gagal baca sheet '{sheet}': {e_sheet}")

        if df_list:
            final_df = pd.concat(df_list, ignore_index=True)
        else:
            final_df = pd.DataFrame()

        return final_df

    except Exception as e:
        log_error(f"❌ Error utama load_rekod_berat_semua: {e}")
        st.error(f"❌ Gagal load semua data rekod berat: {e}")
        return pd.DataFrame()



