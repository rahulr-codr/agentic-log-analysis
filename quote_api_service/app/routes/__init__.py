# app/routes/__init__.py
from fastapi import APIRouter
from app.routes.quotes import router as quotes_router
from app.routes.health import router as health_router

router = APIRouter()
router.include_router(quotes_router, prefix="/quotes", tags=["quotes"])
router.include_router(health_router, prefix="/health", tags=["health"])
