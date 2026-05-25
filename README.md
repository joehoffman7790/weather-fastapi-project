# 🌤️ Weather Dashboard

![Python](https://img.shields.io/badge/Python-3.13.12-3776AB?style=flat&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.x-092E20?style=flat&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-REST_Framework-ff1709?style=flat&logo=django&logoColor=white)
![HTMX](https://img.shields.io/badge/HTMX-Frontend-3D72D7?style=flat)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat&logo=docker&logoColor=white)
![Azure](https://img.shields.io/badge/Azure-Deployed-0078D4?style=flat&logo=microsoftazure&logoColor=white)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF?style=flat&logo=githubactions&logoColor=white)
![Terraform](https://img.shields.io/badge/IaC-Terraform-7B42BC?style=flat&logo=terraform&logoColor=white)
![Status](https://img.shields.io/badge/Status-In_Development-yellow?style=flat)

A full-stack weather dashboard in progress, being built with Django REST Framework to serve a dynamic frontend (Django templates + HTMX) and REST API from a single application. Will display current conditions and a 5-day forecast using OpenWeatherMap data.

This project is a deliberate rewrite of an earlier FastAPI version, undertaken to learn Django's architecture, DRF, PostgreSQL, and class-based design patterns.

---

## Architecture Overview
```
┌──────────────────────────────────────────────────────────┐
│                    GitHub Actions CI/CD                  │
│        Lint → Test → Build Docker Image → Push → Deploy  │
└────────────────────────┬─────────────────────────────────┘
                         │
          ┌──────────────▼──────────────┐
          │      Azure App Service      │
          └──────────────┬──────────────┘
                         │
          ┌──────────────▼──────────────┐
          │      Django Application     │
          │  ┌────────────────────────┐ │
          │  │  Templates + HTMX UI   │ │
          │  └────────────────────────┘ │
          │  ┌────────────────────────┐ │
          │  │   DRF REST Endpoints   │ │
          │  └────────────┬───────────┘ │
          └───────────────┼─────────────┘
                          │
          ┌───────────────▼─────────────┐
          │     OpenWeatherMap API      │
          └─────────────────────────────┘
                          │
          ┌───────────────▼─────────────┐
          │  Azure Database (PostgreSQL)│
          └─────────────────────────────┘
```

## Tech Stack

| Layer | Technology                                                 |
|---|------------------------------------------------------------|
| **Backend** | Python 3.13.12 + Django + Django REST Framework            |
| **Frontend** | Django Templates + HTMX                                    |
| **Database** | PostgreSQL (Azure Database for PostgreSQL Flexible Server) |
| **Weather Data** | OpenWeatherMap API (current + 3-hour forecast)             |
| **Containerization** | Docker                                                     |
| **Cloud Deployment** | Azure App Service + Azure Container Registry               |
| **CI/CD** | GitHub Actions (lint → test → build → push → deploy)       |
| **Infrastructure as Code** | Terraform                                                  |
| **Secret Management** | Azure Key Vault (managed identity)                         |
| **Package Management** | uv + pyproject.toml                                        |
| **Linting** | ruff                                                       |
| **Dev Environment** | macOS + PyCharm Pro                                        |
| **Version Control** | Git / GitHub                                               |

---

```
weather-django/
├── manage.py
├── pyproject.toml
├── Dockerfile
├── .dockerignore
├── .gitignore
├── weather/                  # Django app
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── templates/
│       └── weather/
│           └── index.html
├── config/                   # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── tests/
│   ├── __init__.py
│   └── test_views.py
├── terraform/
│   ├── providers.tf
│   ├── locals.tf
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── key_vault.tf
├── .github/
│   └── workflows/
│       └── ci-cd.yml
└── README.md
```

> **Note:** Structure will update as the rewrite progresses.

---

## API Endpoints

| Method | Endpoint | Description                                | Parameters |
|--------|----------|--------------------------------------------|------------|
| `GET` | `/` | Serves the frontend dashboard              | None |
| `GET` | `/api/weather/current/` | Current weather by coordinates             | `lat` (float), `lon` (float) |
| `GET` | `/api/weather/forecast/` | 5-day forecast aggregated from 3-hour data | `lat` (float), `lon` (float) |
| `GET` | `/api/docs/` | Browsable API (DRF)                        | None |

### Response Format — Current Weather

```json
{
  "location": "New York, NY, US",
  "temperature": 33.6,
  "feels_like": 25.0,
  "humidity": 66,
  "description": "clear sky",
  "wind_speed": 11.5
}
```

### Response Format — 5-Day Forecast

```json
[
  {
    "date": "2025-06-01",
    "high": 35.2,
    "low": 22.1,
    "description": "partly cloudy"
  },
  ...
]
```

---

## CI/CD Pipeline

Every push to `main` triggers a GitHub Actions workflow:

```
Push to main
    │
    ├── Lint (ruff)
    ├── Run tests (pytest)
    ├── Build Docker image
    ├── Push image to Azure Container Registry (ACR)
    └── Deploy container to Azure App Service
```

## Roadmap

- [ ] Bootstrap project with `uv` and Django
- [ ] Configure DRF and PostgreSQL
- [ ] Current weather endpoint
- [ ] 5-day forecast endpoint (aggregate 3-hour OWM data → daily high/low)
- [ ] Django templates + HTMX frontend
- [ ] Docker containerization
- [ ] Terraform infrastructure (App Service, ACR, PostgreSQL, Key Vault)
- [ ] GitHub Actions CI/CD pipeline
- [ ] Custom subdomain + SSL (Azure)

---

## Key Takeaways

This rewrite builds on the foundation of the original FastAPI project and adds:

**Django & DRF** — learning how Django's class-based architecture organises a project, how DRF serializers map models to API responses, and how a single Django app can serve both a UI and a REST API

**PostgreSQL** — shifting from a stateless API (where every request hits OpenWeatherMap directly) to a relational database backed by Azure Database for PostgreSQL Flexible Server, provisioned and managed through Terraform

**HTMX** — adding frontend interactivity without a JavaScript framework, using server-rendered HTML fragments

***OOP in practice** — a deliberate step up from writing standalone scripts and procedural automation, using Django's class-based views and DRF generic views as a real-world introduction to object-oriented design patterns

**uv** — modern Python packaging and dependency management as a replacement for pip/requirements.txt

---
