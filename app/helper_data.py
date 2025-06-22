# helper_data.py
import os
import pandas as pd
import streamlit as st

from google.oauth2 import service_account
import gspread


def is_cloud():
    try:
        _ = st.secrets["gcp_service_account"]
        return True
    except st.errors.StreamlitSecretNotFoundError:
        return False


def load_data():
    if is_cloud():
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"], scopes=scope
        )
        client = gspread.authorize(credentials)
        sheet = client.open("peserta").worksheet("Sheet1")
        data = sheet.get_all_records()
        return pd.DataFrame(data)
    else:
        DIR_SEMASA = os.path.dirname(os.path.abspath(__file__))
        FILE_EXCEL = os.path.join(DIR_SEMASA, "../data/peserta.xlsx")
        if os.path.exists(FILE_EXCEL):
            return pd.read_excel(FILE_EXCEL)
        else:
            st.error("❌ Fail peserta.xlsx tidak dijumpai. Sila pastikan fail wujud dalam direktori data.")
            st.stop()


def save_ranking(df_rekod):
    DIR_SEMASA = os.path.dirname(os.path.abspath(__file__))
    FILE_REKOD = os.path.join(DIR_SEMASA, "../data/rekod_ranking_semasa.xlsx")
    df_rekod.to_excel(FILE_REKOD, index=False)
    return FILE_REKOD
