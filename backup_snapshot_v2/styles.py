import streamlit as st


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
