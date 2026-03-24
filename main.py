from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import httpx
import os
from typing import Optional

# Create the FastAPI app
app = FastAPI()

# Mount the static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load API key from environment
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
GEOCODING_URL = "http://api.openweathermap.org/geo/1.0/direct"


async def geocode_location(city: str, state: Optional[str] = None, country: Optional[str] = None) -> dict:
    """Convert city name to coordinates using OpenWeather Geocoding API"""

    # Build query string
    query_parts = [city]
    if state:
        query_parts.append(state)
    if country:
        query_parts.append(country)

    query = ",".join(query_parts)

    params = {
        "q": query,
        "limit": 1,
        "appid": API_KEY
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(GEOCODING_URL, params=params)
            response.raise_for_status()
            results = response.json()

            if not results:
                raise HTTPException(status_code=404, detail=f"Location '{query}' not found")

            location = results[0]
            return {
                "name": location.get("name"),
                "state": location.get("state"),
                "country": location.get("country"),
                "lat": location["lat"],
                "lon": location["lon"]
            }
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=f"Error geocoding location: {str(e)}")


@app.get("/")
async def serve_frontend():
    """Serve the frontend HTML"""
    return FileResponse("static/index.html")


@app.get("/weather/{lat}/{lon}")
async def get_weather(lat: float, lon: float):
    """Get current weather data for specific coordinates"""

    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key not configured")

    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "imperial"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(BASE_URL, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=f"Error fetching weather: {str(e)}")


@app.get("/weather/city/")
async def get_weather_by_city(
        city: str,
        state: Optional[str] = None,
        country: Optional[str] = None
):
    """Get weather by city name with optional state and country filters

    Examples:
    - /weather/city/London?country=UK
    - /weather/city/Austin?state=TX&country=US
    - /weather/city/Paris
    """

    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key not configured")

    # Geocode the location
    location = await geocode_location(city, state, country)

    # Get weather for those coordinates
    params = {
        "lat": location["lat"],
        "lon": location["lon"],
        "appid": API_KEY,
        "units": "imperial"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(BASE_URL, params=params)
            response.raise_for_status()
            weather_data = response.json()

            # Add geocoding info to response
            weather_data["geocoded_location"] = location

            return weather_data
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=f"Error fetching weather: {str(e)}")





































# @app.get("/")
# async def serve_frontend():
#     """Serve the frontend HTML"""
#     return FileResponse("static/index.html")
#
#
# @app.get("/weather/{lat}/{lon}")
# async def get_weather(lat: float, lon: float):
#     """Get current weather data for specific coordinates"""
#
#     if not API_KEY:
#         raise HTTPException(status_code=500, detail="API key not configured")
#
#     params = {
#         "lat": lat,
#         "lon": lon,
#         "appid": API_KEY,
#         "units": "imperial"
#     }
#
#     async with httpx.AsyncClient() as client:
#         try:
#             response = await client.get(BASE_URL, params=params)
#             response.raise_for_status()
#             return response.json()
#         except httpx.HTTPError as e:
#             raise HTTPException(status_code=500, detail=f"Error fetching weather: {str(e)}")
#

