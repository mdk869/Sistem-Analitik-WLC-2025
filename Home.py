# Home.py
import streamlit as st
from datetime import datetime
import pytz
from app.styles import paparkan_tema, papar_footer, papar_tajuk_utama
from app.helper_info import get_motivasi_harian, get_tips_nutrisi

# === Setup Paparan ===
st.set_page_config(
    page_title="Sistem Analitik WLC 2025",
    page_icon="📊",
    layout="wide"
)

# === Paparkan Tema & Tajuk ===
paparkan_tema()
papar_tajuk_utama()

# === Tarikh Countdown Program ===
tz = pytz.timezone("Asia/Kuala_Lumpur")
tarikh_mula = tz.localize(datetime(2025, 5, 18))
tarikh_akhir = tz.localize(datetime(2025, 8, 20))
hari_ini = datetime.now(tz)

total_hari = (tarikh_akhir - tarikh_mula).days
baki_hari = max((tarikh_akhir - hari_ini).days, 0)
progress_hari = ((total_hari - baki_hari) / total_hari) * 100

# === Layout Info Utama ===
st.markdown("##**Selamat Datang ke Sistem Analitik WLC 2025**")
st.markdown("""
Sistem ini direka khas untuk membantu **penganjur** dan **peserta** memantau prestasi penurunan berat badan sepanjang program.

📅 **Tempoh Program:** 18 Mei 2025 - 20 Ogos 2025  
🏆 **Objektif:** Membantu peserta mencapai berat badan ideal melalui pemantauan berkala.

---
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📅 Baki Hari Program", f"{baki_hari} Hari")
    st.progress(progress_hari/100)

with col2:
    st.metric("🚀 Status Program", f"{round(progress_hari, 1)}% Selesai")

with col3:
    motivasi = get_motivasi_harian()
    st.info(f"💡 **Motivasi Hari Ini:**\n{motivasi}")

# === Bahagian Info Kad ===
st.markdown("## 🔍 **Informasi Program & Tips Kesihatan**")

colA, colB = st.columns(2)

with colA:
    st.success("""
    ### 🎯 Matlamat WLC 2025
    - Memupuk gaya hidup sihat.
    - Menurunkan berat badan secara berhemah.
    - Memantau BMI dan komposisi badan.
    - Menyediakan data analitik untuk peserta dan penganjur.
    """)

    st.warning("""
    ### 📌 Kenapa Gunakan Sistem Ini?
    - Memudahkan pemantauan progres.
    - Data direkod secara cloud (Google Sheets).
    - Paparan leaderboard automatik.
    - Privasi data terjamin.
    """)

with colB:
    st.image("https://i.ibb.co/5xSK5dyf/Instagram-Post-Tips-Nutrisi.png", use_container_width=True)
    nutrisi = get_tips_nutrisi(jumlah=2)
    
    st.subheader("🍎 **Tips Nutrisi Hari Ini**")
    st.info(f"🍎 **Tips Nutrisi Hari Ini**{nutrisi}")

# === Popup Memo / Changelog ===
if "show_memo" not in st.session_state:
    st.session_state.show_memo = True

if st.session_state.show_memo:
    st.info("""
    ## 📢 **Makluman Sistem WLC V3**
    🔔 Update Terbaharu:
    - ✅ Dashboard Interaktif
    - ✅ Leaderboard dengan Medal & Trend 📈📉
    - ✅ Modul Admin (Tambah, Edit, Padam)
    - ✅ Sistem Login Admin
    - ✅ Countdown Program + Motivasi Harian
    - 🔜 Akan Datang: Push Notification, Tips Nutrisi Automatik

    ---
    ✨ Terima kasih kerana menggunakan Sistem WLC V3.
    """)
    if st.button("❌ Tutup Memo"):
        st.session_state.show_memo = False

# === Footer ===
footer_date = hari_ini.strftime("%d/%m/%Y")
papar_footer("MKR", footer_date)
