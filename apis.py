import os
from dotenv import load_dotenv
from lat_lon import get_lat_lon
from user_input import location_start

load_dotenv()
weather_api_key = os.getenv("OPENWEATHER_API_KEY")

weather_api_url = "https://api.openweathermap.org/data/2.5/weather"

def fetch_coordinates():
    try:
        coords = get_lat_lon(location_start)
        if coords:
            return coords
    except Exception as e:
        print(f"Error fetching coordinates: {e}")
    from user_input import get_user_input
    return get_user_input()

lat, lon = fetch_coordinates()
weather_url = f"{weather_api_url}?lat={lat}&lon={lon}&appid={weather_api_key}"

print("Weather API URL:", weather_url)
