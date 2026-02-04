# Weather FastAPI Dashboard

A REST API backend for active weather reporting, built as a learning project to develop practical DevOps and API integration skills.

## Learning Objectives

This project is designed to practice:

1. **REST API Development** - Building a Python FastAPI backend that integrates with external weather APIs
2. **Version Control** - Managing code changes and workflows with Git
3. **Development Lifecycle** - Following structured development practices from planning to deployment
4. **DevOps Automation** - Implementing CI/CD pipelines to automate testing and deployment

## Tech Stack

- **Backend**: FastAPI (Python)
- **API Integration**: OpenWeatherMap API (or your chosen weather service)
- **Development**: WSL2 Ubuntu and PyCharm Pro
- **Version Control**: Git/GitHub

## Getting Started

### Prerequisites

- Python 3.8+
- pip for dependency management
- API key from weather service provider

### Installation
```bash
# Clone the repository
git clone 
cd weather-fastapi

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your API keys to .env
```

### Running Locally
```bash
uvicorn main:app --reload
```

API will be available at `http://localhost:8000`

## Project Structure
```
weather-fastapi/
├── main.py              # FastAPI application entry point
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variable template
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## API Endpoints

- `GET /weather` - Get current weather data
- (Add your endpoints as you build them)

## Development Workflow

1. Create feature branch from `main`
2. Develop and test locally
3. Commit changes with descriptive messages
4. Push branch and create pull request
5. Review and merge to `main`
6. (Future: Automated deployment via CI/CD)

## Future Enhancements

- [ ] Frontend dashboard
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Docker containerization
- [ ] Automated testing
- [ ] Multiple weather API integrations

## License

Personal learning project
	
