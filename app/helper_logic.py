import pandas as pd


def tambah_kiraan_peserta(df):
    df = df.copy()

    df["BMI"] = ((df["BeratTerkini"] / (df["Tinggi"]/100) ** 2)).round(2)
    df["% Penurunan"] = ((df["BeratAwal"] - df["BeratTerkini"]) / df["BeratAwal"] * 100).round(2)

    df["Kategori"] = pd.cut(
        df["BMI"],
        bins=[0, 18.5, 24.9, 29.9, 100],
        labels=["Underweight", "Normal", "Overweight", "Obese"]
    ).astype(str)

    return df


def kira_progress_program():
    tarikh_mula = pd.Timestamp("2025-06-01")
    tarikh_tamat = pd.Timestamp("2025-12-31")
    hari_berlalu = (pd.Timestamp.now().normalize() - tarikh_mula).days + 1
    total_hari = (tarikh_tamat - tarikh_mula).days + 1
    progress = min(max(hari_berlalu / total_hari * 100, 0), 100)

    if progress >= 100:
        status = "Program Tamat"
    elif progress >= 80:
        status = "Fasa Akhir"
    elif progress >= 50:
        status = "Separuh Jalan"
    else:
        status = "Baru Bermula"

    return {
        "tarikh_mula": tarikh_mula,
        "tarikh_tamat": tarikh_tamat,
        "hari_berlalu": hari_berlalu,
        "progress": round(progress, 2),
        "status": status
    }

def kira_bmi(berat, tinggi):
    try:
        tinggi_meter = tinggi / 100
        bmi = berat / (tinggi_meter ** 2)
        return round(bmi, 2)
    except:
        return 0


def kategori_bmi_asia(bmi):
    if bmi < 18.5:
        return "Kurang Berat Badan"
    elif 18.5 <= bmi <= 24.9:
        return "Normal"
    elif 25 <= bmi <= 29.9:
        return "Lebih Berat Badan"
    elif 30 <= bmi <= 34.9:
        return "Obesiti Tahap 1"
    elif 35 <= bmi <= 39.9:
        return "Obesiti Tahap 2"
    else:
        return "Obesiti Morbid"

df["KategoriBMI"] = df["BMI"].apply(kategori_bmi_asia)
