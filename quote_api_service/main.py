from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database.database import engine, Base
from app.routes.quotes import router as quotes_router
from app.config.telemetry_config import setup_telemetry
from app.config.logging_config import setup_logging

import uuid
from fastapi import Request
from app.config.common import CorrelationIdFilter, correlation_id_ctx
from opentelemetry.sdk.resources import Resource

resource = Resource.create(
    {
        "service.name": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,  # e.g., "production", "staging"
        "version": settings.VERSION,
        # ... other attributes
    }
)

logger = setup_logging(resource)


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["X-Correlation-ID", "*"],  # Explicitly allow correlation ID header
)

# Set up correlation ID middleware (after CORS)


# # Attach the filter to the Uvicorn access logger
# access_logger = logging.getLogger("uvicorn.access")
# access_logger.addFilter(CorrelationIdFilter())

app = FastAPI()


# Middleware to extract or generate the correlation id and set it in the context variable
@app.middleware("http")
async def add_correlation_id(request: Request, call_next):
    # Try to extract correlation id from the request header (or generate a new one)
    cid = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    correlation_id_ctx.set(cid)
    response = await call_next(request)
    return response


# app.add_middleware(CorrelationMiddleware)

# Create database tables
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
except Exception as e:
    logger.error("Failed to create database tables", exc_info=True)
    raise

# Set up OpenTelemetry - must be done before including routers
tracer = setup_telemetry(app, engine)

# Include API router
app.include_router(quotes_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    with tracer.start_as_current_span("root_endpoint") as span:
        span.set_attribute("endpoint", "/")
        logger.info("Root endpoint called")
        return {"message": "Welcome to Quote API Service"}
