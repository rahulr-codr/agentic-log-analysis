from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from lookup_service.routes import quotes, products, contacts
from lookup_service.logging_config import logger

app = FastAPI(
    title="Lookup Service",
    description="Service for looking up quotes, products, and contacts",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(quotes.router, prefix="/api/v1", tags=["quotes"])
app.include_router(products.router, prefix="/api/v1", tags=["products"])
app.include_router(contacts.router, prefix="/api/v1", tags=["contacts"])


@app.on_event("startup")
async def startup_event():
    logger.info("application_startup", message="Starting up the Lookup Service")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("application_shutdown", message="Shutting down the Lookup Service")
