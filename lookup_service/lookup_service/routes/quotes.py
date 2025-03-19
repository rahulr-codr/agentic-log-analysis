from fastapi import APIRouter, Depends
from lookup_service.services.quote_service import QuoteService
from lookup_models import Quote

router = APIRouter()
quote_service = QuoteService()


@router.get("/quotes/{quote_number}/revisions/{revision_number}", response_model=Quote)
async def get_quote(quote_number: str, revision_number: int):
    """
    Get a specific revision of a quote by its quote number and revision number.

    Args:
        quote_number: The unique identifier of the quote
        revision_number: The revision number of the quote

    Returns:
        Quote object if found

    Raises:
        HTTPException: If quote is not found (404)
    """
    return quote_service.get_quote(quote_number, revision_number)
