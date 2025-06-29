import streamlit as st
import pandas as pd
from datetime import date

# === Import helper ===
from app.styles import paparkan_tema, papar_header, papar_footer
from app.helper_auth import check_login
from app.helper_log import log_dev
from app.helper_utils import check_header_consistency
from app.helper_logic import kira_bmi, kategori_bmi_asia
from app.helper_data import (
    load_data_peserta,
    tambah_peserta_google_sheet,
    simpan_rekod_berat,
    update_berat_terkini_peserta,
    padam_peserta_dari_sheet,
    backup_data_peserta_to_drive,
    restore_data_peserta_from_drive
)

# === Layout ===
paparkan_tema()
papar_header("Admin Panel | WLC 2025")

st.title("👑 Panel Admin")
st.markdown("Panel pengurusan penuh data peserta WLC 2025.")

# === Auth ===
if not check_login():
    st.error("❌ Akses ditolak! Halaman ini hanya untuk Admin.")
    st.stop()

# === Load Data ===
data_peserta = load_data_peserta()

HEADER_PESERTA = [
    'Nama', 'NoStaf', 'Umur', 'Jantina', 'Jabatan',
    'Tinggi', 'BeratAwal', 'TarikhDaftar',
    'BeratTerkini', 'TarikhTimbang', 'BMI', 'Kategori'
]

# === Tab Layout ===
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "👥 Peserta", "⚖️ Rekod Timbang", "✏️ Kemaskini Data", "💾 Backup/Restore", "🗑️ Padam"
])

# ===================================================================================
# ✅ Tab 1: Senarai Peserta
# ===================================================================================
with tab1:
    st.subheader("📋 Senarai Peserta")

    if check_header_consistency(data_peserta, HEADER_PESERTA, "Data Peserta"):
        st.dataframe(
            data_peserta[[
                'Nama', 'NoStaf', 'Jabatan', 'Umur', 'Jantina',
                'Tinggi', 'BeratAwal', 'BeratTerkini', 'BMI', 'Kategori'
            ]].set_index(pd.Index(range(1, len(data_peserta) + 1), name="No.")),
            use_container_width=True
        )

# ===================================================================================
# ✅ Tab 2: Rekod Timbang
# ===================================================================================
with tab2:
    st.subheader("⚖️ Kemaskini Rekod Timbang")

    nama_list = data_peserta["Nama"].dropna().tolist()

    with st.form("form_timbang"):
        nama = st.selectbox("Nama Peserta", nama_list)
        tarikh = st.date_input("Tarikh Timbang", value=pd.Timestamp.today())
        berat = st.number_input("Berat (kg)", min_value=0.0, step=0.1)

        submit = st.form_submit_button("✅ Simpan Rekod")

        if submit:
            tarikh_str = tarikh.strftime("%Y-%m-%d")
            result = simpan_rekod_berat(nama, tarikh_str, berat)

            if result['rekod_berat'] and result['update_peserta']:
                st.success(f"✅ Berat {berat} kg pada {tarikh_str} untuk {nama} telah dikemaskini.")
            else:
                st.error("❌ Gagal simpan rekod timbang.")

# ===================================================================================
# ✅ Tab 3: Tambah/Kemaskini Peserta
# ===================================================================================
with tab3:
    st.subheader("✏️ Tambah Peserta")

    with st.form("form_tambah"):
        nama = st.text_input("Nama")
        nostaf = st.text_input("No Staf")
        umur = st.number_input("Umur", min_value=10, max_value=100)
        jantina = st.selectbox("Jantina", ["Lelaki", "Perempuan"])
        jabatan = st.text_input("Jabatan")
        tinggi = st.number_input("Tinggi (cm)", min_value=100, max_value=250)
        berat_awal = st.number_input("Berat Awal (kg)", min_value=30.0, max_value=300.0)
        tarikh_daftar = st.date_input("Tarikh Daftar", value=date.today())

        berat_terkini = berat_awal
        bmi = kira_bmi(berat_awal, tinggi)
        kategori = kategori_bmi_asia(bmi)

        st.info(f"BMI: {bmi} ({kategori})")

        submit = st.form_submit_button("➕ Tambah Peserta")

        if submit:
            if nama and nostaf and jabatan:
                tambah_peserta_google_sheet(
                    nama, nostaf, umur, jantina, jabatan,
                    tinggi, berat_awal, tarikh_daftar
                )
                st.success(f"✅ Peserta '{nama}' berjaya ditambah.")
                st.rerun()
            else:
                st.warning("⚠️ Sila isi semua maklumat peserta.")

# ===================================================================================
# ✅ Tab 4: Backup & Restore
# ===================================================================================
with tab4:
    st.subheader("💾 Backup & Restore Data")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⏫ Backup Data ke Drive"):
            file_id = backup_data_peserta_to_drive()
            if file_id:
                st.success(f"✅ Backup berjaya. File ID: {file_id}")
            else:
                st.error("❌ Gagal backup ke Drive.")

    with col2:
        if st.button("⏬ Restore Data dari Drive"):
            berjaya = restore_data_peserta_from_drive()
            if berjaya:
                st.success("✅ Restore berjaya.")
                st.rerun()
            else:
                st.error("❌ Gagal restore data.")

# ===================================================================================
# ✅ Tab 5: Padam Peserta
# ===================================================================================
with tab5:
    st.subheader("🗑️ Padam Peserta")

    if len(data_peserta) > 0:
        nama_list = data_peserta["Nama"].tolist()
        nama_dipilih = st.selectbox("Pilih Nama", nama_list, key="padam")

        confirm = st.checkbox("⚠️ Saya faham dan ingin padam peserta ini.")

        if st.button("🗑️ Padam"):
            if confirm:
                berjaya = padam_peserta_dari_sheet(nama_dipilih)
                if berjaya:
                    st.success(f"✅ {nama_dipilih} telah dipadam.")
                    st.rerun()
                else:
                    st.warning("⚠️ Nama tidak dijumpai atau berlaku ralat.")
            else:
                st.info("👉 Tandakan kotak pengesahan sebelum padam.")
    else:
        st.info("🚫 Tiada peserta untuk dipadam.")

# === Footer ===
papar_footer(
    owner="MKR Dev Team",
    version="v3.4.0",
    last_update="2025-06-29",
    tagline="Empowering Data-Driven Decisions."
)
