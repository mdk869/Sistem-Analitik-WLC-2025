import streamlit as st
from app.styles import paparkan_tema, papar_header, papar_footer
from app.settings import info_program


# ========================================
# ✅ Layout & Header
# ========================================
paparkan_tema()
papar_header("Home | WLC 2025")

st.title("🏠 Selamat Datang ke Sistem Analitik WLC 2025")
st.markdown("Sistem ini direka untuk membantu penganjur memantau perkembangan peserta sepanjang program.")

st.divider()


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
- 📊 **Julai 2025** — Sesi Timbang Bulanan 1
- 📊 **Ogos 2025** — Sesi Timbang Bulanan 2
- 🏆 **20 Ogos 2025** — Timbang Akhir & Majlis Penutup
""")

st.info("✅ Peserta wajib hadir sekurang-kurangnya 3 sesi timbang untuk melayakkan diri dalam penilaian akhir.")

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
- 📧 Email: wlc2025@domain.com
- ☎️ Telefon: 012-3456789
- 🏢 Unit Sumber Manusia, Wilayah Kuala Selangor
""")

st.divider()


# ========================================
# ✅ Footer
# ========================================
papar_footer(
    owner="MKR Dev Team",
    version=info_program["versi"],
    last_update="2025-06-29",
    tagline="Empowering Data-Driven Decisions."
)
