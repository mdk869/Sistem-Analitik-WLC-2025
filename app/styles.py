import streamlit as st

# ✅ Fungsi Apply CSS Global
def apply_css():
    st.markdown("""
    <style>
    /* ✅ Box BMI */
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

    /* ✅ Animation Fade In */
    @keyframes fadeIn {
        to { opacity: 1; }
    }

    /* ✅ Warna Kategori BMI */
    .kurang { background-color: #00BFFF; }    /* Biru Cerah */
    .normal { background-color: #32CD32; }    /* Hijau */
    .lebih  { background-color: #FFD700; }    /* Kuning Emas */
    .obes1  { background-color: #FF8C00; }    /* Oren Gelap */
    .obes2  { background-color: #FF4500; }    /* Merah Tua */
    .morbid { background-color: #8B0000; }    /* Merah Gelap */

    /* ✅ Customize Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 8px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #555;
    }

    /* ✅ Table Styling */
    table {
        border-collapse: collapse;
        width: 100%;
    }
    th, td {
        padding: 6px;
    }
    </style>
    """, unsafe_allow_html=True)


# ✅ Warna kategori BMI untuk digunakan pada plotly dan lain-lain
warna_mapping = {
    "Kurang Berat Badan": "#00BFFF",
    "Normal": "#32CD32",
    "Lebih Berat Badan": "#FFD700",
    "Obesiti Tahap 1": "#FF8C00",
    "Obesiti Tahap 2": "#FF4500",
    "Obesiti Morbid": "#8B0000"
}


# ✅ Tema Global
def paparkan_tema():
    st.set_page_config(
        page_title="Sistem Analitik WLC 2025",
        page_icon="📊",
        layout="wide"
    )


# ✅ Header Page
def papar_header(title):
    st.markdown(f"## {title}")


# ✅ Footer Page
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

# ✅ Tooltip
def css_tooltip():
    st.markdown("""
    <style>
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: pointer;
    }

    .tooltip .tooltiptext {
        visibility: hidden;
        width: 320px;
        background-color: #333;
        color: #fff;
        text-align: left;
        border-radius: 6px;
        padding: 8px;
        position: absolute;
        z-index: 999;
        top: 0;
        left: 105%;
        white-space: normal;
        word-wrap: break-word;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.5);
        border: 1px solid #999;
    }

    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }

    .tooltip .tooltiptext::after {
        content: "";
        position: absolute;
        top: 10px;
        right: 100%;
        margin-top: -5px;
        border-width: 6px;
        border-style: solid;
        border-color: transparent #333 transparent transparent;
    }
    </style>
    """, unsafe_allow_html=True)

# ✅ Tooltip Component
def tooltip(tajuk, keterangan, size="h4"):
    st.markdown(f"""
    <div style='display:flex; align-items:center; gap:6px;'>
        <{size} style='margin:0;'>{tajuk}</{size}>
        <div class="tooltip">🛈
          <span class="tooltiptext">
            {keterangan}
          </span>
        </div>
    </div>
    """, unsafe_allow_html=True)