# pages/admin.py

import streamlit as st
import pandas as pd
from datetime import date

from app.helper_auth import check_login
from app.helper_logic import kira_bmi, kategori_bmi_asia
from app.helper_log import log_dev
from app.helper_utils import check_header_consistency
from app.styles import paparkan_tema, papar_header, papar_footer
from app.helper_data import (
    load_data_peserta,
    tambah_peserta_google_sheet,
    simpan_rekod_berat,
    update_berat_terkini_peserta,
    padam_peserta_dari_sheet
)

# =============================================================
# ✅ Semakan Login
# =============================================================
is_admin = check_login()

if not is_admin:
    st.error("❌ Akses ditolak! Halaman ini hanya untuk Admin.")
    st.stop()


# =============================================================
# ✅ Layout
# =============================================================
paparkan_tema()
papar_header("Admin Panel | WLC 2025")

st.title("👑 Halaman Admin")
st.markdown("Selamat datang ke Panel Admin. Anda mempunyai akses penuh ke fungsi berikut:")

# =============================================================
# ✅ Load Data
# =============================================================
data_peserta = load_data_peserta()
data_rekod = load_data_peserta()

HEADER_PESERTA = [
    'Nama', 'NoStaf', 'Umur', 'Jantina', 'Jabatan',
    'Tinggi', 'BeratAwal', 'TarikhDaftar',
    'BeratTerkini', 'TarikhTimbang', 'BMI', 'Kategori'
]

# =============================================================
# ✅ Papar Senarai Peserta
# =============================================================
st.subheader("📋 Senarai Peserta")

if check_header_consistency(data_peserta, HEADER_PESERTA, "Data Peserta"):
    kolum_pilihan = ['Nama', 'NoStaf', 'Umur', 'Jantina', 'Tinggi', 'BeratAwal', 'TarikhDaftar']

    st.dataframe(
        data_peserta[kolum_pilihan].set_index(
            pd.Index(range(1, len(data_peserta) + 1), name="No.")
        ),
        use_container_width=True
    )

st.divider()

# =============================================================
# ✅ Tambah Peserta
# =============================================================
with st.expander("➕ Tambah Peserta Baru"):

    with st.form("form_tambah_peserta", clear_on_submit=True):
        st.subheader("🆕 Tambah Peserta")

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
                log_dev("Admin", f"Tambah peserta {nama}", "Success")
                st.success(f"✅ Peserta '{nama}' berjaya ditambah.")
                st.rerun()
            else:
                st.warning("⚠️ Sila isi semua maklumat peserta.")

# =============================================================
# ✅ Kemaskini Berat Terkini
# =============================================================
with st.expander("⚖️ Kemaskini Berat Terkini"):

    nama_list = data_peserta["Nama"].dropna().tolist()

    with st.form("kemaskini_berat"):
        nama = st.selectbox("Nama Peserta", nama_list)
        tarikh = st.date_input("Tarikh Timbang", value=pd.Timestamp.today())
        berat = st.number_input("Berat (kg)", min_value=0.0, step=0.1)

        submitted = st.form_submit_button("✅ Simpan Rekod")

        if submitted:
            tarikh_str = tarikh.strftime("%Y-%m-%d")

            result = simpan_rekod_berat(nama, tarikh_str, berat)

            if result['rekod_berat'] and result['update_peserta']:
                st.success(f"✅ Berat {berat} kg pada {tarikh_str} untuk {nama} telah dikemaskini sepenuhnya.")
            elif result['rekod_berat']:
                st.warning(f"⚠️ Rekod berat disimpan ke {tarikh_str}, tetapi gagal update di sheet data_peserta.")
            else:
                st.error("❌ Gagal simpan rekod timbang.")

# =============================================================
# ✅ Padam Peserta
# =============================================================
with st.expander("🗑️ Padam Peserta"):

    if len(data_peserta) > 0:
        nama_list = data_peserta["Nama"].tolist()
        nama_dipilih = st.selectbox("Pilih Nama untuk Dipadam", nama_list, key="padam")

        confirm = st.checkbox("⚠️ Saya ingin padam peserta ini.")

        if st.button("🗑️ Padam Peserta"):
            if confirm:
                berjaya = padam_peserta_dari_sheet(nama_dipilih)
                if berjaya:
                    log_dev("Admin", f"Padam peserta {nama_dipilih}", "Success")
                    st.success(f"✅ {nama_dipilih} telah dipadam dari Google Sheet.")
                    st.rerun()
                else:
                    st.warning("⚠️ Nama tidak dijumpai atau berlaku ralat.")
            else:
                st.info("👉 Tandakan kotak pengesahan sebelum padam.")
    else:
        st.info("🚫 Tiada peserta untuk dipadam.")

st.divider()

# =============================================================
# ✅ Papar Sejarah Rekod Berat
# =============================================================
st.subheader("🗂️ Sejarah Rekod Berat")

if check_header_consistency(data_rekod, HEADER_PESERTA, "Rekod Ranking"):
    kolum_pilihan = ['Nama', 'BeratAwal', 'BeratTerkini', 'TarikhTimbang', 'BMI', 'Kategori']

    st.dataframe(
        data_rekod[kolum_pilihan].set_index(
            pd.Index(range(1, len(data_rekod) + 1), name="No.")
        ),
        use_container_width=True
    )

# =============================================================
# ✅ Footer
# =============================================================
papar_footer(
    owner="MKR Dev Team",
    version="v3.2.5",
    last_update="2025-06-27",
    tagline="Empowering Data-Driven Decisions."
)
