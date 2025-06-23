import requests
from lat_lon import get_lat_lon
from user_input import location_start, location_end

ELEVATION_API_URL = "https://api.open-elevation.com/api/v1/lookup"

class RoadFeatures:
    def __init__(self):
        self.slope = 0.0
        self.curvature = 0.0
        self.elevations = []
        self._fetch_and_compute_features()

    def _fetch_and_compute_features(self):
        start = get_lat_lon(location_start)
        end = get_lat_lon(location_end)

        if not start or not end:
            print("⚠ Could not determine coordinates. Using defaults.")
            return

        lat1, lon1 = start
        lat2, lon2 = end
        mid_lat, mid_lon = (lat1 + lat2) / 2, (lon1 + lon2) / 2

        url = f"{ELEVATION_API_URL}?locations={lat1},{lon1}|{mid_lat},{mid_lon}|{lat2},{lon2}"

        try:
            res = requests.get(url, timeout=5)
            res.raise_for_status()
            results = res.json().get("results", [])

            if len(results) == 3:
                self.elevations = [pt["elevation"] for pt in results]
                self._calculate_features(self.elevations)
            else:
                print("⚠ Unexpected API response. Using defaults.")

        except Exception as e:
            print(f"⚠ Error fetching elevation data: {e}")

    def _calculate_features(self, elevations):
        horizontal_distance = 1000  # Assume 1 km
        elevation_gain = elevations[-1] - elevations[0]
        max_variation = max(abs(elevations[1] - elevations[0]), abs(elevations[2] - elevations[1]))

        self.slope = max(-30, min(30, (elevation_gain / horizontal_distance) * 100))
        self.curvature = min(1.0, max_variation / 100)

    def get_slope_penalty(self):
        return 1 + (self.slope / 30) * 0.5 if self.slope > 0 else 1 - (abs(self.slope) / 30) * 0.3

    def get_curvature_penalty(self):
        return 1 + self.curvature * 0.2

    def get_features(self):
        elevation_start = self.elevations[0] if len(self.elevations) > 0 else None
        elevation_mid = self.elevations[1] if len(self.elevations) > 1 else None
        elevation_end = self.elevations[2] if len(self.elevations) > 2 else None

        return {
            "slope": round(self.slope, 2),
            "curvature": round(self.curvature, 2),
            "slope_penalty": round(self.get_slope_penalty(), 3),
            "curvature_penalty": round(self.get_curvature_penalty(), 3),
            "elevation_start": elevation_start,
            "elevation_mid": elevation_mid,
            "elevation_end": elevation_end
        }

    def __str__(self):
        return f"Real-world Slope: {self.slope:.2f}° | Curvature: {self.curvature:.2f}"

if __name__ == "__main__":
    rf = RoadFeatures()
    print(rf)
    print(rf.get_features())