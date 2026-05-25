from django.conf import settings
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .clients import OpenWeatherClient
from .models import SearchHistory
from .serializers import SearchHistorySerializer
from .services import WeatherService

WEATHER_EMOJI = {
    "Clear": "☀️",
    "Clouds": "☁️",
    "Rain": "🌧️",
    "Drizzle": "🌦️",
    "Thunderstorm": "⛈️",
    "Snow": "🌨️",
    "Mist": "🌫️",
    "Fog": "🌫️",
    "Haze": "🌫️",
    "Smoke": "🌫️",
    "Dust": "🌫️",
    "Sand": "🌫️",
    "Ash": "🌫️",
    "Squall": "💨",
    "Tornado": "🌪️",
}

def _enrich_with_emoji(result: dict) -> dict:
    """Add emoji icons to current and forecast based on condition."""
    result["current"]["emoji"] = WEATHER_EMOJI.get(result["current"]["condition"], "🌡️")
    for day in result["forecast"]:
        day["emoji"] = WEATHER_EMOJI.get(day["condition"], "🌡️")
    return result


def _get_weather_service() -> WeatherService:
    """Construct a WeatherService with the configured API key."""
    client = OpenWeatherClient(settings.OPENWEATHERMAP_API_KEY)
    return WeatherService(client)


# ─── HTMX dashboard views (return HTML) ────────────────────────────────────


def dashboard(request):
    """The main HTML page with the search form."""
    return render(request, "weather/dashboard.html")


def dashboard_search(request):
    """HTMX endpoint - returns an HTML fragment with weather data."""
    city = request.GET.get("city")
    lat = request.GET.get("lat")
    lng = request.GET.get("lng")

    service = _get_weather_service()

    try:
        if city:
            result = service.get_weather_by_city(city)
        elif lat and lng:
            result = service.get_weather_by_coordinates(float(lat), float(lng))
        else:
            return render(
                request,
                "weather/_weather_partial.html",
                {"error": "Please provide a city or coordinates."},
            )
    except ValueError as e:
        return render(request, "weather/_weather_partial.html", {"error": str(e)})

    result = _enrich_with_emoji(result)
    return render(request, "weather/_weather_partial.html", {"data": result})


# ─── DRF API views (return JSON) ───────────────────────────────────────────


@api_view(["GET"])
def weather(request):
    """
    GET /api/weather/?city=London
    GET /api/weather/?lat=51.5&lng=-0.12
    """
    city = request.query_params.get("city")
    lat = request.query_params.get("lat")
    lng = request.query_params.get("lng")

    service = _get_weather_service()

    try:
        if city:
            result = service.get_weather_by_city(city)
        elif lat and lng:
            result = service.get_weather_by_coordinates(float(lat), float(lng))
        else:
            return Response(
                {"error": "Provide either 'city' or both 'lat' and 'lng' query params."},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    return Response(result)


@api_view(["GET"])
def search_history(request):
    """GET /api/searches/ — return the 20 most recent searches."""
    recent = SearchHistory.objects.select_related("location").all()[:20]
    serializer = SearchHistorySerializer(recent, many=True)
    return Response(serializer.data)
