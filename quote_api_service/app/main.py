from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api_v1.api import api_router
from app.core.config import settings
from app.config.telemetry_config import setup_telemetry
from app.middleware.correlation import CorrelationMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    version="1.0.0",
)

# Add correlation middleware first
app.add_middleware(CorrelationMiddleware)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up telemetry after middleware
tracer = setup_telemetry(app, None)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)
