import streamlit as st
from datetime import datetime
import pytz
from app.styles import paparkan_tema, papar_footer


# === Setup Paparan ===
st.set_page_config(
    page_title="WLC 2025 - Home",
    page_icon="🏠",
    layout="wide"
)

# === Paparan Tema ===
paparkan_tema()

# === Hero Section ===
st.markdown("""
<div style="text-align:center">
    <h1 style="color:#FFB800;">🏋️‍♂️ Weight Loss Challenge 2025</h1>
    <h3 style="margin-top:-10px;">Menuju Berat Ideal, Hidup Lebih Sihat!</h3>
    <p>Inisiatif Kesihatan <strong>Wilayah Kuala Selangor</strong> bagi memupuk gaya hidup sihat melalui cabaran penurunan berat badan.</p>
</div>
""", unsafe_allow_html=True)


st.divider()

# === Tentang Program ===
with st.container():
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("❓ Apa itu WLC 2025?")
        st.markdown("""
        **Weight Loss Challenge (WLC) 2025** adalah program komuniti yang bertujuan untuk:  
        - ✅ Meningkatkan kesedaran tentang kepentingan berat badan sihat.  
        - ✅ Menggalakkan aktiviti fizikal & pemakanan sihat.  
        - ✅ Memantau perkembangan penurunan berat badan secara sistematik.

        **🗓️ Tempoh Program:** 18 Mei 2025 - 20 Ogos 2025  
        """)
        st.success("Semua data yang dipaparkan adalah statistik umum program. Akses penuh kepada data peserta hanya oleh pihak penganjur (Admin).")

    with col2:
        st.image("https://i.ibb.co/hZV4QF6/healthy.png", use_column_width=True)

st.divider()

# === Tentang WebApp ===
st.subheader("🌐 Tentang WebApp WLC 2025")
st.markdown("""
Aplikasi ini direka untuk:  
- ✅ Memaparkan perkembangan program secara umum.  
- ✅ Menunjukkan visual statistik, carta BMI & leaderboard.  
- ✅ Membantu penganjur (Admin) mengurus data melalui **Admin Panel**.

> ⚠️ **Tiada fungsi login untuk peserta.** Web ini terbuka untuk paparan umum sahaja.  
> ✅ **Login hanya untuk penganjur bagi urusan pengurusan data.**
""")

st.divider()

# === Kad Status Program ===
st.subheader("📊 Status Semasa Program")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("👥 Jumlah Peserta", "150")
with col2:
    st.metric("🚀 Status Program", "Sedang Berjalan")
with col3:
    st.metric("📅 Tarikh Mula", "18 Mei 2025")
with col4:
    st.metric("🗓️ Timbang Seterusnya", "20 Julai 2025")

st.divider()

# === FAQ Ringkas ===
st.subheader("💡 FAQ (Soalan Lazim)")

faq = st.expander("🧑‍💻 Siapa boleh akses sistem ini?")
faq.write("✅ Semua boleh akses untuk melihat perkembangan program secara umum. Akses pengurusan hanya untuk penganjur (Admin).")

faq = st.expander("🔐 Adakah data peserta dipaparkan?")
faq.write("❌ Tidak. Hanya data agregat atau statistik umum dipaparkan. Data individu tidak dikongsi secara awam.")

faq = st.expander("🔑 Bagaimana penganjur login?")
faq.write("✅ Melalui Admin Panel dengan username & password khas untuk penganjur.")

faq = st.expander("🎯 Adakah peserta boleh kemaskini berat sendiri?")
faq.write("❌ Tidak. Semua kemaskini dilakukan oleh penganjur sahaja.")

st.divider()

# === Pengumuman ===
st.subheader("📢 Pengumuman Terkini")
st.info("""
- ✅ **Leaderboard** kini dilengkapi dengan trend naik/turun & sistem medal.
- ✅ Paparan BMI telah dikemaskini dengan kategori Asia.
- ✅ Timbang seterusnya adalah pada **20 Julai 2025**.
- 🔜 Akan datang: Push Notification Telegram & Tips Nutrisi Harian.
""")

st.divider()

# === Footer ===
local_tz = pytz.timezone("Asia/Kuala_Lumpur")
footer_date = datetime.now(local_tz).strftime("%d/%m/%Y")
papar_footer("MKR", footer_date)
