import json
from pathlib import Path
from typing import Optional, Dict
from fastapi import HTTPException

from lookup_models import Quote
from lookup_service.logging_config import logger


class QuoteService:
    def __init__(self):
        self.quotes: Dict[str, Quote] = {}
        self._load_quotes()
        logger.info("quote_service_initialized", message="Quote service initialized")

    def _load_quotes(self):
        quotes_file = (
            Path(__file__).parent.parent.parent
            / "data"
            / "quotes"
            / "consolidated_quotes.json"
        )
        try:
            with open(quotes_file, "r") as f:
                quotes_data = json.load(f)
                for quote_number, quote_data in quotes_data.items():
                    self.quotes[quote_number] = Quote(**quote_data)
            logger.info("quotes_loaded", count=len(self.quotes))
        except FileNotFoundError:
            logger.warning("quotes_file_not_found", file_path=str(quotes_file))
            raise HTTPException(status_code=500, detail="Quotes data file not found")

    def get_quote(self, quote_number: str, revision_number: int) -> Quote:
        logger.info(
            "quote_lookup_started",
            quote_number=quote_number,
            revision_number=revision_number,
        )
        id = f"{quote_number}__{revision_number}"
        if id not in self.quotes:
            logger.warning("quote_not_found", quote_number=quote_number)
            raise HTTPException(
                status_code=404, detail=f"Quote {quote_number} not found"
            )
        logger.info("quote_found", quote_number=quote_number)
        return self.quotes[id]
