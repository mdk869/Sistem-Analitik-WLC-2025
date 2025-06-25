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

# === Memo Update Sistem ===
with st.expander("📢 **Makluman Update Sistem WLC V3 - Klik untuk lihat**", expanded=True):
    st.markdown("""
- ✅ **Dashboard Interaktif**  
- ✅ **Leaderboard dengan Medal & Trend**  
- ✅ **Modul Admin (Tambah, Edit, Padam)**  
- ✅ **Sistem Login Admin**  
- ✅ **Integrasi API Motivasi & Cuaca**  
- 🔜 **Push Notification Telegram, Tips Nutrisi Harian**

✨ Terima kasih kerana menggunakan **Sistem WLC V3**.
    """)


# === Kad Maklumat Program ===
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("👥 Jumlah Peserta", "150")
with col2:
    st.metric("📅 Tarikh Mula", "18 Mei 2025")
with col3:
    st.metric("🗓️ Timbang Seterusnya", "20 Julai 2025")


st.divider()


# === Tips Kesihatan & Motivasi ===
st.subheader("💡 Tips Kesihatan & Motivasi Hari Ini")

col4, col5 = st.columns(2)

with col4:
    st.success("""
**🚶‍♂️ Bergeraklah Lebih Banyak!**  
Setiap langkah membantu membakar kalori dan meningkatkan kesihatan jantung anda.
""")

    st.info("""
**🥗 Pilih Pemakanan Sihat**  
Fokus kepada makanan rendah lemak, rendah gula, dan tinggi serat.
""")

with col5:
    st.warning("""
**💧 Minum Air Secukupnya**  
Air membantu metabolisme dan mengurangkan rasa lapar palsu.
""")

    st.success("""
**🧠 Jaga Kesihatan Mental**  
Tidur cukup, rehat secukupnya, dan jangan stress!
""")


st.divider()

# === Footer ===
local_tz = pytz.timezone("Asia/Kuala_Lumpur")
footer_date = datetime.now(local_tz).strftime("%d/%m/%Y")
papar_footer("MKR", footer_date)
