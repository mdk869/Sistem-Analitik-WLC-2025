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
    tarikh_mula = pd.Timestamp("2025-06-18")
    tarikh_tamat = pd.Timestamp("2025-08-20")
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

# =========================================
# ✅ Kiraan Berat Ideal dan Target Realistik
# =========================================

def kira_berat_ideal(tinggi_cm, target_bmi=22.0):
    tinggi_m = tinggi_cm / 100
    berat_ideal = target_bmi * (tinggi_m ** 2)
    return round(berat_ideal, 2)


def kira_berat_target(tinggi_cm, target_bmi):
    tinggi_m = tinggi_cm / 100
    berat_target = target_bmi * (tinggi_m ** 2)
    return round(berat_target, 2)


def kira_target_realistik(berat_sekarang, tinggi_cm):
    berat_overweight = kira_berat_target(tinggi_cm, 24.9)
    penurunan_5 = berat_sekarang * 0.05
    penurunan_10 = berat_sekarang * 0.10

    # Pilih target yang lebih logik: capai overweight atau turun 10%
    target = max(berat_overweight, berat_sekarang - penurunan_10)
    return round(target, 2)


def dataframe_status_berat(df):
    data = []

    for _, row in df.iterrows():
        tinggi = row["Tinggi"]
        berat = row["BeratTerkini"]
        nama = row["Nama"]
        kategori = row["Kategori"]

        berat_overweight = kira_berat_target(tinggi, 24.9)
        berat_ideal = kira_berat_ideal(tinggi)

        target_realistik = kira_target_realistik(berat, tinggi)

        perlu_turun_ideal = max(0, round(berat - berat_ideal, 2))
        perlu_turun_realistik = max(0, round(berat - target_realistik, 2))

        data.append({
            "Nama": nama,
            "Kategori Sekarang": kategori,
            "Berat Sekarang (kg)": berat,
            "Target Realistik (kg)": target_realistik,
            "Perlu Turun (Realistik) (kg)": perlu_turun_realistik,
            "Berat Ideal (kg)": berat_ideal,
            "Perlu Turun (Ideal) (kg)": perlu_turun_ideal
        })

    df_status = pd.DataFrame(data)
    return df_status.sort_values(by="Perlu Turun (Realistik) (kg)", ascending=False)

def generate_kiraan_penurunan(df):
    df = df.copy()

    df['Berat Ideal'] = df.apply(kira_berat_ideal, axis=1)
    df['Target Realistik'] = df.apply(kira_target_realistik, axis=1)

    df['Perlu Turun (Ideal)'] = (df['BeratTerkini'] - df['Berat Ideal']).apply(lambda x: round(x, 2) if x > 0 else 0)
    df['Perlu Turun (Realistik)'] = (df['BeratTerkini'] - df['Target Realistik']).apply(lambda x: round(x, 2) if x > 0 else 0)

    df_output = df[['Nama', 'Kategori', 'BeratTerkini', 'Target Realistik', 'Perlu Turun (Realistik)', 'Berat Ideal', 'Perlu Turun (Ideal)']]
    return df_output.sort_values(by="Perlu Turun (Realistik)", ascending=False).reset_index(drop=True)