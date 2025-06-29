import streamlit as st
import pandas as pd
from datetime import date

# ✅ Import Helper
from app.helper_auth import check_login
from app.helper_logic import kira_bmi, kategori_bmi_asia
from app.helper_utils import carian_nama_suggestion, check_header_consistency
from app.helper_drive import upload_to_drive
from app.helper_data import (
    load_data_peserta,
    load_rekod_berat_semua,
    simpan_rekod_berat,
    padam_peserta_dari_sheet,
    update_data_peserta,
    daftar_peserta
)
from app.styles import paparkan_tema, papar_header, papar_footer


# =========================================
# ✅ Semakan Login
# =========================================
if not check_login():
    st.error("❌ Akses ditolak! Halaman ini hanya untuk Admin.")
    st.stop()

# =========================================
# ✅ Layout
# =========================================
paparkan_tema()
papar_header("Admin Panel | WLC 2025")

st.title("👑 Halaman Admin")
st.markdown("Panel kawalan penuh untuk pengurusan data peserta dan rekod timbang WLC 2025.")

# =========================================
# ✅ Load Data
# =========================================
data_peserta = load_data_peserta()
data_rekod = load_rekod_berat_semua()

HEADER_PESERTA = [
    'Nama', 'NoStaf', 'Umur', 'Jantina', 'Jabatan',
    'Tinggi', 'BeratAwal', 'TarikhDaftar',
    'BeratTerkini', 'TarikhTimbang', 'BMI', 'Kategori'
]

# =========================================
# ✅ Tabs Layout
# =========================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 Senarai Peserta", 
    "➕ Tambah Peserta", 
    "⚖️ Rekod Timbang", 
    "🛠️ Kemaskini Data", 
    "🗄️ Backup & Restore"
])

# =========================================
# ✅ Tab 1: Senarai Peserta
# =========================================
with tab1:
    st.subheader("📋 Senarai Peserta")

    if check_header_consistency(data_peserta, HEADER_PESERTA, "Data Peserta"):
        st.dataframe(
            data_peserta.set_index(
                pd.Index(range(1, len(data_peserta) + 1), name="No.")
            ),
            use_container_width=True
        )

# =========================================
# ✅ Tab 2: Tambah Peserta
# =========================================
with tab2:
    st.subheader("➕ Tambah Peserta Baru")

    with st.form("form_tambah", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nama = st.text_input("Nama")
            nostaf = st.text_input("No Staf")
            umur = st.number_input("Umur", 10, 100)
            jantina = st.selectbox("Jantina", ["Lelaki", "Perempuan"])
        with col2:
            jabatan = st.text_input("Jabatan")
            tinggi = st.number_input("Tinggi (cm)", 100, 250)
            berat_awal = st.number_input("Berat Awal (kg)", 30.0, 300.0)
            tarikh = st.date_input("Tarikh Daftar", value=date.today())

        bmi = kira_bmi(berat_awal, tinggi)
        kategori = kategori_bmi_asia(bmi)

        st.info(f"BMI: {bmi} ({kategori})")

        submit = st.form_submit_button("✅ Tambah")

        if submit:
            daftar_peserta(
                nama, nostaf, umur, jantina, jabatan,
                tinggi, berat_awal, tarikh
            )
            st.success(f"✅ Peserta '{nama}' berjaya ditambah.")
            st.rerun()

# =========================================
# ✅ Tab 3: Rekod Timbang
# =========================================
with tab3:
    st.subheader("⚖️ Rekod Timbangan Berat")

    nama_timbang = carian_nama_suggestion(data_peserta, label="Nama untuk Timbang", key="timbang")

    if nama_timbang:
        row = data_peserta[data_peserta["Nama"].str.lower() == nama_timbang.lower()]
        if row.empty:
            st.warning("❌ Nama tidak ditemui dalam senarai peserta.")
            st.stop()

        nostaf = row.iloc[0]["NoStaf"]

        with st.form("form_timbang", clear_on_submit=True):
            tarikh = st.date_input("Tarikh Timbang", value=date.today())
            berat = st.number_input("Berat (kg)", min_value=30.0, max_value=300.0)

            submit = st.form_submit_button("✅ Simpan Rekod")

            if submit:
                data = {
                    "Nama": nama_timbang,
                    "NoStaf": nostaf,
                    "Tarikh": tarikh.strftime("%Y-%m-%d"),
                    "Berat": berat,
                    "SesiBulan": tarikh.strftime("%Y-%m")
                }

                status = simpan_rekod_berat(data)

                # Kemas kini berat terkini peserta
                update_data_peserta(
                    nostaf,
                    {
                        "BeratTerkini": berat,
                        "TarikhTimbang": tarikh.strftime("%Y-%m-%d"),
                        "BMI": kira_bmi(berat, row.iloc[0]["Tinggi"]),
                        "Kategori": kategori_bmi_asia(kira_bmi(berat, row.iloc[0]["Tinggi"]))
                    }
                )

                if status:
                    st.success(f"✅ Rekod berat untuk {nama_timbang} berjaya disimpan.")
                else:
                    st.warning("⚠️ Terdapat isu semasa simpan rekod.")
                st.rerun()

# =========================================
# ✅ Tab 4: Kemaskini Data Peserta
# =========================================
with tab4:
    st.subheader("🛠️ Kemaskini Data Peserta")

    nama_edit = carian_nama_suggestion(data_peserta, label="Nama Peserta", key="edit")

    if nama_edit:
        df_row = data_peserta[data_peserta["Nama"].str.lower() == nama_edit.lower()]

        if not df_row.empty:
            row = df_row.iloc[0]
            with st.form("form_edit", clear_on_submit=True):
                col1, col2 = st.columns(2)

                with col1:
                    nostaf = st.text_input("No Staf", row["NoStaf"])
                    umur = st.number_input("Umur", 10, 100, int(row["Umur"]))
                    jantina = st.selectbox(
                        "Jantina", ["Lelaki", "Perempuan"],
                        index=0 if row["Jantina"].lower() == "lelaki" else 1
                    )
                    jabatan = st.text_input("Jabatan", row["Jabatan"])

                with col2:
                    tinggi = st.number_input("Tinggi (cm)", 100, 250, int(row["Tinggi"]))
                    berat_terkini = st.number_input(
                        "Berat Terkini (kg)", 30.0, 300.0, float(row["BeratTerkini"])
                    )
                    tarikh_timbang = st.date_input(
                        "Tarikh Timbang", pd.to_datetime(row["TarikhTimbang"])
                    )

                # ✅ Auto BMI & Kategori
                bmi = kira_bmi(berat_terkini, tinggi)
                kategori = kategori_bmi_asia(bmi)

                st.info(f"BMI: {bmi} ({kategori})")

                submit = st.form_submit_button("✅ Kemaskini")

                if submit:
                    update_data_peserta(
                        nostaf,
                        {
                            "Nama": nama,
                            "Umur": umur,
                            "Jantina": jantina,
                            "Jabatan": jabatan,
                            "Tinggi": tinggi,
                            "BeratTerkini": berat_terkini,
                            "TarikhTimbang": str(tarikh_timbang),
                            "BMI": bmi,
                            "Kategori": kategori
                        }
                    )


# =========================================
# ✅ Tab 5: Backup & Restore
# =========================================
with tab5:
    st.subheader("🗄️ Backup & Restore Data")

    with st.expander("📥 Backup Data"):
        st.info("Backup semua data ke Google Drive.")
        if st.button("🔽 Backup Data"):
            file_name = f"backup_data_peserta_{date.today()}.xlsx"
            data_peserta.to_excel(file_name, index=False)
            upload_to_drive(file_name, file_name)
            st.success(f"✅ Data berjaya dibackup ke Google Drive sebagai '{file_name}'.")

    with st.expander("📤 Export Data Manual"):
        pilihan = st.selectbox("Pilih Data untuk Export", ["Data Peserta", "Rekod Timbang"])
        if st.button("🔽 Export"):
            if pilihan == "Data Peserta":
                df = data_peserta
            else:
                df = data_rekod
            file_name = f"{pilihan.lower().replace(' ','_')}_{date.today()}.xlsx"
            df.to_excel(file_name, index=False)
            st.download_button("💾 Download", data=open(file_name, "rb"), file_name=file_name)

    with st.expander("♻️ Restore Data"):
        st.warning("⚠️ Fungsi Restore manual. Upload akan overwrite data sedia ada.")
        file_upload = st.file_uploader("Upload Fail XLSX untuk Restore", type=["xlsx"])
        if file_upload:
            df_restore = pd.read_excel(file_upload)
            st.dataframe(df_restore)
            st.success("✅ Data berjaya dimuat naik. Sila implement restore ke Google Sheets secara manual.")

# =========================================
# ✅ Footer
# =========================================
papar_footer(
    owner="MKR Dev Team",
    version="v4.1.0",
    last_update="2025-06-29",
    tagline="Empowering Data-Driven Decisions."
)
