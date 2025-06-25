import streamlit as st
from datetime import datetime, timedelta
import pytz
import random
import requests
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

# === Countdown ke Timbang Akhir ===
st.subheader("⏳ Countdown ke Timbang Akhir")
tarikh_timbang_akhir = datetime(2025, 8, 20, 8, 0, 0)
now = datetime.now(pytz.timezone("Asia/Kuala_Lumpur"))
countdown = tarikh_timbang_akhir - now
days = countdown.days
hours, remainder = divmod(countdown.seconds, 3600)
minutes, seconds = divmod(remainder, 60)
st.success(f"📅 {days} hari, ⏰ {hours} jam {minutes} minit {seconds} saat lagi!")

# === Fun Fact Kesihatan ===
st.subheader("🍏 Fun Fact Kesihatan")
facts = [
    "🥦 Brokoli mengandungi lebih protein daripada daging per kalori!",
    "💧 Minum air sebelum makan boleh bantu kurangkan pengambilan kalori.",
    "🧠 Tidur yang cukup bantu pembakaran lemak lebih efektif.",
    "🔥 10 minit lompat tali membakar lebih banyak kalori daripada joging 30 minit.",
    "🍋 Lemon membantu penghadaman dan detox semula jadi."
]
st.info(random.choice(facts))

# === Petikan Motivasi ===
st.subheader("💡 Petikan Motivasi Hari Ini")
try:
    res = requests.get("https://api.adviceslip.com/advice")
    if res.status_code == 200:
        advice = res.json()["slip"]["advice"]
        st.success(f"🌟 \"{advice}\"")
    else:
        st.error("❌ Tidak dapat memuatkan petikan motivasi.")
except:
    st.warning("⚠️ Gagal mendapatkan petikan motivasi.")

# === FAQ Interaktif ===
st.subheader("❓ Soalan Lazim (FAQ)")
with st.expander("📝 Bagaimana sistem ini berfungsi?"):
    st.write("""
    Sistem ini membantu penganjur memantau kemajuan peserta dalam program penurunan berat badan.
    Data seperti berat badan, BMI, dan leaderboard akan dikemaskini oleh admin.
    """)

with st.expander("🔒 Adakah data peserta dipaparkan kepada umum?"):
    st.write("""
    Tidak. Data individu tidak dipaparkan kepada umum. Hanya data umum dan statistik keseluruhan yang boleh dilihat.
    """)

with st.expander("📅 Bilakah sesi timbang seterusnya?"):
    st.write("""
    Sesi timbang seterusnya dijadualkan pada **20 Julai 2025**.
    """)

with st.expander("📊 Apa yang boleh dilihat dalam Dashboard?"):
    st.write("""
    Anda boleh lihat perkembangan keseluruhan, statistik BMI peserta, dan leaderboard % penurunan berat.
    """)

# === Quick Navigation ===
st.subheader("🚀 Pergi ke:")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Dashboard"):
        st.switch_page("pages/dashboard.py")

with col2:
    if st.button("🏆 Leaderboard"):
        st.switch_page("pages/leaderboard.py")

with col3:
    if st.button("⚖️ Info BMI"):
        st.switch_page("pages/bmi.py")

# === Footer ===
local_tz = pytz.timezone("Asia/Kuala_Lumpur")
footer_date = datetime.now(local_tz).strftime("%d/%m/%Y")
papar_footer("MKR", footer_date)
