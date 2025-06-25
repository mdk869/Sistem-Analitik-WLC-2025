from datetime import datetime
import pytz

# === Tarikh & Masa Lokal Malaysia
def get_tarikh_masa():
    tz = pytz.timezone('Asia/Kuala_Lumpur')
    return datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

def get_bulan_sekarang():
    tz = pytz.timezone('Asia/Kuala_Lumpur')
    return datetime.now(tz).strftime('%Y-%m')
