# app/helper_info.py

import random

def get_motivasi_harian():
    motivasi_list = [
        "Setiap langkah kecil membawa perubahan besar.",
        "Kejayaan bermula dengan tindakan hari ini.",
        "Fokus pada progres, bukan kesempurnaan.",
        "Air kosong lebih berharga dari air bergula.",
        "Tubuh yang sihat adalah aset paling berharga.",
        "Bergerak lebih, duduk kurang!",
        "Pilihan hari ini menentukan kesihatan masa depan.",
        "Makan untuk hidup, bukan hidup untuk makan."
    ]
    return random.choice(motivasi_list)

def get_tips_nutrisi():
    nutrisi_list = [
        "🍽️ Kawal Saiz Hidangan",
        "🥗 Utamakan Makanan Segar",
        "🥚 Cukupkan Protein",
        "🚫 Kurangkan"
        "- Minuman manis (teh tarik, air gas, sirap). "
        "- Makanan bergoreng dan berminyak."
        "- Gula tersembunyi (biskut, kek, roti putih)."
        "- Garam berlebihan (jajan, makanan segera).",
        "💧 Minum Air Cukup: Sasaran minimum 2–3 liter sehari. Elakkan air manis sebagai pengganti.",
        "⏰ Makan Ikut Jadual: Sarapan ringan + makan tengah hari seimbang + makan malam sederhana. ",
        "🏃‍♂️ Sokong dengan Aktiviti Fizikal: Sasaran 150 minit aktiviti fizikal sederhana seminggu."
       
    ]
    return random.choice(nutrisi_list)
