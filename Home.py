# Home.py
import streamlit as st

# === Setup Paparan ===
st.set_page_config(
    page_title="Sistem Analitik WLC 2025",
    page_icon="📊",
    layout="wide"
)

# === Gaya Tema (Elegan, Profesional) ===
st.markdown("""
<style>
.wlc-title {
    font-size: 40px;
    font-weight: 700;
    color: #00264d;
    text-align: center;
    margin-top: 2rem;
    margin-bottom: 0.5rem;
}
.wlc-subtitle {
    font-size: 20px;
    font-weight: 400;
    color: #4d4d4d;
    text-align: center;
    margin-bottom: 2rem;
}
.wlc-box {
    background-color: #f5f8ff;
    border: 1px solid #cce0ff;
    border-radius: 15px;
    padding: 2rem;
    box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
    text-align: center;
    max-width: 700px;
    margin: 0 auto;
}
</style>
""", unsafe_allow_html=True)

# === Kandungan Utama ===
st.markdown("""
<div class='wlc-title'>📊 Sistem Analitik WLC 2025</div>
<div class='wlc-subtitle'>Satu platform pemantauan dan analitik untuk penganjur program Weight Loss Challenge (WLC)</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='wlc-box'>
    <p>Selamat datang ke sistem rasmi WLC 2025. Sistem ini direka khas untuk membantu pihak penganjur:</p>
    <ul style='text-align:left;'>
        <li>Merekod dan menyemak kemajuan peserta</li>
        <li>Menjana ranking dan statistik semasa</li>
        <li>Backup dan eksport data</li>
    </ul>
    <br>
    <p><strong>Sila gunakan menu di sebelah kiri</strong> untuk akses fungsi utama seperti:</p>
    <ul style='text-align:left;'>
        <li><strong>Admin Panel</strong> – Urus data peserta dan lihat ranking</li>
        <li><strong>Dashboard</strong> – Visualisasi & Analitik penuh</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# === Footer ===
st.markdown("""
---
<div style='text-align:center; font-size:13px; color:gray;'>
Dibangunkan oleh <strong>MKR</strong> · Weight Loss Challenge Wilayah Kuala Selangor 2025
</div>
""", unsafe_allow_html=True)
