# Home.py
import streamlit as st
from datetime import datetime
import pytz

from app.styles import paparkan_tema, papar_footer, papar_tajuk_utama, papar_kandungan_home

# === Setup Paparan ===
st.set_page_config(
    page_title="Sistem Analitik WLC 2025",
    page_icon="📊",
    layout="wide"
)

# === Paparkan Tema dan Tajuk ===
paparkan_tema()
papar_tajuk_utama()
papar_kandungan_home()

# === Popup Memo Update Sistem ===
if "show_memo" not in st.session_state:
    st.session_state.show_memo = True

if st.session_state.show_memo:
    with st.modal("📢 Makluman Sistem WLC V3"):
        st.subheader("🔔 Update Terbaharu - WLC V3")
        st.markdown("""
        - ✅ **Penambahan Dashboard Interaktif**
        - ✅ Fungsi **Leaderboard dengan Trend Naik/Turun + Medal**
        - ✅ Kemaskini Paparan BMI dengan kategori Asia
        - ✅ Modul Admin lengkap (Tambah, Edit, Padam Peserta)
        - ✅ Sistem login admin (username & password)
        - ✅ Integrasi dengan API Motivasi & Cuaca
        - 🔜 Akan Datang: Push Notification Telegram, Tips Nutrisi Harian

        ---
        """)
        st.success("✨ Terima kasih kerana menggunakan Sistem WLC V3.")
        if st.button("❌ Tutup"):
            st.session_state.show_memo = False


# === Footer ===
local_tz = pytz.timezone("Asia/Kuala_Lumpur")
footer_date = datetime.now(local_tz).strftime("%d/%m/%Y")
papar_footer("MKR", footer_date)