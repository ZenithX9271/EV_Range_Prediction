import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError

geolocator = Nominatim(user_agent="ev_range_predictor")

def get_lat_lon(place_name):
    try:
        location = geolocator.geocode(place_name)
        if location:
            return (location.latitude, location.longitude)
    except GeocoderServiceError as e:
        print(f"⚠ Geocoding error: {e}")
    return None


def main():
    location_start = "Tirupati"
    location_end = "Piler"
    lat_start, lon_start = get_lat_lon(location_start)
    time.sleep(1)
    lat_end, lon_end = get_lat_lon(location_end)
    return lat_start, lon_start, lat_end, lon_end