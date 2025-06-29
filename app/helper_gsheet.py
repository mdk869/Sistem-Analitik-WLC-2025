import pandas as pd
import streamlit as st
from app.helper_utils import get_worksheet



# ✅ Fungsi load worksheet kepada DataFrame
def load_worksheet_to_df(spreadsheet, worksheet_name):
    try:
        ws = get_worksheet(spreadsheet, worksheet_name)
        if ws is None:
            return pd.DataFrame()

        data = ws.get_all_records()
        if data:
            df = pd.DataFrame(data)
        else:
            df = pd.DataFrame()
            st.warning(f"⚠️ Worksheet '{worksheet_name}' kosong.")
        return df
    except Exception as e:
        st.error(f"❌ Error: {e}")
        return pd.DataFrame()


# ✅ Fungsi simpan DataFrame ke worksheet
def save_df_to_worksheet(spreadsheet, worksheet_name, dataframe):
    try:
        ws = get_worksheet(spreadsheet, worksheet_name)

        if ws is None:
            return False

        ws.clear()  # Kosongkan worksheet dahulu
        ws.update([dataframe.columns.values.tolist()] + dataframe.values.tolist())
        st.success(f"✅ Data berjaya disimpan ke '{worksheet_name}'.")
        return True
    except Exception as e:
        st.error(f"❌ Error: {e}")
        return pd.DataFrame()

    