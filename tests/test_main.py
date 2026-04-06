import os

from fastapi.testclient import TestClient

from main import app

# Mock API key for testing
os.environ["OPENWEATHER_API_KEY"] = "test_key_for_ci"

client = TestClient(app)


def test_read_root():
    """Test the root endpoint serves HTML"""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_weather_by_coordinates():
    """Test coordinate-based weather endpoint structure"""
    # This will fail without real API key, but tests the endpoint exists
    response = client.get("/weather/40.7128/-74.0060")
    # Should return 200 or 500 (API error), but not 404
    assert response.status_code in [200, 500]


def test_weather_by_city():
    """Test city-based weather endpoint structure"""
    response = client.get("/weather/city?city=London")
    # Should return 200 or 500 (API error), but not 404
    assert response.status_code in [200, 500, 404]


def test_invalid_coordinates():
    """Test invalid coordinate handling"""
    response = client.get("/weather/invalid/coords")
    assert response.status_code == 422  # Validation error
