# pages/admin.py

import streamlit as st
from app.styles import papar_header, papar_footer
from components.widgets_admin import (
    borang_tambah_peserta,
    borang_edit_peserta,
    borang_padam_peserta,
    papar_senarai_peserta,
    paparan_statistik_mini
)

# ========== Header Halaman ==========
papar_header("🛠️ Panel Admin - WLC 2025")

# ========== Tab Navigasi ==========
tab1, tab2, tab3, tab4 = st.tabs([
    "➕ Tambah Peserta", 
    "✏️ Kemaskini Peserta", 
    "🗑️ Padam Peserta", 
    "👥 Senarai Peserta"
])

with tab1:
    borang_tambah_peserta()

with tab2:
    borang_edit_peserta()

with tab3:
    borang_padam_peserta()

with tab4:
    papar_senarai_peserta()

# ========== Statistik Ringkas ==========
st.divider()
paparan_statistik_mini()

# ========== Footer ==========
papar_footer()
