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

def get_tips_nutrisi(jumlah=1):
    nutrisi_list = [
        "🚫 Kurangkan minuman manis (teh tarik, air gas, sirap).",
        "🍟 Elakkan makanan bergoreng dan berminyak.",
        "🍪 Hadkan gula tersembunyi (biskut, kek, roti putih).",
        "🧂 Kurangkan garam berlebihan (jajan, makanan segera).",
        "🥗 Lebihkan sayur dan buah dalam setiap hidangan.",
        "🚶‍♂️ Banyakkan aktiviti fizikal, sekurang-kurangnya 30 minit sehari."  
    ]
    jumlah = min(jumlah, len(nutrisi_list))
    return random.sample(nutrisi_list, jumlah)
