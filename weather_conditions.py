import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

class WeatherConditions:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.temperature = None
        self.wind_speed = None
        self.weather_main = "clear"
        self.weather_description = ""

    def fetch_weather(self):
        params = {
            "lat": self.latitude,
            "lon": self.longitude,
            "appid": API_KEY,
            "units": "metric"
        }

        try:
            response = requests.get(WEATHER_API_URL, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()

            self.temperature = data["main"]["temp"]
            self.wind_speed = data["wind"]["speed"]
            self.weather_main = data["weather"][0]["main"].lower()
            self.weather_description = data["weather"][0]["description"]

        except Exception as e:
            print(f"⚠ Weather API fetch failed: {e}")

    def get_penalty(self):
        penalty = 0
        if self.temperature is not None:
            if self.temperature < 5:
                penalty += 0.1
            elif self.temperature > 35:
                penalty += 0.08

        if self.wind_speed is not None:
            if self.wind_speed > 8:
                penalty += 0.07

        return penalty

    def __str__(self):
        return (
            f"Weather: {self.weather_main.capitalize()} ({self.weather_description})\n"
            f"Temperature: {self.temperature}°C | Wind Speed: {self.wind_speed} m/s\n"
            f"Efficiency Penalty: {self.get_penalty() * 100:.1f}%"
        )

if __name__ == "__main__":
    wc = WeatherConditions(28.5459, 77.1988)
    wc.fetch_weather()
    print(wc)