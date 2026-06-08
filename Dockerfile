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

EXPOSE 8000

# Start gunicorn directly — no entrypoint script
CMD ["/app/.venv/bin/gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-"]