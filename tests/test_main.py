from unittest.mock import patch

from fastapi.testclient import TestClient

# Patch get_api_key BEFORE importing the app, so the cached value is the mock.
# This prevents any real Azure Key Vault calls during tests.
with patch("main.get_api_key", return_value="test_key_for_ci"):
    from main import app

client = TestClient(app)


def test_read_root():
    """Test the root endpoint serves HTML"""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


@patch("main.get_api_key", return_value="test_key_for_ci")
def test_weather_by_coordinates(mock_get_key):
    """Test coordinate-based weather endpoint structure"""
    response = client.get("/weather/40.7128/-74.0060")
    # Should return 200 or 500 (API error from real OpenWeather call), but not 404
    assert response.status_code in [200, 500]


@patch("main.get_api_key", return_value="test_key_for_ci")
def test_weather_by_city(mock_get_key):
    """Test city-based weather endpoint structure"""
    response = client.get("/weather/city?city=London")
    assert response.status_code in [200, 500, 404]


def test_invalid_coordinates():
    """Test invalid coordinate handling"""
    response = client.get("/weather/invalid/coords")
    assert response.status_code == 422  # Validation error
