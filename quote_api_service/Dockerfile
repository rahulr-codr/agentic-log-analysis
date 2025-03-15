FROM python:3.13-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
COPY . /app

# Install the application dependencies.
WORKDIR /app
RUN uv sync --frozen --no-cache

# Set environment variables for OpenTelemetry
ENV OTEL_SERVICE_NAME=quote-api-service
ENV OTEL_TRACES_EXPORTER=otlp
ENV OTEL_METRICS_EXPORTER=otlp
ENV OTEL_LOGS_EXPORTER=otlp
ENV OTEL_EXPORTER_OTLP_PROTOCOL=grpc
ENV OTEL_LOG_LEVEL=debug
ENV OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
ENV OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
ENV PYTHONUNBUFFERED=1

# Run the application.
CMD ["/app/.venv/bin/opentelemetry-instrument", "/app/.venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--no-access-log", "--log-level", "info"]
