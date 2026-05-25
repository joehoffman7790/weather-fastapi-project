from rest_framework import serializers

from .models import CurrentWeather, ForecastDay, Location, SearchHistory


class LocationSerializer(serializers.ModelSerializer):
    """Serializes a Location model."""

    class Meta:
        model = Location
        fields = ["name", "country_code", "latitude", "longitude"]


class CurrentWeatherSerializer(serializers.ModelSerializer):
    """Serializes current weather, including computed Fahrenheit fields."""

    temp_f = serializers.FloatField(read_only=True)
    feels_like_f = serializers.FloatField(read_only=True)
    wind_speed_mph = serializers.FloatField(read_only=True)

    class Meta:
        model = CurrentWeather
        fields = [
            "temp_c",
            "temp_f",
            "feels_like_c",
            "feels_like_f",
            "humidity",
            "wind_speed_ms",
            "wind_speed_mph",
            "condition",
            "condition_icon",
            "fetched_at",
        ]


class ForecastDaySerializer(serializers.ModelSerializer):
    """Serializes a single forecast day, including computed Fahrenheit fields."""

    temp_high_f = serializers.FloatField(read_only=True)
    temp_low_f = serializers.FloatField(read_only=True)

    class Meta:
        model = ForecastDay
        fields = [
            "date",
            "temp_high_c",
            "temp_high_f",
            "temp_low_c",
            "temp_low_f",
            "condition",
            "condition_icon",
        ]


class WeatherResponseSerializer(serializers.Serializer):
    """Top-level response shape combining location, current, and forecast."""

    location = LocationSerializer()
    current = CurrentWeatherSerializer()
    forecast = ForecastDaySerializer(many=True)


class SearchHistorySerializer(serializers.ModelSerializer):
    """Serializes a search history entry, with location nested."""

    location = LocationSerializer(read_only=True)

    class Meta:
        model = SearchHistory
        fields = ["location", "search_type", "searched_at"]