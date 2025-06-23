import requests
import os
from dotenv import load_dotenv
from gps_tracker import get_gps_location  # This must return (lat, lon)

load_dotenv()
weather_api_key = os.getenv("OPENWEATHER_API_KEY")
weather_api_url = "https://api.openweathermap.org/data/2.5/weather"
road_api_url = "https://nominatim.openstreetmap.org/reverse"

class Roadconditions:
    """Fetches real-time road and weather-based surface conditions."""

    def __init__(self):
        self.data = {
            "condition": "dry",
            "weather_main": "clear",
            "weather_description": "",
            "temperature": None,
            "humidity": None,
            "pressure": None,
            "wind_speed": None,
            "road_class": "unknown",
            "road_type": "unknown",
            "friction_coefficient": 0.7,
            "location": None,
            "road_data": {}
        }

        self.friction_map = {
            "asphalt": 0.8,
            "concrete": 0.75,
            "gravel": 0.5,
            "unpaved": 0.4,
            "icy": 0.2,
            "wet": 0.6,
            "snow": 0.3,
            "mud": 0.35,
            "residential": 0.75,
            "highway": 0.85,
        }

    def fetch_weather_data(self, lat, lon):
        try:
            response = requests.get(weather_api_url, params={
                "lat": lat,
                "lon": lon,
                "appid": weather_api_key,
                "units": "metric"
            })

            if response.status_code == 200:
                json_data = response.json()
                self.data["weather_main"] = json_data["weather"][0]["main"].lower()
                self.data["weather_description"] = json_data["weather"][0]["description"]
                self.data["temperature"] = json_data["main"]["temp"]
                self.data["humidity"] = json_data["main"]["humidity"]
                self.data["pressure"] = json_data["main"]["pressure"]
                self.data["wind_speed"] = json_data["wind"]["speed"]

                if self.data["weather_main"] in ["rain", "drizzle", "snow", "mist"]:
                    self.data["condition"] = self.data["weather_main"]
                elif self.data["weather_main"] in ["clear", "clouds"]:
                    self.data["condition"] = "dry"

        except Exception as e:
            print("Weather API error:", e)

    def fetch_road_data(self, lat, lon):
        try:
            response = requests.get(road_api_url, params={
                "lat": lat,
                "lon": lon,
                "format": "json"
            })

            if response.status_code == 200:
                json_data = response.json()
                self.data["road_data"] = json_data

                road_class = json_data.get("class") or json_data.get("osm_type") or "unknown"
                road_type = json_data.get("type") or json_data.get("address", {}).get("road") or "unknown"

                self.data["road_class"] = road_class.lower() if isinstance(road_class, str) else str(road_class)
                self.data["road_type"] = road_type.lower() if isinstance(road_type, str) else str(road_type)

                location = json_data.get("display_name")
                if not location:
                    address = json_data.get("address", {})
                    location = ", ".join(filter(None, [
                        address.get("road"),
                        address.get("suburb"),
                        address.get("city_district"),
                        address.get("city"),
                        address.get("state"),
                        address.get("country")
                    ]))

                self.data["location"] = location or "Unknown location"

        except Exception as e:
            print("Road API error:", e)

    def calculate_friction(self):
        base_friction = self.friction_map.get(self.data["road_type"], 0.7)
        condition = self.data["condition"]

        if condition in ["rain", "snow", "wet"]:
            base_friction *= 0.7
        elif condition in ["icy", "mud"]:
            base_friction *= 0.5

        self.data["friction_coefficient"] = round(base_friction, 2)

    def analyze(self):
        lat, lon = get_gps_location()
        if lat and lon:
            print(f"GPS Location: {lat}, {lon}")
            self.fetch_weather_data(lat, lon)
            self.fetch_road_data(lat, lon)
            self.calculate_friction()

    def get_conditions(self):
        return self.data

    def __str__(self):
        road_data_str = "\n".join(f"{key}: {value}" for key, value in self.data['road_data'].items())
        return (
            f"Location: {self.data['location']}\n"
            f"Weather: {self.data['weather_main'].capitalize()} ({self.data['weather_description']})\n"
            f"Temperature: {self.data['temperature']}°C | Humidity: {self.data['humidity']}% | Pressure: {self.data['pressure']} hPa\n"
            f"Road: {self.data['road_class']} - {self.data['road_type']}\n"
            f"Friction Coefficient: {self.data['friction_coefficient']}\n"
            f"Full Road Data:\n{road_data_str}"
        )

if __name__ == "__main__":
    rc = Roadconditions()
    rc.analyze()
    print("\nFinal Road & Weather Conditions:\n")
    print(rc)
    print(rc.get_conditions())