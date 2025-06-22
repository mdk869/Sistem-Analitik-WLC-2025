# Home.py
import streamlit as st
from datetime import datetime
import pytz

st.set_page_config(page_title="WLC 2025", layout="wide")
st.title("🏠 Selamat Datang ke Sistem Analitik WLC 2025")

# --- Info Ringkas ---
st.markdown("""
Sistem ini dibangunkan untuk membantu pihak penganjur **Weight Loss Challenge (WLC) Wilayah Kuala Selangor 2025**

### Fungsi Utama:
- 📊 **Dashboard**: Analisis penurunan berat, BMI, carta dan statistik peserta.
- 🔐 **Admin Panel**: Simpan ranking, urus data, dan akses sejarah peserta.

➡️ Sila pilih modul pada menu sebelah kiri untuk teruskan.
""")

# --- Nota Kemaskini ---
st.info("🚀 Sistem sedang aktif dan tersedia sepenuhnya di platform Streamlit Cloud.")

# --- Footer ---
footer_date = datetime.now(pytz.timezone("Asia/Kuala_Lumpur")).strftime("%d/%m/%Y")
st.markdown(f"""
---
<div style='font-size:14px;'>
    Dibangunkan oleh <strong>MKR</strong> | Kemaskini terakhir: {footer_date}
</div>
""", unsafe_allow_html=True)
