FROM python:3.11-slim

# Don't write .pyc files; flush output immediately
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install uv (matches what we used locally)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Install dependencies (frozen = match uv.lock exactly, no-dev = skip pytest/ruff)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copy the rest of the app
COPY . .

# Collect static files (Django admin CSS, etc.)
RUN /app/.venv/bin/python manage.py collectstatic --noinput

EXPOSE 8000

# Use the entrypoint script to run migrations then start gunicorn
CMD ["/app/entrypoint.sh"]