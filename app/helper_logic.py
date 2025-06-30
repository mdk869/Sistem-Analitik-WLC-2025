import pandas as pd
from app.helper_utils import convert_columns_to_numeric

def tambah_kiraan_peserta(df):
    """
    Tambah kolum BMI, Kategori dan % Penurunan ke dataframe peserta.
    """
    df = df.copy()

    # Tukar kolum kepada numeric
    df = convert_columns_to_numeric(df, ["Tinggi", "BeratAwal", "BeratTerkini"])

    # Isi NaN dengan 0 untuk elakkan error
    df[["Tinggi", "BeratAwal", "BeratTerkini"]] = df[["Tinggi", "BeratAwal", "BeratTerkini"]].fillna(0)

    # Kiraan BMI dengan kawalan ZeroDivisionError
    df["BMI"] = df.apply(
        lambda x: round(x["BeratTerkini"] / (x["Tinggi"] / 100) ** 2, 2) if x["Tinggi"] > 0 else 0,
        axis=1
    )
    df["Kategori"] = df["BMI"].apply(kategori_bmi_asia)

    # Kiraan % Penurunan dengan kawalan ZeroDivisionError
    df["% Penurunan"] = df.apply(
        lambda x: round(((x["BeratAwal"] - x["BeratTerkini"]) / x["BeratAwal"]) * 100, 2)
        if x["BeratAwal"] > 0 else 0,
        axis=1
    )

    # Bersihkan nilai -ve atau NaN
    df["% Penurunan"] = df["% Penurunan"].fillna(0).clip(lower=0)

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

# =========================================
# ✅ Kiraan BMI
# =========================================
def kira_bmi(berat, tinggi):
    try:
        tinggi_m = float(tinggi) / 100
        berat = float(berat)
        bmi = berat / (tinggi_m ** 2)
        return round(bmi, 2)
    except:
        return 0


# =========================================
# ✅ Kategori BMI Asia
# =========================================
def kategori_bmi_asia(bmi):
    try:
        bmi = float(bmi)
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 23:
            return "Normal"
        elif 23 <= bmi < 27.5:
            return "Overweight"
        else:
            return "Obese"
    except:
        return "-"

# =========================================
# ✅ Formula BMI
# =========================================
def kira_bmi(berat, tinggi):
    """
    BMI = berat (kg) / (tinggi (m))^2
    """
    try:
        tinggi_meter = tinggi / 100
        bmi = berat / (tinggi_meter ** 2)
        return round(bmi, 2)
    except Exception:
        return 0


# =========================================
# ✅ Kategori BMI Asia
# =========================================
def kategori_bmi_asia(bmi):
    """
    Kategori BMI berdasarkan standard Asia.
    """
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 23:
        return "Normal"
    elif 23 <= bmi < 27.5:
        return "Overweight"
    else:
        return "Obese"


# =========================================
# ✅ Tambah Kiraan BMI & Kategori
# =========================================
def tambah_kiraan_peserta(df):
    """
    Tambah kolum BMI dan Kategori ke dataframe peserta.
    """
    df = df.copy()
    df = convert_columns_to_numeric(df, ["Tinggi", "BeratTerkini"])

    df["BMI"] = (df["BeratTerkini"] / (df["Tinggi"] / 100) ** 2).round(2)
    df["Kategori"] = df["BMI"].apply(kategori_bmi_asia)

    return df


# =========================================
# ✅ Tambah Kolum Kiraan Peserta
# =========================================
def tambah_kiraan_peserta(df):
    """
    Tambah kolum BMI, Kategori dan % Penurunan ke dataframe peserta.
    """
    df = df.copy()

    # Tukar kolum kepada numeric
    df = convert_columns_to_numeric(df, ["Tinggi", "BeratAwal", "BeratTerkini"])

    # Kiraan BMI
    df["BMI"] = (
        df.apply(lambda x: kira_bmi(x["BeratTerkini"], x["Tinggi"]), axis=1)
    )
    df["Kategori"] = df["BMI"].apply(kategori_bmi_asia)

    # Kiraan % Penurunan
    df["% Penurunan"] = (
        ((df["BeratAwal"] - df["BeratTerkini"]) / df["BeratAwal"]) * 100
    ).round(2)

    df["% Penurunan"] = df["% Penurunan"].fillna(0).clip(lower=0)

    return df