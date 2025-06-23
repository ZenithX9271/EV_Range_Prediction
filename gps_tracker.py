import geocoder
import time

def get_gps_location():
    """Fetches GPS coordinates based on public IP."""
    location = geocoder.ip('me')
    if location.ok:
        return location.lat, location.lng
    return None, None
