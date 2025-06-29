import pandas as pd
from datetime import datetime
from app.helper_connection import SPREADSHEET_PESERTA, SPREADSHEET_RANKING
from app.helper_gsheet import load_worksheet_to_df, save_df_to_worksheet


def load_data_peserta():
    df = load_worksheet_to_df(SPREADSHEET_PESERTA, "peserta")
    return df


def load_rekod_berat_semua():
    df = load_worksheet_to_df(SPREADSHEET_RANKING, "rekod")
    return df


def tambah_peserta_google_sheet(nama, nostaf, umur, jantina, jabatan, tinggi, berat_awal, tarikh):
    ws = SPREADSHEET_PESERTA.worksheet("peserta")
    ws.append_row([
        nama, nostaf, umur, jantina, jabatan,
        tinggi, berat_awal, tarikh.strftime('%Y-%m-%d'),
        berat_awal, tarikh.strftime('%Y-%m-%d'), '', ''
    ])


def simpan_rekod_berat(nama, tarikh, berat):
    try:
        df_rekod = load_rekod_berat_semua()

        tarikh_obj = pd.to_datetime(tarikh)
        sesi_bulan = tarikh_obj.strftime("%Y-%m")

        new_row = {
            'Nama': nama,
            'Tarikh': tarikh,
            'Berat': berat,
            'SesiBulan': sesi_bulan
        }

        df_rekod = pd.concat([df_rekod, pd.DataFrame([new_row])], ignore_index=True)

        save_df_to_worksheet(SPREADSHEET_RANKING, "rekod", df_rekod)

        # Update berat terkini peserta
        df_peserta = load_data_peserta()
        df_peserta.loc[df_peserta['Nama'].str.lower() == nama.lower(), 'BeratTerkini'] = berat
        df_peserta.loc[df_peserta['Nama'].str.lower() == nama.lower(), 'TarikhTimbang'] = tarikh

        save_df_to_worksheet(SPREADSHEET_PESERTA, "peserta", df_peserta)

        return {"rekod_berat": True, "update_peserta": True}

    except Exception as e:
        return {"rekod_berat": False, "update_peserta": False, "error": str(e)}


def padam_peserta_dari_sheet(nama):
    df = load_data_peserta()
    df = df[df["Nama"].str.lower() != nama.lower()]
    save_df_to_worksheet(SPREADSHEET_PESERTA, "peserta", df)
    return True


def update_data_peserta(nama, nostaf, umur, jantina, jabatan, tinggi, berat_terkini, tarikh_timbang, bmi, kategori):
    df = load_data_peserta()
    mask = df['Nama'].str.lower() == nama.lower()

    df.loc[mask, 'NoStaf'] = nostaf
    df.loc[mask, 'Umur'] = umur
    df.loc[mask, 'Jantina'] = jantina
    df.loc[mask, 'Jabatan'] = jabatan
    df.loc[mask, 'Tinggi'] = tinggi
    df.loc[mask, 'BeratTerkini'] = berat_terkini
    df.loc[mask, 'TarikhTimbang'] = tarikh_timbang.strftime('%Y-%m-%d')
    df.loc[mask, 'BMI'] = bmi
    df.loc[mask, 'Kategori'] = kategori

    save_df_to_worksheet(SPREADSHEET_PESERTA, "peserta", df)
    return True
