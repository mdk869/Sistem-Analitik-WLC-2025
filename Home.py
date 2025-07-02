import streamlit as st
from app.styles import paparkan_tema, papar_header, papar_footer
from app.settings import info_program
from app.logger import log_traffic_to_sheet

# ========================================
# ✅ Layout & Header
# ========================================
paparkan_tema()
papar_header("Home | WLC 2025")

st.title("🏠 Selamat Datang ke Sistem Analitik WLC 2025")
st.markdown("Sistem ini direka untuk membantu penganjur memantau perkembangan peserta sepanjang program.")

st.divider()

log_traffic_to_sheet()

if "logged" not in st.session_state:
    log_traffic_to_sheet()
    st.session_state["logged"] = True

# ========================================
# ✅ Info Program
# ========================================
st.subheader("📜 Info Program WLC 2025")

st.info(f"""
**{info_program['nama_program']}**

🗓️ **Tarikh Program:** {info_program['tarikh_mula'].strftime('%d %B %Y')} hingga {info_program['tarikh_tamat'].strftime('%d %B %Y')}

🎯 **Objektif Program:**
- Membantu peserta mencapai berat badan ideal
- Meningkatkan kesedaran tentang kesihatan dan gaya hidup sihat
- Mewujudkan budaya hidup aktif di tempat kerja dan komuniti
""")

st.divider()


# ========================================
# ✅ Jadual Program
# ========================================
st.subheader("📅 Jadual & Perjalanan Program")

st.markdown("""
- 🔥 **18 Jun 2025** — Pendaftaran & Timbang Awal
- 📊 **17 Julai 2025** — Sesi Timbangan Ke-2
- 🏆 **20 Ogos 2025** — Timbangan Akhir & Penilaian
""")

st.info("✅ Peserta wajib hadir 3 sesi timbangan untuk melayakkan diri dalam penilaian akhir.")

st.divider()


# ========================================
# ✅ Panduan Peserta
# ========================================
st.subheader("📖 Panduan Peserta")

st.markdown("""
- ✅ Pastikan hadir sesi timbang mengikut jadual.
- ✅ Data berat akan direkod untuk analisis dan penilaian.
- 🔒 Data adalah sulit dan hanya pihak penganjur yang boleh akses.
- 💡 Gunakan dashboard untuk melihat perkembangan BMI, penurunan berat dan leaderboard.
""")

st.divider()


# ========================================
# ✅ Hubungi Penganjur
# ========================================
st.subheader("📞 Hubungi Penganjur")

st.markdown("""
- 📧 Email: irwan.zon@airselangor.com
- ☎️ Telefon: 03-3280 5485
- 🏢 Unit HSE, Wilayah Kuala Selangor
""")

st.divider()


# ========================================
# ✅ Footer
# ========================================
papar_footer()
