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
    "Makan untuk hidup, bukan hidup untuk makan.",
    "Perubahan bermula dari diri sendiri, bukan orang lain.",
    "Disiplin hari ini adalah kunci kejayaan esok.",
    "Kuat bukan kerana nasib, tapi kerana usaha berulang-ulang.",
    "Kesihatan bukan tujuan, ia adalah gaya hidup.",
    "Jangan bandingkan diri dengan orang lain, lawan hanya diri semalam.",
    "Kalori boleh dikira, tapi semangat tak boleh diukur.",
    "Satu senaman kecil lebih baik daripada tiada langsung.",
    "Kegagalan hari ini bukan penamat, tapi permulaan untuk bangkit.",
    "Tiada jalan pintas untuk sihat, hanya konsisten dan komitmen.",
    "Badan cergas, minda pun tajam.",
    "Every small step leads to big changes.",
    "Success starts with the actions you take today.",
    "Focus on progress, not perfection.",
    "Water is more valuable than sugary drinks.",
    "A healthy body is your greatest asset.",
    "Move more, sit less!",
    "The choices you make today shape your future health.",
    "Eat to live, not live to eat.",
    "Change begins with yourself, not others.",
    "Discipline today is the key to tomorrow’s success.",
    "Strength comes from consistent effort, not luck.",
    "Health isn’t a goal, it’s a lifestyle.",
    "Don’t compare yourself to others; compete with who you were yesterday.",
    "Calories can be counted, but determination is priceless.",
    "A short workout is better than no workout at all.",
    "Failure isn’t the end — it’s the beginning of a comeback.",
    "There’s no shortcut to being healthy — just consistency and commitment.",
    "Strong body, sharp mind.",
    "What you do today decides how you feel tomorrow.",
    "Small habits create big results."
    ]

    return random.choice(motivasi_list)

def get_tips_nutrisi(jumlah=1):
    nutrisi_list += [
    "🥤 Minum air kosong sekurang-kurangnya 2-3 liter sehari, elakkan air manis.",
    "🍚 Kawal saiz hidangan, guna konsep suku-suku-separuh.",
    "🥩 Cukupkan sumber protein dalam setiap hidangan (ayam, ikan, telur, tempe, kekacang).",
    "🍞 Pilih karbohidrat kompleks seperti beras perang, oat, ubi, atau roti wholemeal.",
    "🛑 Elakkan makanan ultra-proses seperti sosej, nugget, makanan segera.",
    "🍳 Masak dengan cara sihat — stim, rebus, grill, air fryer atau bakar.",
    "🔍 Sentiasa baca label makanan, semak jumlah gula, garam, dan lemak.",
    "⏰ Jangan skip makan, makan ikut waktu untuk elakkan craving berlebihan.",
    "🧠 Makan dengan mindful — kunyah perlahan dan nikmati makanan, elakkan makan sambil tengok skrin.",
    "😴 Tidur cukup 6–8 jam sehari untuk kawal hormon lapar dan tingkatkan metabolisme."
    ]

    jumlah = min(jumlah, len(nutrisi_list))
    return random.sample(nutrisi_list, jumlah)
