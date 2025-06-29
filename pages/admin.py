import streamlit as st
import pandas as pd
from datetime import date
from io import BytesIO

# ✅ Import Helper
from app.helper_auth import check_login
from app.helper_log import log_dev
from app.helper_utils import check_header_consistency
from app.helper_logic import kira_bmi, kategori_bmi_asia
from app.helper_data import (
    load_data_peserta, load_rekod_berat_semua,
    tambah_peserta_google_sheet,
    padam_peserta_dari_sheet, simpan_rekod_berat
)
from app.helper_drive import upload_to_drive, download_from_drive, list_files_in_folder
from app.styles import paparkan_tema, papar_header, papar_footer


# ===========================================
# ✅ Check Login
# ===========================================
if not check_login():
    st.error("❌ Akses ditolak! Halaman ini hanya untuk Admin.")
    st.stop()


# ===========================================
# ✅ Layout
# ===========================================
paparkan_tema()
papar_header("Admin Panel | WLC 2025")
st.title("👑 Panel Admin")
st.markdown("Akses penuh kepada pengurusan data peserta dan sistem.")

# ===========================================
# ✅ Load Data
# ===========================================
data_peserta = load_data_peserta()
data_rekod = load_rekod_berat_semua()

HEADER_PESERTA = [
    'Nama', 'NoStaf', 'Umur', 'Jantina', 'Jabatan',
    'Tinggi', 'BeratAwal', 'TarikhDaftar',
    'BeratTerkini', 'TarikhTimbang', 'BMI', 'Kategori'
]


# ===========================================
# ✅ Tab Layout
# ===========================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "👥 Peserta", "➕ Tambah", "⚖️ Rekod Timbang",
    "🛠️ Edit Data", "📦 Backup/Restore"
])


# ===========================================
# ✅ Tab 1: Senarai Peserta
# ===========================================
with tab1:
    st.subheader("📋 Senarai Peserta")
    if check_header_consistency(data_peserta, HEADER_PESERTA, "Data Peserta"):
        st.dataframe(
            data_peserta.set_index(pd.Index(range(1, len(data_peserta) + 1), name="No.")),
            use_container_width=True
        )
    log_dev("Admin", "Buka Tab Senarai Peserta", "Success")


# ===========================================
# ✅ Tab 2: Tambah Peserta
# ===========================================
with tab2:
    st.subheader("➕ Tambah Peserta")

    with st.form("form_tambah_peserta", clear_on_submit=True):
        nama = st.text_input("Nama")
        nostaf = st.text_input("No Staf")
        umur = st.number_input("Umur", 10, 100)
        jantina = st.selectbox("Jantina", ["Lelaki", "Perempuan"])
        jabatan = st.text_input("Jabatan")
        tinggi = st.number_input("Tinggi (cm)", 100, 250)
        berat_awal = st.number_input("Berat Awal (kg)", 30.0, 300.0)
        tarikh_daftar = st.date_input("Tarikh Daftar", value=date.today())

        bmi = kira_bmi(berat_awal, tinggi)
        kategori = kategori_bmi_asia(bmi)
        st.info(f"BMI: {bmi} ({kategori})")

        if st.form_submit_button("➕ Tambah Peserta"):
            if nama and nostaf and jabatan:
                tambah_peserta_google_sheet(
                    nama, nostaf, umur, jantina, jabatan, tinggi, berat_awal, tarikh_daftar
                )
                st.success(f"✅ Peserta {nama} berjaya ditambah.")
                st.rerun()
            else:
                st.warning("⚠️ Sila isi semua maklumat yang wajib.")


# ===========================================
# ✅ Tab 3: Rekod Timbang
# ===========================================
with tab3:
    st.subheader("⚖️ Rekod Timbang Peserta")

    nama_list = data_peserta["Nama"].dropna().tolist()
    nama_input = st.text_input("Cari Nama (Auto Lengkap atau Dropdown)")
    nama_pilih = st.selectbox("Atau Pilih Nama", nama_list)

    nama_final = nama_input if nama_input else nama_pilih

    with st.form("form_rekod_timbang", clear_on_submit=True):
        tarikh = st.date_input("Tarikh Timbang", date.today())
        berat = st.number_input("Berat (kg)", min_value=30.0, max_value=300.0, step=0.1)

        if st.form_submit_button("✅ Simpan Rekod"):
            if nama_final:
                tarikh_str = tarikh.strftime("%Y-%m-%d")
                result = simpan_rekod_berat(nama_final, tarikh_str, berat)

                if result['rekod_berat'] and result['update_peserta']:
                    st.success(f"✅ Berat {berat} kg pada {tarikh_str} untuk {nama_final} telah dikemaskini.")
                elif result['rekod_berat']:
                    st.warning(f"⚠️ Rekod berat disimpan tetapi gagal update berat terkini.")
                else:
                    st.error("❌ Gagal simpan rekod timbang.")

                st.rerun()
            else:
                st.warning("⚠️ Sila masukkan nama peserta.")


# ===========================================
# ✅ Tab 4: Edit Data Peserta
# ===========================================
with tab4:
    st.subheader("🛠️ Kemaskini Data Peserta")

    nama_list = data_peserta["Nama"].dropna().tolist()
    nama_input = st.text_input("Cari Nama (Input Manual)")
    nama_pilih = st.selectbox("Atau Pilih Nama", nama_list)

    nama_final = nama_input if nama_input else nama_pilih

    if nama_final:
        data_row = data_peserta[data_peserta["Nama"] == nama_final]

        if not data_row.empty:
            row = data_row.iloc[0]

            with st.form("form_edit_peserta", clear_on_submit=True):
                nostaf = st.text_input("No Staf", row["NoStaf"])
                umur = st.number_input("Umur", 10, 100, int(row["Umur"]))
                jantina = st.selectbox("Jantina", ["Lelaki", "Perempuan"], index=["Lelaki", "Perempuan"].index(row["Jantina"]))
                jabatan = st.text_input("Jabatan", row["Jabatan"])
                tinggi = st.number_input("Tinggi (cm)", 100, 250, int(row["Tinggi"]))
                berat_terkini = st.number_input("Berat Terkini (kg)", 30.0, 300.0, float(row["BeratTerkini"]))
                tarikh_timbang = st.date_input("Tarikh Timbang", pd.to_datetime(row["TarikhTimbang"]))

                bmi = kira_bmi(berat_terkini, tinggi)
                kategori = kategori_bmi_asia(bmi)
                st.info(f"BMI: {bmi} ({kategori})")

                if st.form_submit_button("💾 Simpan Perubahan"):
                    tambah_peserta_google_sheet(
                        nama_final, nostaf, umur, jantina, jabatan,
                        tinggi, berat_terkini, tarikh_timbang, bmi, kategori
                    )
                    st.success(f"✅ Data peserta {nama_final} telah dikemaskini.")
                    st.rerun()


# ===========================================
# ✅ Tab 5: Backup & Restore
# ===========================================
with tab5:
    st.subheader("📦 Backup & Restore Data")

    with st.expander("⬇️ Backup Data Manual"):
        st.markdown("**Pilih jenis data untuk backup:**")
        pilihan = st.selectbox("Data", ["Data Peserta", "Rekod Timbang"])

        if st.button("⬇️ Download Backup"):
            if pilihan == "Data Peserta":
                df = data_peserta
                filename = "data_peserta_backup.xlsx"
            else:
                df = data_rekod
                filename = "rekod_timbang_backup.xlsx"

            towrite = BytesIO()
            df.to_excel(towrite, index=False)
            towrite.seek(0)
            st.download_button(
                label="📥 Download File",
                data=towrite,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    with st.expander("⬆️ Upload/Restore Data dari Drive"):
        st.info("🚀 Fungsi ini dalam pembangunan versi penuh.")

    with st.expander("🗑️ Padam Peserta"):
        nama_list = data_peserta["Nama"].tolist()
        nama_padam = st.selectbox("Pilih Nama untuk Dipadam", nama_list)

        confirm = st.checkbox("⚠️ Saya ingin padam peserta ini.")

        if st.button("🗑️ Padam Peserta"):
            if confirm:
                berjaya = padam_peserta_dari_sheet(nama_padam)
                if berjaya:
                    st.success(f"✅ {nama_padam} telah dipadam.")
                    st.rerun()
                else:
                    st.warning("⚠️ Gagal padam peserta.")
            else:
                st.info("👉 Tandakan kotak pengesahan sebelum padam.")

# ===========================================
# ✅ Footer
# ===========================================
papar_footer(
    owner="MKR Dev Team",
    version="v3.5.0",
    last_update="2025-06-29",
    tagline="Empowering Data-Driven Decisions."
)
