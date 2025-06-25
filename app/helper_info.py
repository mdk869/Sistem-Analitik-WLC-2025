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
