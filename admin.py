# admin.py
import streamlit as st
import pandas as pd
from datetime import datetime
import tempfile
import pytz

from app.helper_auth import check_admin_auth
from app.helper_data import load_data, save_ranking, is_cloud
from app.helper_logic import tambah_kiraan_peserta

st.set_page_config(page_title="Admin WLC 2025", layout="wide")
st.title("🔐 Admin Panel - WLC 2025")

# --- AUTH ---
with st.sidebar:
    st.header("Login Admin")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Login")

if login_btn:
    if check_admin_auth(username, password):
        st.session_state["auth"] = True
        st.session_state["user"] = username
    else:
        st.error("❌ Login gagal. Sila cuba lagi.")

if not st.session_state.get("auth"):
    st.warning("Sila login untuk akses ciri pentadbir.")
    st.stop()

# --- LOAD DATA ---
df = load_data()
df = tambah_kiraan_peserta(df)
df_leaderboard = df.sort_values("% Penurunan", ascending=False).reset_index(drop=True)
df_leaderboard["Ranking"] = df_leaderboard.index + 1

st.subheader("🏆 Leaderboard Semasa")
st.dataframe(df_leaderboard[["Ranking", "Nama", "% Penurunan", "BeratAwal", "BeratTerkini"]], use_container_width=True)

# --- SIMPAN RANKING ---
if st.button("💾 Simpan Ranking ke Excel & Google Drive"):
    rekod_df = df_leaderboard[["Nama", "Ranking"]]
    path_file = save_ranking(rekod_df)

    if is_cloud():
        from pydrive2.auth import GoogleAuth
        from pydrive2.drive import GoogleDrive
        from google.oauth2 import service_account

        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=["https://www.googleapis.com/auth/drive"]
        )

        gauth = GoogleAuth()
        gauth.credentials = credentials
        drive = GoogleDrive(gauth)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp_file:
            rekod_df.to_excel(tmp_file.name, index=False)
            file_drive = drive.CreateFile({
                'title': 'rekod_ranking_semasa.xlsx',
                'parents': [{'id': '1XR6OlFeiDLet9niwsUdmvKW4GGKNOkgT'}]  # Folder ID Google Drive
            })
            file_drive.SetContentFile(tmp_file.name)
            file_drive.Upload()

        st.success("✅ Ranking berjaya disimpan & dimuat naik ke Google Drive.")
    else:
        st.success(f"✅ Ranking berjaya disimpan ke fail: {path_file}")

# --- Footer ---
footer_date = datetime.now(pytz.timezone("Asia/Kuala_Lumpur")).strftime("%d/%m/%Y")
st.markdown(f"""
<hr>
<div style='font-size:14px;'>
    <strong>Admin Panel WLC 2025</strong> | Login sebagai: <code>{st.session_state['user']}</code><br>
    Kemaskini terakhir: {footer_date}
</div>
""", unsafe_allow_html=True)
