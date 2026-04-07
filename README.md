# 🌤️ Weather FastAPI Dashboard

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat&logo=docker&logoColor=white)
![Azure](https://img.shields.io/badge/Azure-Deployed-0078D4?style=flat&logo=microsoftazure&logoColor=white)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?style=flat&logo=githubactions&logoColor=white)
![Terraform](https://img.shields.io/badge/IaC-Terraform-7B42BC?style=flat&logo=terraform&logoColor=white)
![Status](https://img.shields.io/badge/Status-In%20Development-yellow?style=flat)

A full-stack, containerized weather dashboard that delivers real-time weather data using a FastAPI backend and a lightweight HTML/CSS/JavaScript frontend.

This project was built as a hands-on learning exercise to explore the full development-to-cloud lifecycle — from local development and Dockerization to deployment on Azure using Terraform and a CI/CD pipeline powered by GitHub Actions.

The application is currently under active development as I continue refining infrastructure, security, and scalability.

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

## Project Structure

```
weather-fastapi/
├── main.py
├── static
│   ├── index.html
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
├── terraform/
│   ├── providers.tf
│   ├── locals.tf
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── .github/
│   └── workflows/
│       └── ci-cd.yml
└── README.md
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

Every push to the main branch triggers a GitHub Actions workflow that automates the build and deployment process:

```
Push to main
    │
    ├── Lint (ruff / flake8)
    ├── Run tests (pytest)
    ├── Build Docker image
    ├── Push image to Azure Container Registry (ACR)
    └── Deploy container to Azure App Service
```

## Roadmap

- [x] FastAPI backend with OpenWeatherMap integration
- [x] Docker containerization
- [x] Basic frontend dashboard (HTML/CSS/JS, served via FastAPI static files)
- [x] GitHub Actions CI/CD pipeline (lint, test, build, push, deploy)
- [x] Deploy to Azure (App Service + Container Instances)
- [x] Infrastructure as Code with Terraform
- [ ] Add forecast endpoint (multi-day weather data)
- [ ] Improve secret management with Azure Key Vault
- [ ] Monitoring and alerting (Azure Monitor / Application Insights)

---

## Key Takeaways

This project helped me build and reinforce several skills that translate directly to real-world engineering work:

FastAPI & async Python — understanding async route handling, how Pydantic enables validation and schema generation, and serving a static frontend alongside an API
Docker — the difference between building images and running containers, how build context impacts image size, and why containerization improves deployment consistency
CI/CD — building a pipeline that runs linting and validation before deployment, and integrating GitHub Actions with Azure for automated delivery
Infrastructure as Code — provisioning and managing Azure resources with Terraform instead of manual configuration, enabling reproducibility and version control
Security fundamentals — handling environment variables safely, using .env for local development, and understanding how secrets move through deployment workflows
Git workflow — using branching and pull requests to manage changes and maintain a clean, understandable commit history

---

*Built as part of a self-directed learning path toward automation and DevOps engineering, with a focus on understanding how each layer of the stack fits together..*
