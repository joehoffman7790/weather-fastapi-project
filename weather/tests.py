from unittest.mock import patch

import pytest
from django.test import Client


@pytest.fixture
def client():
    return Client()


def test_dashboard_loads(client):
    """Dashboard returns 200."""
    response = client.get("/")
    assert response.status_code == 200


def test_dashboard_search_no_params(client):
    """Search with no params returns error in partial."""
    response = client.get("/search/")
    assert response.status_code == 200
    assert b"Please provide" in response.content


def test_dashboard_search_by_city(client):
    """Search by city returns weather partial."""
    mock_result = {
        "current": {
            "city": "London",
            "country": "GB",
            "temp": 15.0,
            "feels_like": 13.0,
            "humidity": 80,
            "wind_speed": 5.0,
            "condition": "Clouds",
            "description": "overcast clouds",
        },
        "forecast": [],
    }
    with patch("weather.views._get_weather_service") as mock_service:
        mock_service.return_value.get_weather_by_city.return_value = mock_result
        response = client.get("/search/?city=London")
    assert response.status_code == 200


def test_api_weather_no_params(client):
    """API weather with no params returns 400."""
    response = client.get("/api/weather/")
    assert response.status_code == 400


def test_api_weather_by_city(client):
    """API weather by city returns 200."""
    mock_result = {
        "current": {
            "city": "London",
            "country": "GB",
            "temp": 15.0,
            "feels_like": 13.0,
            "humidity": 80,
            "wind_speed": 5.0,
            "condition": "Clouds",
            "description": "overcast clouds",
        },
        "forecast": [],
    }
    with patch("weather.views._get_weather_service") as mock_service:
        mock_service.return_value.get_weather_by_city.return_value = mock_result
        response = client.get("/api/weather/?city=London")
    assert response.status_code == 200
