import httpx


class OpenWeatherClient:
    """Client for OpenWeatherMap API. Knows how to make API calls, nothing else."""

    BASE_URL = "https://api.openweathermap.org"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def geocode(self, city_name: str) -> dict:
        """Convert a city name to coordinates. Returns the first match."""
        url = f"{self.BASE_URL}/geo/1.0/direct"
        params = {
            "q": city_name,
            "limit": 1,
            "appid": self.api_key,
        }
        response = httpx.get(url, params=params)
        response.raise_for_status()
        results = response.json()
        if not results:
            raise ValueError(f"No geocoding results for '{city_name}'")
        return results[0]

    def fetch_current(self, latitude: float, longitude: float) -> dict:
        """Fetch current weather for given coordinates."""
        url = f"{self.BASE_URL}/data/2.5/weather"
        params = {
            "lat": latitude,
            "lon": longitude,
            "appid": self.api_key,
            "units": "metric",
        }
        response = httpx.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def fetch_forecast(self, latitude: float, longitude: float) -> dict:
        """Fetch 5-day / 3-hour forecast for given coordinates."""
        url = f"{self.BASE_URL}/data/2.5/forecast"
        params = {
            "lat": latitude,
            "lon": longitude,
            "appid": self.api_key,
            "units": "metric",
        }
        response = httpx.get(url, params=params)
        response.raise_for_status()
        return response.json()
