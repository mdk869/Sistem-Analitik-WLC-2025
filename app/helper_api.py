# app/helper_api.py
import requests
import streamlit as st

# === API Quotes Motivasi ===
def get_quote():
    url = "https://api.quotable.io/random"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data["content"], data["author"]
        else:
            return None, None
    except:
        return None, None


# === API Senaman dari ExerciseDB ===
def get_exercise(body_part="back", jumlah=3):
    url = f"https://exercisedb.p.rapidapi.com/exercises/bodyPart/{body_part}"
    headers = {
        "X-RapidAPI-Key": st.secrets["RAPIDAPI_KEY"],
        "X-RapidAPI-Host": "exercisedb.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data[:jumlah]
        else:
            return []
    except:
        return []


# === API Cuaca (OpenWeather) ===
def get_weather(city="Kuala Selangor"):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={st.secrets['OPENWEATHER_KEY']}&units=metric"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            cuaca = data["weather"][0]["description"].title()
            suhu = data["main"]["temp"]
            return f"{cuaca}, {suhu}°C"
        else:
            return "Tidak dapat capai API cuaca"
    except:
        return "Tidak dapat capai API cuaca"
