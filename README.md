# 🌤️ Weather FastAPI Dashboard

A containerized REST API backend for real-time weather reporting, built as a hands-on learning project to develop practical Python, API integration, and DevOps skills.

> **Status:** Mostly complete — core API and Docker setup are functional. CI/CD and cloud deployment are next on the roadmap.

---

## Learning Objectives

This project was built to practice real-world engineering skills in a contained, deployable context:

| Area | What I Practiced |
|---|---|
| **REST API Development** | Building a FastAPI backend integrated with a live external weather API |
| **Containerization** | Packaging the app with Docker for consistent, portable environments |
| **Version Control** | Structured Git workflows — branching, commits, pull requests |
| **DevOps Foundation** | Local dev → Docker → (next) CI/CD pipeline |

---

## Tech Stack

- **Backend:** Python + FastAPI
- **Frontend:** HTML/CSS/JS dashboard (served as static files via FastAPI)
- **Weather Data:** OpenWeatherMap API
- **Containerization:** Docker
- **Dev Environment:** WSL2 (Ubuntu) + PyCharm Pro
- **Version Control:** Git / GitHub

---

## Getting Started

### Prerequisites

- Python 3.8+
- Docker (recommended) or pip for local development
- OpenWeatherMap API key → [get one free here](https://openweathermap.org/api)

### Option 1: Run with Docker (recommended)

```bash
# Clone the repo
git clone <your-repo-url>
cd weather-fastapi

# Copy and configure environment variables
cp .env.example .env
# Edit .env and add your OPENWEATHER_API_KEY

# Build and run the container
docker build -t weather-fastapi .
docker run -p 8000:8000 --env-file .env weather-fastapi
```

### Option 2: Run locally

```bash
# Clone the repo
git clone <your-repo-url>
cd weather-fastapi

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your OPENWEATHER_API_KEY

# Start the dev server
uvicorn main:app --reload
```

API available at: `http://localhost:8000`  
Interactive docs at: `http://localhost:8000/docs`

---

## Project Structure

```
weather-fastapi/
├── main.py              # FastAPI app — routes, API integration, static file serving
├── static/              # Frontend — HTML/CSS/JS dashboard UI
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container build instructions
├── .dockerignore        # Files excluded from Docker build context
├── .env                 # Local environment variables (never committed)
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

---

## API Endpoints

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| `GET` | `/` | Serves the HTML frontend dashboard | None |
| `GET` | `/weather/{lat}/{lon}` | Current weather by coordinates (JSON) | `lat` (float), `lon` (float) |
| `GET` | `/weather/city` | Current weather by city name (JSON) | `city` (required), `state` (optional), `country` (optional) |
| `GET` | `/docs` | Auto-generated interactive API docs (Swagger UI) | None |

### Examples

**Search by coordinates:**
```
GET /weather/40.7128/-74.0060
```

**Search by city:**
```
GET /weather/city?city=London&country=UK
GET /weather/city?city=Austin&state=TX&country=US
GET /weather/city?city=New York&state=NY&country=US
GET /weather/city?city=Paris
```

**Response Format:**
```json
{
  "coord": {"lon": -74.006, "lat": 40.7128},
  "weather": [{"id": 800, "main": "Clear", "description": "clear sky"}],
  "main": {
    "temp": 33.57,
    "feels_like": 24.96,
    "humidity": 66
  },
  "wind": {"speed": 11.5},
  "name": "New York",
  "geocoded_location": {
    "name": "New York",
    "state": "New York",
    "country": "US",
    "lat": 40.7128,
    "lon": -74.006
  }
}
```

Note: `geocoded_location` only appears in city-based search responses.

---

## Development Workflow

```
feature branch → local dev & test → commit → pull request → merge to main
```

1. Branch off `main` for each new feature or fix
2. Develop and test locally (or in Docker)
3. Write descriptive commit messages
4. Open a pull request and review before merging

---

## Roadmap

- [x] FastAPI backend with OpenWeatherMap integration
- [x] Docker containerization
- [x] Basic frontend dashboard (HTML/CSS/JS, served via FastAPI static files)
- [ ] GitHub Actions CI/CD pipeline (lint, test, build)
- [ ] Deploy to Azure (App Service or Container Instances)
- [ ] Infrastructure as Code with Terraform
- [ ] Add forecast endpoint (multi-day weather data)

---

## Key Takeaways

A few things this project helped solidify:

- How FastAPI handles async routes and automatic schema generation via Pydantic
- Why environment variables matter and how `.env` + `.gitignore` protect secrets
- The difference between building an image and running a container, and why that distinction matters for deployment
- How a structured Git workflow scales from solo projects to team environments

---
