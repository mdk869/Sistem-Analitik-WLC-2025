# app/styles.py
from datetime import datetime
import pytz
import streamlit as st

def paparkan_tema():
    st.markdown("""
    <style>
    .wlc-title {
        font-size: 30px;
        font-weight: 700;
        color: #00264d;
        text-align: center;
        margin-top: 2rem;
        margin-bottom: 0.5rem;
    }
    .wlc-sub-title {
        font-size: 0.95rem;
        color: #333;
        margin-bottom: 0.4rem;
    }
    .wlc-value {
        font-size: 1.9rem;
        font-weight: bold;
        color: #0074D9;
    }           
    .wlc-subtitle {
        font-size: 20px;
        font-weight: 400;
        color: #4d4d4d;
        text-align: center;
        margin-bottom: 2rem;
    }
    .wlc-box {
        background-color: #f9f9f9;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 2px 2px 6px rgba(0, 0, 0, 0.05);
        text-align: center;
        margin-bottom: 1 rem;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    .bmi-box {
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        color: white;
        font-family: sans-serif;
        box-shadow: 2px 2px 6px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    .bmi-title {
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 0.4rem;
    }
    .bmi-value {
        font-size: 1.6rem;
        font-weight: bold;
    }
.kurang { background-color: #2ecc71; }         /* Hijau */
.normal { background-color: #f1c40f; }         /* Kuning */
.lebih { background-color: #e67e22; }          /* Oren */
.obes1 { background-color: #e74c3c; }          /* Merah */
.obes2 { background-color: #8e44ad; }          /* Ungu */
.morbid { background-color: #2c3e50; }         /* Biru Gelap */
</style>
""", unsafe_allow_html=True)



def papar_tajuk_utama():
    st.title("Selamat Datang ke Sistem Analitik WLC 2025")

def papar_kandungan_home():
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
def papar_header(teks):
    st.markdown(f"<div class='wlc-header'>{teks}</div>", unsafe_allow_html=True)
    
def papar_footer(owner="MKR", date=None):
    st.markdown(f"""
    <hr>
    <div style="text-align:center; font-size: 14px; opacity: 0.7">
        Dibangunkan oleh <strong>{owner}</strong> | Kemas kini terakhir {date}
    </div>
    """, unsafe_allow_html=True)

