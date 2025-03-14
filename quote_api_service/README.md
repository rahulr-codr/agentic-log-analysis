# Quote API Service

A FastAPI-based service for managing quotes with OpenTelemetry integration for observability.

## Features

- FastAPI REST API
- SQLAlchemy ORM with SQLite database
- OpenTelemetry integration for:
  - Distributed tracing
  - Metrics collection
  - Log aggregation
- Docker support
- Poetry for dependency management

## Prerequisites

- Python 3.9 or higher
- Poetry for dependency management
- Docker and Docker Compose (optional, for containerized deployment)

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd quote-api-service
```

2. Install Poetry if you haven't already:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. Install dependencies using Poetry:
```bash
poetry install
```

4. Create a `.env` file in the root directory with the following variables:
```env
DATABASE_URL=sqlite:///./quotes.db
LOG_LEVEL=INFO
OTEL_SERVICE_NAME=quote_api_service
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317  # For local development
```

## Running the Application

### Local Development

1. Activate the Poetry environment:
```bash
poetry shell
```

2. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Using Docker

1. Build and start the containers:
```bash
docker compose up --build
```

2. Stop the containers:
```bash
docker compose down
```

## API Documentation

Once the application is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## OpenTelemetry Integration

The application is configured to send telemetry data to an OpenTelemetry collector. Make sure you have the following services running:

- OpenTelemetry Collector
- Loki (for logs)
- Grafana (for visualization)
- Tempo (for traces)
- Mimir (for metrics)

The default configuration assumes these services are running locally. Update the `OTEL_EXPORTER_OTLP_ENDPOINT` in your `.env` file if your collector is running elsewhere.

## Development

### Project Structure

```
quote-api-service/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   ├── config/
│   ├── core/
│   ├── db/
│   ├── models/
│   └── schemas/
├── tests/
├── alembic/
├── .env
├── docker-compose.yml
├── Dockerfile
├── main.py
├── pyproject.toml
└── README.md
```

### Running Tests

```bash
poetry run pytest
```

## License

[Your License Here]
