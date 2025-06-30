import streamlit as st
import pandas as pd
from gspread.exceptions import WorksheetNotFound

from app.helper_connection import get_sheet


# =========================================
# ✅ Load Worksheet ke DataFrame
# =========================================
def load_worksheet_to_df(spreadsheet_id, sheet_name):
    try:
        sh = get_sheet(spreadsheet_id)
        ws = sh.worksheet(sheet_name)
        data = ws.get_all_records()
        df = pd.DataFrame(data)
        return df
    except WorksheetNotFound:
        st.warning(f"⚠️ Sheet '{sheet_name}' tidak wujud.")
        return pd.DataFrame()
    except Exception as e:
        st.warning(f"⚠️ Error load sheet '{sheet_name}': {e}")
        return pd.DataFrame()


# =========================================
# ✅ Save DataFrame ke Worksheet (Replace)
# =========================================
def save_df_to_worksheet(spreadsheet_id, sheet_name, df):
    try:
        sh = get_sheet(spreadsheet_id)
        try:
            ws = sh.worksheet(sheet_name)
        except WorksheetNotFound:
            ws = sh.add_worksheet(title=sheet_name, rows="1000", cols="50")

        ws.clear()

        if not df.empty:
            header = list(df.columns)
            values = [header] + df.astype(str).values.tolist()
            ws.update("A1", values)

        return True
    except Exception as e:
        st.error(f"❌ Gagal simpan ke sheet '{sheet_name}': {e}")
        return False


# =========================================
# ✅ Append Row ke Worksheet
# =========================================
def append_row_to_worksheet(spreadsheet_id, sheet_name, row_dict):
    df = load_worksheet_to_df(spreadsheet_id, sheet_name)
    df = pd.concat([df, pd.DataFrame([row_dict])], ignore_index=True)
    return save_df_to_worksheet(spreadsheet_id, sheet_name, df)


# =========================================
# ✅ Update Baris Berdasarkan Key Column
# =========================================
def update_baris_dalam_worksheet(spreadsheet_id, sheet_name, key_column, key_value, update_dict):
    df = load_worksheet_to_df(spreadsheet_id, sheet_name)
    if df.empty:
        st.warning(f"⚠️ Sheet '{sheet_name}' kosong atau tidak wujud.")
        return False

    index = df[df[key_column] == key_value].index
    if not index.empty:
        idx = index[0]
        for col, val in update_dict.items():
            if col in df.columns:
                df.at[idx, col] = val
        save_df_to_worksheet(spreadsheet_id, sheet_name, df)
        return True
    else:
        st.warning(f"⚠️ Key '{key_value}' tidak dijumpai dalam '{key_column}'.")
        return False


# =========================================
# ✅ Delete Baris Berdasarkan Key Column
# =========================================
def delete_baris_dalam_worksheet(spreadsheet_id, sheet_name, key_column, key_value):
    df = load_worksheet_to_df(spreadsheet_id, sheet_name)
    if df.empty:
        st.warning(f"⚠️ Sheet '{sheet_name}' kosong atau tidak wujud.")
        return False

    new_df = df[df[key_column] != key_value]
    if len(new_df) == len(df):
        st.warning(f"⚠️ Key '{key_value}' tidak dijumpai dalam '{key_column}'.")
        return False

    save_df_to_worksheet(spreadsheet_id, sheet_name, new_df)
    return True


# =========================================
# ✅ Semak & Cipta Sheet Jika Tiada
# =========================================
def check_or_create_sheet(spreadsheet_id, sheet_name, header_list):
    try:
        sh = get_sheet(spreadsheet_id)
        try:
            sh.worksheet(sheet_name)
        except WorksheetNotFound:
            ws = sh.add_worksheet(title=sheet_name, rows="1000", cols="50")
            ws.append_row(header_list)
        return True
    except Exception as e:
        st.error(f"❌ Gagal semak/cipta sheet '{sheet_name}': {e}")
        return False


# =========================================
# ✅ Load Banyak Sheet Ikut Prefix (contoh: rekod_berat_*)
# =========================================
def load_multiple_sheets_by_prefix(spreadsheet_id, prefix):
    try:
        sh = get_sheet(spreadsheet_id)
        sheet_list = [ws.title for ws in sh.worksheets() if ws.title.startswith(prefix)]

        df_list = []
        for sheet in sheet_list:
            df = load_worksheet_to_df(spreadsheet_id, sheet)
            if not df.empty:
                df["Sheet"] = sheet
                df_list.append(df)

        if df_list:
            return pd.concat(df_list, ignore_index=True)
        else:
            return pd.DataFrame()

    except Exception as e:
        st.error(f"❌ Gagal load sheets dengan prefix '{prefix}': {e}")
        return pd.DataFrame()
