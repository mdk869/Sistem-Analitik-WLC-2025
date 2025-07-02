import streamlit as st
import pandas as pd
from datetime import date
from io import BytesIO

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
# ✅ Header
# =========================================
HEADER_PESERTA = [
    'Nama', 'NoStaf', 'Umur', 'Jantina', 'Jabatan',
    'Tinggi', 'BeratAwal', 'TarikhDaftar',
    'BeratTerkini', 'TarikhTimbang', 'BMI', 'Kategori'
]

# =========================================
# ✅ Fungsi Refresh Cache
# =========================================
def refresh_data():
    with st.spinner("🔄 Memuat semula data..."):
        st.session_state.data_peserta = load_data_peserta()
        st.session_state.data_rekod = load_rekod_berat_semua()
    st.success("✅ Data berjaya dikemaskini.")

# =========================================
# ✅ Load Data ke Cache jika belum ada
# =========================================
if "data_peserta" not in st.session_state:
    refresh_data()

data_peserta = st.session_state.data_peserta
data_rekod = st.session_state.data_rekod

# =========================================
# ✅ Butang Manual Refresh Page
# =========================================
with st.sidebar:
    st.info("ℹ️ Gunakan butang di bawah untuk refresh data daripada Google Sheets.")
    if st.button("🔄 Refresh Data"):
        refresh_data()
        st.rerun()

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
with st.expander("🩺 Semakan Kiraan BMI Peserta"):
    df_check = data_peserta.copy()

    # Kiraan semula BMI dan Kategori
    df_check["BMI Semakan"] = df_check.apply(
        lambda x: kira_bmi(x["BeratTerkini"], x["Tinggi"]), axis=1
    )
    df_check["Kategori Semakan"] = df_check["BMI Semakan"].apply(kategori_bmi_asia)

    # Cari perbezaan
    df_check["BMI Berbeza"] = df_check["BMI"] != df_check["BMI Semakan"]
    df_check["Kategori Berbeza"] = df_check["Kategori"] != df_check["Kategori Semakan"]

    # Paparkan peserta yang ada perbezaan
    df_salah = df_check[(df_check["BMI Berbeza"]) | (df_check["Kategori Berbeza"])]

    if not df_salah.empty:
        st.error(f"❌ {len(df_salah)} peserta ada isu kiraan BMI atau Kategori.")
        st.dataframe(df_salah[
            ["Nama", "BMI", "BMI Semakan", "Kategori", "Kategori Semakan"]
        ], use_container_width=True)
    else:
        st.success("✅ Semua peserta tiada isu kiraan BMI dan Kategori.")


if st.button("♻️ Auto Betulkan BMI & Kategori"):
    data_peserta["BMI"] = data_peserta.apply(
        lambda x: kira_bmi(x["BeratTerkini"], x["Tinggi"]), axis=1
    )
    data_peserta["Kategori"] = data_peserta["BMI"].apply(kategori_bmi_asia)

    st.success("✅ Semua BMI dan Kategori telah dikemaskini.")


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
            refresh_data()
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
                    "Berat": berat
                }

                simpan_rekod_berat(data)

                st.success(f"✅ Rekod berat untuk {nama_timbang} berjaya disimpan.")
                refresh_data()
                st.rerun()

# =========================================
# ✅ Tab 4: Kemaskini Data Peserta
# =========================================
with tab4:
    st.subheader("🛠️ Kemaskini & Padam Data Peserta")

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

                bmi = kira_bmi(berat_terkini, tinggi)
                kategori = kategori_bmi_asia(bmi)

                st.info(f"BMI: {bmi} ({kategori})")

                col_submit, col_delete = st.columns(2)

                with col_submit:
                    submit = st.form_submit_button("✅ Kemaskini")

                with col_delete:
                    padam = st.form_submit_button("🗑️ Padam Peserta")

                if submit:
                    update_data_peserta(
                        nostaf,
                        {
                            "Nama": nama_edit,
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
                    st.success(f"✅ Data peserta '{nama_edit}' berjaya dikemaskini.")
                    refresh_data()
                    st.rerun()

                if padam:
                    with st.expander("⚠️ Pengesahan Padam Peserta"):
                        st.warning("❌ Tindakan ini akan padam peserta secara kekal dari senarai.")
                        confirm = st.checkbox("✔️ Saya faham dan bersetuju untuk padam peserta ini.")

                        input_nama = st.text_input(
                            "Taip semula nama peserta untuk pengesahan:",
                            placeholder="Contoh: Ahmad Bin Ali"
                        )

                        if confirm and input_nama.lower().strip() == nama_edit.lower().strip():
                            padam_peserta_dari_sheet(nostaf)
                            st.success(f"✅ Peserta '{nama_edit}' berjaya dipadam.")
                            refresh_data()
                            st.rerun()
                        else:
                            st.info("ℹ️ Sahkan checkbox dan taip nama dengan betul untuk teruskan padam.")


# =========================================
# ✅ Tab 5: Backup & Restore
# =========================================
with tab5:
    st.subheader("🗄️ Backup & Restore Data")

    with st.expander("📥 Backup Data ke Google Drive"):
        st.info("Backup semua data ke Google Drive.")
        if st.button("🔽 Backup Data"):
            file_name = f"data_peserta_{date.today().strftime('%Y%m%d')}.xlsx"
            data_peserta.to_excel(file_name, index=False)
            upload_to_drive(file_name, file_name)
            st.success(f"✅ Data berjaya dibackup ke Google Drive sebagai '{file_name}'.")

    with st.expander("📤 Export Data Manual"):
        pilihan = st.selectbox("Pilih Data untuk Export", ["Data Peserta", "Rekod Timbang"])
        if st.button("🔽 Export"):
            df = data_peserta if pilihan == "Data Peserta" else data_rekod
            towrite = BytesIO()
            df.to_excel(towrite, index=False, engine='openpyxl')
            towrite.seek(0)
            st.download_button(
                label="💾 Download File",
                data=towrite,
                file_name=f"{pilihan.lower().replace(' ','_')}_{date.today().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    with st.expander("♻️ Restore Data (Manual)"):
        st.warning("⚠️ Fungsi Restore manual. Upload akan overwrite data sedia ada (belum auto sync ke Google Sheet).")
        file_upload = st.file_uploader("Upload Fail XLSX untuk Restore", type=["xlsx"])
        if file_upload:
            df_restore = pd.read_excel(file_upload)
            st.dataframe(df_restore)
            st.info("✅ Data berjaya dimuat naik. **Sila implement restore ke Google Sheets secara manual.**")

# =========================================
# ✅ Footer
# =========================================
papar_footer(
    owner="MKR Dev Team",
    version="v4.3.0",
    last_update="2025-06-30",
    tagline="Empowering Data-Driven Decisions."
)
