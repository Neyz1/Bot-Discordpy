# Générer par IA 

import requests

# ⚡ Ta clé API OpenWeatherMap
API_KEY = "TA_CLE_API_ICI"

# Ville à chercher
city = "Paris"

# Requête API
url = "https://api.openweathermap.org/data/2.5/weather"
params = {
    "q": city,
    "appid": API_KEY,
    "units": "metric",
    "lang": "fr"
}

response = requests.get(url, params=params)

if response.status_code != 200:
    print("❌ Ville introuvable.")
else:
    data = response.json()

    # Stockage des infos dans des variables simples
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    wind = data["wind"]["speed"]
    description = data["weather"][0]["description"].capitalize()

    # Affichage simple
    print("🌡 Température :", temp, "°C")
    print("🤔 Ressenti   :", feels_like, "°C")
    print("💧 Humidité   :", humidity, "%")
    print("🌬 Vent       :", wind, "m/s")
    print("☁️ Condition  :", description)