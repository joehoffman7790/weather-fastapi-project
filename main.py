from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
app = FastAPI()

# Add CORS middleware to allow frontend to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


@app.get("/")
async def root():
     return {"message": "Weather Dashboard API"}


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
     

