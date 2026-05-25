from collections import defaultdict
from datetime import datetime

from .clients import OpenWeatherClient
from .models import CurrentWeather, ForecastDay, Location, SearchHistory


class WeatherService:
    """Orchestrates OpenWeatherMap calls and database caching."""

    def __init__(self, client: OpenWeatherClient):
        self.client = client

    def get_weather_by_city(self, name: str) -> dict:
        """Look up weather by city name. Geocodes first, then delegates."""
        geocode_result = self.client.geocode(name)
        location, _ = Location.objects.get_or_create(
            latitude=round(geocode_result["lat"], 6),
            longitude=round(geocode_result["lon"], 6),
            defaults={
                "name": geocode_result["name"],
                "country_code": geocode_result.get("country", ""),
            },
        )
        return self._get_weather_for_location(location, search_type="city")

    def get_weather_by_coordinates(self, latitude: float, longitude: float) -> dict:
        """Look up weather by coordinates directly."""
        location, _ = Location.objects.get_or_create(
            latitude=round(latitude, 6),
            longitude=round(longitude, 6),
            defaults={"name": f"{latitude},{longitude}", "country_code": ""},
        )
        return self._get_weather_for_location(location, search_type="coordinates")

    def _get_weather_for_location(self, location: Location, search_type: str) -> dict:
        """Internal: check cache, refresh if needed, return combined data."""
        # Record the search
        SearchHistory.objects.create(location=location, search_type=search_type)

        # Refresh current weather if stale or missing
        current = getattr(location, "current", None)
        if current is None or current.is_stale():
            current = self._refresh_current(location)

        # Refresh forecast if stale or missing
        forecast_days = list(location.forecast_days.all())
        if not forecast_days or any(day.is_stale() for day in forecast_days):
            forecast_days = self._refresh_forecast(location)

        return {
            "location": {
                "name": location.name,
                "country_code": location.country_code,
                "latitude": float(location.latitude),
                "longitude": float(location.longitude),
            },
            "current": {
                "temp_c": current.temp_c,
                "temp_f": round(current.temp_f, 1),
                "feels_like_c": current.feels_like_c,
                "feels_like_f": round(current.feels_like_f, 1),
                "humidity": current.humidity,
                "wind_speed_ms": current.wind_speed_ms,
                "wind_speed_mph": round(current.wind_speed_mph, 1),
                "condition": current.condition,
                "condition_icon": current.condition_icon,
            },
            "forecast": [
                {
                    "date": day.date,
                    "temp_high_c": day.temp_high_c,
                    "temp_high_f": round(day.temp_high_f, 1),
                    "temp_low_c": day.temp_low_c,
                    "temp_low_f": round(day.temp_low_f, 1),
                    "condition": day.condition,
                    "condition_icon": day.condition_icon,
                }
                for day in forecast_days
            ],
        }

    def _refresh_current(self, location: Location) -> CurrentWeather:
        """Fetch current weather from the API and save to the database."""
        data = self.client.fetch_current(float(location.latitude), float(location.longitude))
        weather = data["weather"][0]
        # Delete the old one if it exists, then create new (auto_now_add resets fetched_at)
        CurrentWeather.objects.filter(location=location).delete()
        return CurrentWeather.objects.create(
            location=location,
            temp_c=data["main"]["temp"],
            feels_like_c=data["main"]["feels_like"],
            humidity=data["main"]["humidity"],
            wind_speed_ms=data["wind"]["speed"],
            condition=weather["main"],
            condition_icon=weather["icon"],
        )

    def _refresh_forecast(self, location: Location) -> list[ForecastDay]:
        """Fetch the 5-day forecast, aggregate to daily highs/lows, save to database."""
        data = self.client.fetch_forecast(float(location.latitude), float(location.longitude))

        # Group 3-hour entries by date
        by_date = defaultdict(list)
        for entry in data["list"]:
            date_str = entry["dt_txt"].split(" ")[0]  # "2026-05-24 12:00:00" → "2026-05-24"
            by_date[date_str].append(entry)

        # Delete the old forecast for this location, then build new
        ForecastDay.objects.filter(location=location).delete()

        new_days = []
        for date_str, entries in by_date.items():
            high = max(e["main"]["temp_max"] for e in entries)
            low = min(e["main"]["temp_min"] for e in entries)
            # Pick the entry closest to noon as "representative" for icon/condition
            noon_entry = min(entries, key=lambda e: abs(int(e["dt_txt"].split(" ")[1].split(":")[0]) - 12))
            day = ForecastDay.objects.create(
                location=location,
                date=datetime.strptime(date_str, "%Y-%m-%d").date(),
                temp_high_c=high,
                temp_low_c=low,
                condition=noon_entry["weather"][0]["main"],
                condition_icon=noon_entry["weather"][0]["icon"],
            )
            new_days.append(day)

        return new_days