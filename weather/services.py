import os
import httpx
from weather.models import CurrentWeather, Location

OWM_BASE = "https://api.openweathermap.org"


def _api_key() -> str:
    key = os.environ.get("OPENWEATHERMAP_API_KEY")
    if not key:
        raise RuntimeError("OPENWEATHERMAP_API_KEY is not set in the environment")
    return key


def geocode_city(name: str) -> dict | None:
    """Resolve a city name to its identifying details.

    Returns a dict with name, country, lat, lon — or None if the
    city can't be found. This is the 'resolve identity' step.
    """
    response = httpx.get(
        f"{OWM_BASE}/geo/1.0/direct",
        params={"q": name, "limit": 1, "appid": _api_key()},
        timeout=10.0,
    )
    response.raise_for_status()
    results = response.json()

    if not results:
        return None

    top = results[0]
    return {
        "name": top["name"],
        "country": top["country"],
        "lat": top["lat"],
        "lon": top["lon"],
    }


def fetch_current_weather(lat: float, lon: float) -> dict:
    """Fetch current weather for coordinates.

    Returns a normalized dict. This is the 'fetch data' step.
    """
    response = httpx.get(
        f"{OWM_BASE}/data/2.5/weather",
        params={
            "lat": lat,
            "lon": lon,
            "appid": _api_key(),
            "units": "imperial",
        },
        timeout=10.0,
    )
    response.raise_for_status()
    data = response.json()

    return {
        "temp": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "condition": data["weather"][0]["main"],
        "condition_icon": data["weather"][0]["icon"],
    }

def get_weather_for_city(name: str) -> dict | None:
    """Return current weather for a city, using the two-layer cache.

    Layer 1 (permanent): Location — a city's identity never changes.
    Layer 2 (time-boxed): CurrentWeather — expires via is_stale().

    Returns a dict the view can render, or None if the city
    can't be found.
    """
    served_from_cache = True  # assume cache hit; flip to False if we fetch

    # --- Layer 1: resolve the city to a Location (permanent cache) ---
    location = Location.objects.filter(name__iexact=name).first()

    if location is None:
        served_from_cache = False
        geo = geocode_city(name)
        if geo is None:
            return None
        location = Location.objects.create(
            name=geo["name"],
            country_code=geo["country"],
            latitude=geo["lat"],
            longitude=geo["lon"],
        )

    # --- Layer 2: get fresh weather for that Location (expiring cache) ---
    weather = CurrentWeather.objects.filter(location=location).first()

    if weather is None or weather.is_stale():
        served_from_cache = False
        fresh = fetch_current_weather(location.latitude, location.longitude)

        weather, _ = CurrentWeather.objects.update_or_create(
            location=location,
            defaults={
                "temp_c": fresh["temp"],
                "feels_like_c": fresh["feels_like"],
                "humidity": fresh["humidity"],
                "wind_speed_ms": fresh["wind_speed"],
                "condition": fresh["condition"],
                "condition_icon": fresh["condition_icon"],
            },
        )

    return {
        "city": location.name,
        "country": location.country_code,
        "temp": weather.temp_c,
        "feels_like": weather.feels_like_c,
        "humidity": weather.humidity,
        "wind_speed": weather.wind_speed_ms,
        "condition": weather.condition,
        "condition_icon": weather.condition_icon,
        "from_cache": served_from_cache,
    }

    return {
        "city": location.name,
        "country": location.country_code,
        "temp": weather.temp_c,
        "feels_like": weather.feels_like_c,
        "humidity": weather.humidity,
        "wind_speed": weather.wind_speed_ms,
        "condition": weather.condition,
        "condition_icon": weather.condition_icon,
        "from_cache": weather.is_stale() is False,
    }