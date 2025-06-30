import streamlit as st

# ✅ CSS
st.markdown("""
    <style>
    .bmi-box {
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        color: white;
        font-family: 'Segoe UI', sans-serif;
        box-shadow: 2px 4px 10px rgba(0,0,0,0.1);
        margin-bottom: 0.5rem;
        opacity: 0;
        animation: fadeIn 0.8s ease forwards;
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .bmi-box:hover {
        transform: translateY(-5px);
        box-shadow: 4px 6px 12px rgba(0,0,0,0.2);
    }

    .bmi-title {
        font-size: 0.95rem;
        font-weight: 600;
        margin-bottom: 0.4rem;
    }

    .bmi-value {
        font-size: 2rem;
        font-weight: bold;
    }

    @keyframes fadeIn {
        to { opacity: 1; }
    }

    .kurang { background-color: #00BFFF; }    /* Biru Cerah */
    .normal { background-color: #32CD32; }    /* Hijau */
    .lebih  { background-color: #FFD700; }    /* Kuning Emas */
    .obes1  { background-color: #FF8C00; }    /* Oren Gelap */
    .obes2  { background-color: #FF4500; }    /* Merah Tua */
    .morbid { background-color: #8B0000; }    /* Merah Gelap */
    </style>
""", unsafe_allow_html=True)




# ✅ Warna kategori BMI
warna_mapping = {
    "Kurang Berat Badan": "#00BFFF",
    "Normal": "#32CD32",
    "Lebih Berat Badan": "#FFD700",
    "Obesiti Tahap 1": "#FF8C00",
    "Obesiti Tahap 2": "#FF4500",
    "Obesiti Morbid": "#8B0000"
}


# ✅ Tema
def paparkan_tema():
    st.set_page_config(
        page_title="Sistem Analitik WLC 2025",
        page_icon="📊",
        layout="wide"
    )


# ✅ Header
def papar_header(title):
    st.markdown(f"## {title}")


# ✅ Footer
def papar_footer(owner, version, last_update, tagline):
    st.markdown(f"""
    <hr>
    <center>
    <small>
    {tagline} <br>
    Versi {version} | Dikemaskini {last_update} <br>
    &copy; {owner}
    </small>
    </center>
    """, unsafe_allow_html=True)
