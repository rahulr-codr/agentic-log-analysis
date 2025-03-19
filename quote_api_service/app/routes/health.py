from fastapi import APIRouter, status
from pydantic import BaseModel
from typing import Dict

router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    version: str
    details: Dict[str, str]


@router.get("", response_model=HealthResponse)
async def health_check():
    """Check the health of the service"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "details": {"database": "connected", "cache": "connected"},
    }
