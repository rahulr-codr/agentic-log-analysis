from fastapi import APIRouter, HTTPException, Path, Body, status, Depends
from typing import List
from lookup_models import (
    EnrichedQuote,
    Quote,
    QuoteCreate,
    QuoteUpdate,
    QuotePublish,
    QuoteCancel,
    QuoteApprove,
)
from ..service.quote_service import QuoteService
import structlog

router = APIRouter()
logger = structlog.get_logger()


async def get_quote_service():
    return QuoteService()


@router.post(
    "/create", status_code=status.HTTP_201_CREATED, response_model=EnrichedQuote
)
async def create_quote(
    quote_create: QuoteCreate, quote_service: QuoteService = Depends(get_quote_service)
):
    """Create a new quote"""
    return await quote_service.create_agreement("Q-2024-005", 4)  # Example lookup


@router.put("/update", response_model=Quote)
async def update_quote(
    quote_update: QuoteUpdate = Body(...),
):
    """Update an existing quote"""
    return {
        "message": "Quote updated successfully",
    }


@router.post("/publish", response_model=Quote)
async def publish_quote(
    quote_update: QuotePublish = Body(...),
):
    """Publish a quote"""
    return {
        "message": "Quote published successfully",
    }


@router.post("/cancel", response_model=Quote)
async def cancel_quote(
    quote_update: QuoteCancel = Body(...),
):
    """Cancel a quote"""
    return {
        "message": "Quote cancelled successfully",
    }


@router.post("/approve", response_model=Quote)
async def approve_quote(
    quote_update: QuoteApprove = Body(...),
):
    """Approve a quote"""
    return {
        "message": "Quote approved successfully",
    }
