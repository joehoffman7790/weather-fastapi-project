from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import httpx
import os

# Create the FastAPI app
app = FastAPI()

# Mount the static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load API key from environment
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


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
     

