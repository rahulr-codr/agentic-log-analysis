from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from lookup_service.routes import quotes, products, contacts

app = FastAPI(
    title="Lookup Service",
    description="Service for looking up quotes, products, and contacts",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(quotes.router, prefix="/api/v1", tags=["quotes"])
app.include_router(products.router, prefix="/api/v1", tags=["products"])
app.include_router(contacts.router, prefix="/api/v1", tags=["contacts"])


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
