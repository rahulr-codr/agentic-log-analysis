import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import quotes
from app.database.database import engine, Base
from app.config.logging_config import setup_logging

# Setup logging before anything else
setup_logging()
logger = logging.getLogger(__name__)

# Create database tables
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
except Exception as e:
    logger.error("Failed to create database tables", exc_info=True)
    raise

app = FastAPI(
    title="Quote API Service",
    description="A service for managing quotes",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info("CORS middleware configured")

# Include routers
app.include_router(quotes.router, prefix="/api/v1", tags=["quotes"])
logger.info("API routes registered")


@app.get("/")
async def root():
    logger.debug("Root endpoint accessed")
    return {"message": "Welcome to Quote API Service"}


@app.on_event("startup")
async def startup_event():
    logger.info("Application startup", extra={"event": "startup"})


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown", extra={"event": "shutdown"})
