import logging
from sqlalchemy.orm import Session
from app.models.quote import Quote
from app.schemas.quote import QuoteCreate, QuoteUpdate

logger = logging.getLogger(__name__)


def get_quote(db: Session, quote_id: int):
    logger.debug("Fetching quote from database", extra={"quote_id": quote_id})
    quote = db.query(Quote).filter(Quote.id == quote_id).first()
    if quote:
        logger.debug("Quote found in database", extra={"quote_id": quote_id})
    else:
        logger.debug("Quote not found in database", extra={"quote_id": quote_id})
    return quote


def get_quotes(db: Session, skip: int = 0, limit: int = 100):
    logger.debug("Fetching quotes from database", extra={"skip": skip, "limit": limit})
    quotes = db.query(Quote).offset(skip).limit(limit).all()
    logger.debug("Retrieved quotes from database", extra={"count": len(quotes)})
    return quotes


def create_quote(db: Session, quote: QuoteCreate):
    logger.debug(
        "Creating new quote in database", extra={"quote_text": quote.text[:50] + "..."}
    )
    try:
        db_quote = Quote(**quote.model_dump())
        db.add(db_quote)
        db.commit()
        db.refresh(db_quote)
        logger.debug(
            "Successfully created quote in database", extra={"quote_id": db_quote.id}
        )
        return db_quote
    except Exception as e:
        logger.error("Failed to create quote in database", exc_info=True)
        db.rollback()
        raise


def update_quote(db: Session, quote_id: int, quote: QuoteUpdate):
    logger.debug("Updating quote in database", extra={"quote_id": quote_id})
    try:
        db_quote = get_quote(db, quote_id)
        if not db_quote:
            logger.debug("Quote not found for update", extra={"quote_id": quote_id})
            return None

        update_data = quote.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_quote, key, value)

        db.commit()
        db.refresh(db_quote)
        logger.debug(
            "Successfully updated quote in database", extra={"quote_id": quote_id}
        )
        return db_quote
    except Exception as e:
        logger.error(
            "Failed to update quote in database",
            extra={"quote_id": quote_id},
            exc_info=True,
        )
        db.rollback()
        raise


def delete_quote(db: Session, quote_id: int):
    logger.debug("Deleting quote from database", extra={"quote_id": quote_id})
    try:
        db_quote = get_quote(db, quote_id)
        if not db_quote:
            logger.debug("Quote not found for deletion", extra={"quote_id": quote_id})
            return None

        db.delete(db_quote)
        db.commit()
        logger.debug(
            "Successfully deleted quote from database", extra={"quote_id": quote_id}
        )
        return db_quote
    except Exception as e:
        logger.error(
            "Failed to delete quote from database",
            extra={"quote_id": quote_id},
            exc_info=True,
        )
        db.rollback()
        raise
