import json
from pathlib import Path
from typing import Optional, Dict
from fastapi import HTTPException

from lookup_service.models import Quote


class QuoteService:
    def __init__(self):
        self.quotes: Dict[str, dict] = {}
        self._load_quotes()

    def _load_quotes(self) -> None:
        """Load quotes from the consolidated JSON file."""
        quotes_file = Path("data/quotes/consolidated_quotes.json")
        if quotes_file.exists():
            with open(quotes_file, "r") as f:
                self.quotes = json.load(f)

    def get_quote(self, quote_number: str, revision_number: int) -> Quote:
        """
        Retrieve a specific revision of a quote by its quote number and revision number.

        Args:
            quote_number: The unique identifier of the quote
            revision_number: The revision number of the quote

        Returns:
            Quote object if found

        Raises:
            HTTPException: If quote is not found (404)
        """
        quote_key = f"{quote_number}__{revision_number}"
        if quote_data := self.quotes.get(quote_key):
            return Quote(**quote_data)
        raise HTTPException(
            status_code=404,
            detail=f"Quote {quote_number} revision {revision_number} not found",
        )
