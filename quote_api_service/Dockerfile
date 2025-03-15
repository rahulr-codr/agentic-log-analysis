FROM python:3.13-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
COPY . /app

# Install the application dependencies.
WORKDIR /app
RUN uv sync --frozen --no-cache

ENV PYTHONUNBUFFERED=1

# Run the application.
CMD ["/app/.venv/bin/opentelemetry-instrument", "/app/.venv/bin/uvicorn", "main:app",  "--host", "0.0.0.0", "--port", "8000", "--no-access-log", "--log-level", "info", "--root-path", "/quotes"]
