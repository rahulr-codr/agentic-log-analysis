# Quote API Service

A FastAPI-based service for managing and retrieving quotes, with OpenTelemetry instrumentation and structured logging.

## Features

- FastAPI REST API
- Structured logging with `structlog`
- OpenTelemetry instrumentation
- JSON formatted logs with trace context

## Prerequisites

- Python 3.8+
- pip

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd quote-api-service
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Local Development

Run the application with OpenTelemetry instrumentation:

```bash
OTEL_SERVICE_NAME=quote-api-service \
OTEL_TRACES_EXPORTER=otlp \
OTEL_METRICS_EXPORTER=otlp \
OTEL_LOGS_EXPORTER=otlp \
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317 \
opentelemetry-instrument python main.py
```

The API will be available at:
- http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Docker

1. Build the Docker image:
```bash
docker build -t quote-api-service .
```

2. Run the container:
```bash
docker run -p 8000:8000 quote-api-service
```

## API Endpoints

- `GET /`: Root endpoint that returns a welcome message

## Observability

### Logging

The application uses structured logging with `structlog`, configured to output JSON-formatted logs with the following information:
- Timestamp
- Log level
- Event message
- OpenTelemetry trace and span IDs
- Additional context

Example log output:
```json
{
    "event": "root_endpoint_called",
    "level": "info",
    "timestamp": "2024-03-15T03:26:22.385681Z",
    "trace_id": "8a1c9469e01578e86cf4d0a07892943c",
    "span_id": "b7ad6b7169203331",
    "path": "/"
}
```

### OpenTelemetry

The application is instrumented with OpenTelemetry for:
- Distributed tracing
- Metrics
- Logs

Configure the OpenTelemetry endpoint using the `OTEL_EXPORTER_OTLP_ENDPOINT` environment variable.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Add your license here]
