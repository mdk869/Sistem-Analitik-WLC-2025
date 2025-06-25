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
st.info("""
📢 **Makluman Sistem WLC V3**  
🔔 Update Terbaharu:  
- ✅ Dashboard Interaktif  
- ✅ Leaderboard dengan Medal & Trend  
- ✅ Modul Admin (Tambah, Edit, Padam)  
- ✅ Sistem Login  
- 🔜 Push Notification & Tips Nutrisi (akan datang)  

✨ Terima kasih kerana menggunakan Sistem WLC V3.
""")


# === Footer ===
local_tz = pytz.timezone("Asia/Kuala_Lumpur")
footer_date = datetime.now(local_tz).strftime("%d/%m/%Y")
papar_footer("MKR", footer_date)