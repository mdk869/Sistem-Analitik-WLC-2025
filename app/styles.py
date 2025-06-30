import streamlit as st

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
.kurang { background-color: #00BFFF; }         /* Hijau */
.normal { background-color: #32CD32; }         /* Kuning */
.lebih { background-color: #FFD700; }          /* Oren */
.obes1 { background-color: #FF8C00; }          /* Merah */
.obes2 { background-color: #FF4500; }          /* Ungu */
.morbid { background-color: #8B0000; }         /* Biru Gelap */
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
