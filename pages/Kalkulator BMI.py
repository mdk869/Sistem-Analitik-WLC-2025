import streamlit as st
from app.styles import papar_footer
# ===========================
# ✅ Formula Kiraan BMI
# ===========================
def kira_bmi(berat, tinggi):
    try:
        tinggi_meter = tinggi / 100
        bmi = berat / (tinggi_meter ** 2)
        return round(bmi, 2)
    except:
        return 0

# ===========================
# ✅ Kategori BMI Asia
# ===========================
def kategori_bmi_asia(bmi):
    if bmi < 18.5:
        return "Kurang Berat Badan"
    elif 18.5 <= bmi <= 24.99:
        return "Normal"
    elif 25 <= bmi <= 29.9:
        return "Lebih Berat Badan"
    elif 30 <= bmi <= 34.9:
        return "Obesiti Tahap 1"
    elif 35 <= bmi <= 39.9:
        return "Obesiti Tahap 2"
    else:
        return "Obesiti Morbid"

# ===========================
# ✅ Interface Streamlit
# ===========================
st.set_page_config(page_title="Kalkulator BMI", page_icon="⚖️", layout="centered")
st.title("⚖️ Kalkulator BMI | WLC 2025")

st.markdown("Masukkan tinggi dan berat untuk kira BMI secara realtime.")

# ===========================
# ✅ Input User
# ===========================
tinggi = st.number_input("Tinggi (cm)", min_value=100.0, max_value=250.0, value=170.0, step=0.1)
berat = st.number_input("Berat (kg)", min_value=30.0, max_value=300.0, value=70.0, step=0.1)

# ===========================
# ✅ Output BMI
# ===========================
bmi = kira_bmi(berat, tinggi)
kategori = kategori_bmi_asia(bmi)

st.info(f"**BMI anda ialah:** `{bmi}`")
st.success(f"**Kategori BMI:** `{kategori}`")

# ===========================
# ✅ Info Panduan
# ===========================
with st.expander("ℹ️ Info Kategori BMI & Nasihat Kesihatan"):
    st.markdown("""
    ### 🔎 **Kategori BMI Asia (WHO & KKM)**

    - **< 18.5** : Kurang Berat Badan  
    - **18.5 – 24.9** : Normal  
    - **25 – 29.9** : Lebih Berat Badan  
    - **30 – 34.9** : Obesiti Tahap 1  
    - **35 – 39.9** : Obesiti Tahap 2  
    - **≥ 40** : Obesiti Morbid  

    ---

    ### 🏥 **Nasihat Kesihatan untuk BMI ≥ 25**

    - ✔️ Pemeriksaan kesihatan (BP, gula, kolesterol)
    - ✔️ Pemakanan sihat – kurangkan lemak, gula, garam
    - ✔️ Aktif fizikal: 150-300 minit/minggu
    - ✔️ Pengurusan stres dan tidur cukup
    - ✔️ BMI ≥ 30: rujuk doktor untuk intervensi perubatan
    - ✔️ BMI ≥ 35 atau ≥ 40: boleh rujuk pembedahan bariatrik

    ---

    ### ⚠️ **Risiko Kesihatan BMI Tinggi:**
    - Serangan jantung
    - Strok
    - Diabetes
    - Kegagalan buah pinggang
    - Kanser
    - Kematian pramatang
    """)

papar_footer()
