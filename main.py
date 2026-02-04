from fastapi import FastAPI, HTTPException
import httpx
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
app = FastAPI()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


@app.get("/")
async def root():
     return {"message": "Weather Dashboard API"}


@app.get("/weather/{lat}/{lon}")
async def get_weather(lat: float, lon: float):
     print(f"API_KEY is set: {API_KEY is not None}")
     print(f"API_KEY length: {len(API_KEY) if API_KEY else 0}")
     print(f"Requesting weather for: {lat}, {lon}")

     if not API_KEY:
          raise HTTPException(status_code=500, detail="API key not configured")

     params = {
          "lat": lat,
          "lon": lon,
          "appid": API_KEY,
          "units": "imperial"
     }

     print(f"Request params: {params}")

     async with httpx.AsyncClient() as client:
          try:
               response = await client.get(BASE_URL, params=params)
               print(f"Response status: {response.status_code}")
               print(f"Response text: {response.text[:200]}")
               response.raise_for_status()
               return response.json()
          except httpx.HTTPError as e:
               print(f"Error occurred: {str(e)}")
               raise HTTPException(status_code=500, detail=f"Error fetching weather: {str(e)}")
     

