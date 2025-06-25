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
    <h3>Menuju Berat Ideal, Hidup Lebih Sihat!</h3>
    <p>Sebuah inisiatif untuk menggalakkan gaya hidup sihat di <strong>Wilayah Kuala Selangor</strong>.</p>
</div>
""", unsafe_allow_html=True)


st.divider()

# === Tentang Program ===
st.subheader("❓ Tentang Program WLC 2025")
st.markdown("""
Program **Weight Loss Challenge (WLC) 2025** adalah satu kempen gaya hidup sihat  
untuk membantu peserta menurunkan berat badan dengan cara sihat, konsisten dan berinformasi.

**🗓️ Tempoh Program:** 18 Mei 2025 - 20 Ogos 2025  
**🎯 Objektif:**  
- Meningkatkan kesedaran tentang pentingnya menjaga berat badan.  
- Menggalakkan aktiviti fizikal secara berkala.  
- Memberi pendedahan tentang pemakanan sihat dan kawalan berat badan.

**🔒 Privasi:**  
Sistem ini memastikan data peserta disimpan secara selamat dan hanya boleh diakses oleh peserta sendiri dan penganjur.
""")

st.divider()

# === Tentang WebApp ===
st.subheader("🌐 Tentang WebApp WLC 2025")
st.markdown("""
WebApp ini direka untuk memudahkan:  
- ✅ Peserta memantau perkembangan berat badan.  
- ✅ Melihat trend BMI dan ranking peserta (Leaderboard).  
- ✅ Panel Admin untuk pengurusan data dan program.

**Nota:**  
Dashboard hanya memaparkan data **individu** berdasarkan akaun peserta yang login.  
Panel Admin mempunyai akses penuh untuk pengurusan data.
""")

st.divider()

# === Kad Info Program ===
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

with st.expander("🧑‍💻 Siapa boleh akses sistem ini?"):
    st.markdown("✅ Peserta WLC 2025 dan Penganjur.")

with st.expander("🔑 Bagaimana untuk login?"):
    st.markdown("✅ Peserta boleh akses dashboard menggunakan No. Staf atau email (akan datang). Admin perlu login di Panel Admin.")

with st.expander("🔐 Adakah data saya selamat?"):
    st.markdown("✅ Sistem ini menggunakan Google Sheet sebagai backend yang selamat dengan akses terkawal.")

with st.expander("🎯 Bagaimana nak sertai program ini?"):
    st.markdown("✅ Penyertaan telah ditutup untuk sesi 2025.")

st.divider()

# === Notis / Pengumuman ===
st.info("""
📢 **Pengumuman Penting:**  
- Timbang seterusnya pada **20 Julai 2025**.  
- Pastikan anda login untuk kemas kini berat terkini selepas penimbangan.
""")

st.divider()

# === Footer ===
local_tz = pytz.timezone("Asia/Kuala_Lumpur")
footer_date = datetime.now(local_tz).strftime("%d/%m/%Y")
papar_footer("MKR", footer_date)
