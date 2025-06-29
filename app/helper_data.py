import pandas as pd
from datetime import datetime
from app.helper_connection import SPREADSHEET_PESERTA, SPREADSHEET_RANKING
from app.helper_gsheet import load_worksheet_to_df, save_df_to_worksheet
from app.helper_log_utils import log_event, log_error


def load_data_peserta():
    try:
        df = load_worksheet_to_df(SPREADSHEET_PESERTA, "peserta")
        return df
    except Exception as e:
        log_error("helper_data", f"Load Data Peserta Error: {e}")
        return pd.DataFrame()


def load_rekod_berat_semua():
    try:
        df = load_worksheet_to_df(SPREADSHEET_RANKING, "rekod")
        return df
    except Exception as e:
        log_error("helper_data", f"Load Rekod Berat Error: {e}")
        return pd.DataFrame()


def tambah_peserta_google_sheet(nama, nostaf, umur, jantina, jabatan, tinggi, berat_awal, tarikh):
    try:
        tarikh_str = tarikh.strftime('%Y-%m-%d')
        bmi = round(berat_awal / ((tinggi / 100) ** 2), 2)
        kategori = kategori_bmi_asia(bmi)

        row = [nama, nostaf, umur, jantina, jabatan, tinggi, berat_awal, tarikh_str,
               berat_awal, tarikh_str, bmi, kategori]

        ws = SPREADSHEET_PESERTA.worksheet("peserta")
        ws.append_row(row)
        log_event("helper_data", f"Tambah Peserta {nama}")
        return True
    except Exception as e:
        log_error("helper_data", f"Tambah Peserta Error: {e}")
        return False


def simpan_rekod_berat(nama, tarikh, berat):
    try:
        ws_rekod = SPREADSHEET_RANKING.worksheet("rekod")
        ws_rekod.append_row([nama, tarikh, berat])

        # Update berat terkini dalam peserta
        df = load_data_peserta()
        idx = df.index[df['Nama'].str.lower() == nama.lower()]

        if not idx.empty:
            df.at[idx[0], 'BeratTerkini'] = berat
            df.at[idx[0], 'TarikhTimbang'] = tarikh

            bmi = round(berat / ((df.at[idx[0], 'Tinggi'] / 100) ** 2), 2)
            kategori = kategori_bmi_asia(bmi)

            df.at[idx[0], 'BMI'] = bmi
            df.at[idx[0], 'Kategori'] = kategori

            save_df_to_worksheet(SPREADSHEET_PESERTA, "peserta", df)

            log_event("helper_data", f"Simpan Rekod Berat {nama}")
            return {"rekod_berat": True, "update_peserta": True}
        else:
            return {"rekod_berat": False, "update_peserta": False}

    except Exception as e:
        log_error("helper_data", f"Simpan Rekod Berat Error: {e}")
        return {"rekod_berat": False, "update_peserta": False}


def padam_peserta_dari_sheet(nama):
    try:
        df = load_data_peserta()
        df_new = df[df["Nama"].str.lower() != nama.lower()]
        save_df_to_worksheet(SPREADSHEET_PESERTA, "peserta", df_new)
        log_event("helper_data", f"Padam Peserta {nama}")
        return True
    except Exception as e:
        log_error("helper_data", f"Padam Peserta Error: {e}")
        return False


def update_data_peserta(nama, nostaf, umur, jantina, jabatan, tinggi, berat, tarikh, bmi, kategori):
    try:
        df = load_data_peserta()
        idx = df.index[df['Nama'].str.lower() == nama.lower()]

        if not idx.empty:
            df.at[idx[0], 'NoStaf'] = nostaf
            df.at[idx[0], 'Umur'] = umur
            df.at[idx[0], 'Jantina'] = jantina
            df.at[idx[0], 'Jabatan'] = jabatan
            df.at[idx[0], 'Tinggi'] = tinggi
            df.at[idx[0], 'BeratTerkini'] = berat
            df.at[idx[0], 'TarikhTimbang'] = tarikh.strftime('%Y-%m-%d')
            df.at[idx[0], 'BMI'] = bmi
            df.at[idx[0], 'Kategori'] = kategori

            save_df_to_worksheet(SPREADSHEET_PESERTA, "peserta", df)
            log_event("helper_data", f"Kemaskini Peserta {nama}")
            return True
        else:
            return False

    except Exception as e:
        log_error("helper_data", f"Update Peserta Error: {e}")
        return False


# Helper tambahan
def kategori_bmi_asia(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 23:
        return "Normal"
    elif 23 <= bmi < 27.5:
        return "Overweight"
    else:
        return "Obese"
