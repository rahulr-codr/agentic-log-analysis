import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.schemas.quote import Quote, QuoteCreate, QuoteUpdate
from app.services.quote_service import (
    get_quote,
    get_quotes,
    create_quote,
    update_quote,
    delete_quote,
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/quotes/", response_model=List[Quote])
def read_quotes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.debug("Fetching quotes", extra={"skip": skip, "limit": limit})
    try:
        quotes = get_quotes(db, skip=skip, limit=limit)
        logger.info("Successfully retrieved quotes", extra={"count": len(quotes)})
        return quotes
    except Exception as e:
        logger.error("Failed to retrieve quotes", exc_info=True)
        raise


@router.post("/quotes/", response_model=Quote)
def create_new_quote(quote: QuoteCreate, db: Session = Depends(get_db)):
    logger.info("Creating new quote", extra={"quote_text": quote.text[:50] + "..."})
    try:
        new_quote = create_quote(db=db, quote=quote)
        logger.info("Successfully created quote", extra={"quote_id": new_quote.id})
        return new_quote
    except Exception as e:
        logger.error("Failed to create quote", exc_info=True)
        raise


@router.get("/quotes/{quote_id}", response_model=Quote)
def read_quote(quote_id: int, db: Session = Depends(get_db)):
    logger.debug("Fetching quote", extra={"quote_id": quote_id})
    try:
        db_quote = get_quote(db, quote_id=quote_id)
        if db_quote is None:
            logger.warning("Quote not found", extra={"quote_id": quote_id})
            raise HTTPException(status_code=404, detail="Quote not found")
        logger.info("Successfully retrieved quote", extra={"quote_id": quote_id})
        return db_quote
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Failed to retrieve quote", extra={"quote_id": quote_id}, exc_info=True
        )
        raise


@router.put("/quotes/{quote_id}", response_model=Quote)
def update_existing_quote(
    quote_id: int, quote: QuoteUpdate, db: Session = Depends(get_db)
):
    logger.info("Updating quote", extra={"quote_id": quote_id})
    try:
        db_quote = update_quote(db, quote_id=quote_id, quote=quote)
        if db_quote is None:
            logger.warning("Quote not found for update", extra={"quote_id": quote_id})
            raise HTTPException(status_code=404, detail="Quote not found")
        logger.info("Successfully updated quote", extra={"quote_id": quote_id})
        return db_quote
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Failed to update quote", extra={"quote_id": quote_id}, exc_info=True
        )
        raise


@router.delete("/quotes/{quote_id}", response_model=Quote)
def delete_existing_quote(quote_id: int, db: Session = Depends(get_db)):
    logger.info("Deleting quote", extra={"quote_id": quote_id})
    try:
        db_quote = delete_quote(db, quote_id=quote_id)
        if db_quote is None:
            logger.warning("Quote not found for deletion", extra={"quote_id": quote_id})
            raise HTTPException(status_code=404, detail="Quote not found")
        logger.info("Successfully deleted quote", extra={"quote_id": quote_id})
        return db_quote
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Failed to delete quote", extra={"quote_id": quote_id}, exc_info=True
        )
        raise
