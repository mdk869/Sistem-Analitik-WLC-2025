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
    nutrisi_list = [
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


def get_tips_kesihatan(jumlah=1):
    health_list = [
    "Get morning sunlight for natural Vitamin D.",
    "Dapatkan cahaya matahari pagi sekurang-kurangnya 10-15 minit.",
    "Check your health regularly — blood pressure, sugar, cholesterol.",
    "Buat pemeriksaan kesihatan berkala untuk cegah penyakit.",
    "Healthy living is a lifestyle, not a short-term goal.",
    "Gaya hidup sihat bukan untuk sementara, tapi untuk sepanjang hayat.",
    "Small steps everyday lead to big changes.",
    "Langkah kecil hari ini akan jadi perubahan besar esok.",
    "Avoid smoking and limit alcohol — your body will thank you.",
    "Berhenti merokok dan kurangkan alkohol untuk kesihatan lebih baik.",
    "Sleep early, wake up fresh.",
    "Tidur awal, bangun dengan lebih segar dan produktif.",
    "No excuses — your health is your responsibility.",
    "Tiada alasan — kesihatan adalah tanggungjawab diri sendiri.",
    "Love yourself enough to live a healthy life.",
    "Sayangi diri sendiri dengan memilih hidup yang lebih sihat."
    "Get enough sleep, at least 6-8 hours per night.",
    "Tidur yang cukup bantu jaga kesihatan badan dan mental.",
    "Breathe deeply, relax, and manage your stress.",
    "Urus tekanan dengan aktiviti santai atau hobi kegemaran.",
    "Laugh more, stress less.",
    "Ketawa lebih, stress kurang.",
    "Don’t compare your journey to others — focus on yourself.",
    "Bandingkan diri dengan versi diri anda semalam, bukan orang lain.",
    "If you’re tired, rest — not quit.",
    "Kalau penat, rehat. Jangan berhenti.",
    "Stay consistent, not perfect.",
    "Konsisten lebih penting daripada kesempurnaan."
    "Move more, sit less.",
    "Bergerak sekurang-kurangnya 30 minit sehari.",
    "Exercise not just for weight loss, but for a healthy mind.",
    "Senaman bukan untuk kurus saja, tapi untuk badan dan minda yang sihat.",
    "Take regular breaks from screens — rest your eyes and mind.",
    "Jangan duduk terlalu lama, bangun dan regangkan badan setiap jam.",
    "Strengthen your muscles — it helps with fat loss and long-term health.",
    "Bina otot untuk kesihatan jangka panjang dan bakar lebih kalori.",
    "Walk after meals — helps digestion and blood sugar control.",
    "Berjalan 5-10 minit selepas makan bantu penghadaman.",
    "Sweat daily — your body is designed to move.",
    "Berpeluh setiap hari, itu tanda badan aktif dan sihat."
    ]

    jumlah = min(jumlah, len(health_list))
    return random.sample(health_list, jumlah)