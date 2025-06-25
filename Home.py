# Home.py
import streamlit as st
from datetime import datetime
import pytz
from app.styles import paparkan_tema, papar_footer

# === Setup Paparan ===
st.set_page_config(
    page_title="Sistem Analitik WLC 2025",
    page_icon="🏋️‍♂️",
    layout="wide"
)

paparkan_tema()

# === Header Utama ===
st.title("🏋️‍♂️ Weight Loss Challenge (WLC) Wilayah Kuala Selangor 2025")
st.subheader("📊 Sistem Analitik · Program Penurunan Berat Badan")

st.info("""
**Selamat datang ke Sistem Analitik WLC 2025!**  
Platform ini dibangunkan khusus untuk membantu *penganjur program* memantau perkembangan peserta sepanjang cabaran berlangsung.

- 🎯 **Objektif:** Membantu peserta mencapai berat badan sihat secara konsisten dan terkawal.
- 🔒 **Privasi:** Data peribadi peserta adalah rahsia dan tidak dipaparkan secara umum.
- 👨‍💻 **Akses:** Sistem ini boleh digunakan oleh peserta untuk melihat maklumat umum, perkembangan program, statistik BMI keseluruhan, dan leaderboard umum.

---
""")

# === Info Program ===
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
### 🎯 Tentang Program WLC 2025
- 📅 **Tempoh Program:** 18 Mei 2025 - 20 Ogos 2025  
- 🏢 **Lokasi:** Wilayah Kuala Selangor  
- 🧠 **Konsep:** Penurunan berat badan secara sihat, berilmu, dan diselia  
- 🥇 **Kriteria Kemenangan:** Berdasarkan **% penurunan berat badan tertinggi**  

### 🚀 Apa Yang Anda Akan Dapat?
- Dashboard visual perkembangan peserta (secara umum)  
- Tips pemakanan sihat dan aktiviti fizikal  
- Info BMI populasi peserta  
- Paparan leaderboard (tanpa dedahan berat individu)

---
    """)

with col2:
    st.image("https://i.ibb.co/hZV4QF6/healthy.png", use_column_width=True)


# === Maklumat Tambahan ===
st.markdown("""
## 🔍 Fungsi Utama Sistem
- 📈 **Dashboard Analitik:** Paparan graf penurunan berat, BMI dan statistik kategori peserta.
- 🏆 **Leaderboard:** Senarai peserta dengan peratus penurunan berat terbaik.
- 🔐 **Admin Panel:** Modul khas untuk penganjur program bagi mengurus peserta.  

---
""")

st.success("""
💡 **Nota:**  
Akses penuh kepada pengurusan data hanya diberikan kepada pihak *penganjur program* melalui modul Admin. Peserta hanya boleh melihat paparan umum, tanpa akses kepada maklumat peribadi individu.
""")

# === Footer ===
local_tz = pytz.timezone("Asia/Kuala_Lumpur")
footer_date = datetime.now(local_tz).strftime("%d/%m/%Y")
papar_footer("MKR", footer_date)
