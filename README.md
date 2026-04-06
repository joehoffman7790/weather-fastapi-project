# 🌤️ Weather FastAPI Dashboard

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat&logo=docker&logoColor=white)
![Azure](https://img.shields.io/badge/Azure-Deployed-0078D4?style=flat&logo=microsoftazure&logoColor=white)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?style=flat&logo=githubactions&logoColor=white)
![Terraform](https://img.shields.io/badge/IaC-Terraform-7B42BC?style=flat&logo=terraform&logoColor=white)
![Status](https://img.shields.io/badge/Status-Production-brightgreen?style=flat)

A full-stack, containerized weather dashboard delivering real-time weather data via a FastAPI backend and a lightweight HTML/CSS/JS frontend. Built end-to-end as a hands-on learning project — from local development to Dockerized deployment on Azure, with a fully automated CI/CD pipeline managed through GitHub Actions and infrastructure provisioned via Terraform.

---

## Architecture Overview

```
┌──────────────────────────────────────────────────────────┐
│                    GitHub Actions CI/CD                   │
│   Lint → Test → Build Docker Image → Push → Deploy       │
└────────────────────────┬─────────────────────────────────┘
                         │
          ┌──────────────▼──────────────┐
          │        Azure Container      │
          │   App Service / Instances   │
          └──────────────┬──────────────┘
                         │
          ┌──────────────▼──────────────┐
          │     FastAPI Application     │
          │  ┌────────────────────────┐ │
          │  │  Static Frontend (UI)  │ │
          │  └────────────────────────┘ │
          │  ┌────────────────────────┐ │
          │  │   REST API Endpoints   │ │
          │  └────────────┬───────────┘ │
          └───────────────┼─────────────┘
                          │
          ┌───────────────▼─────────────┐
          │     OpenWeatherMap API      │
          └─────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.11 + FastAPI |
| **Frontend** | HTML / CSS / JavaScript (served via FastAPI static files) |
| **Weather Data** | OpenWeatherMap API |
| **Containerization** | Docker |
| **Cloud Deployment** | Azure App Service + Azure Container Instances |
| **CI/CD** | GitHub Actions (lint → test → build → push → deploy) |
| **Infrastructure as Code** | Terraform |
| **Dev Environment** | WSL2 (Ubuntu) + PyCharm Pro |
| **Version Control** | Git / GitHub |

---

## Getting Started

### Prerequisites

- Python 3.8+
- Docker (recommended for local parity with production)
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
├── .env.example         # Environment variable template
├── .gitignore           # Git ignore rules
├── terraform/           # Azure infrastructure definitions
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── .github/
│   └── workflows/
│       └── ci-cd.yml    # GitHub Actions pipeline
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

> `geocoded_location` only appears in city-based search responses.

---

## CI/CD Pipeline

Every push to `main` or `master` triggers the full GitHub Actions pipeline:

```
Push to main or master
    │
    ├── Lint (flake8 / ruff)
    ├── Test (pytest)
    ├── Build Docker image
    ├── Push to Azure Container Registry
    └── Deploy to Azure (App Service + Container Instances)
```

Infrastructure is defined and version-controlled in Terraform under `/terraform`, enabling reproducible, auditable Azure provisioning.

---

## Development Workflow

```
feature branch → local dev & test → commit → pull request → merge to main → CI/CD auto-deploys
```

1. Branch off `main` for each new feature or fix
2. Develop and test locally (or in Docker)
3. Write descriptive commit messages
4. Open a pull request and review before merging
5. Merge triggers the GitHub Actions pipeline automatically

---

## Roadmap

- [x] FastAPI backend with OpenWeatherMap integration
- [x] Docker containerization
- [x] Basic frontend dashboard (HTML/CSS/JS, served via FastAPI static files)
- [x] GitHub Actions CI/CD pipeline (lint, test, build, push, deploy)
- [x] Deploy to Azure (App Service + Container Instances)
- [x] Infrastructure as Code with Terraform
- [ ] Add forecast endpoint (multi-day weather data)
- [ ] Unit test coverage expansion
- [ ] Monitoring and alerting (Azure Monitor / Application Insights)

---

## Key Takeaways

Building this end-to-end sharpened several skills that translate directly to production engineering work:

- **FastAPI & async Python** — how async routes work, how Pydantic drives automatic schema generation and validation, and how to serve a static frontend alongside a REST API from a single application
- **Docker** — the distinction between building an image and running a container, how build context affects image size, and why containerization matters for deployment consistency
- **CI/CD** — designing a pipeline that enforces code quality (lint, test) before any artifact is built or deployed, and how GitHub Actions integrates with Azure for automated delivery
- **Infrastructure as Code** — provisioning cloud resources with Terraform rather than manually through the portal, making infrastructure reproducible and version-controlled
- **Security fundamentals** — environment variables, `.env` + `.gitignore` patterns, and how secrets flow safely from local dev through CI/CD to production
- **Git workflow** — structured branching, pull requests, and how a clean commit history supports both solo and team development

---

*Built as part of a self-directed learning path toward automation engineering — focused on understanding the "why" behind every layer of the stack.*
