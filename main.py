from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import httpx
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import httpx
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Create the FastAPI app
app = FastAPI()

# Add CORS middleware (can remove this now since frontend is on same origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static folder - THIS MUST COME AFTER app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load API key
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


# Serve the frontend HTML at root
@app.get("/")
async def serve_frontend():
    return FileResponse("static/index.html")


# Weather API endpoint
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
     

