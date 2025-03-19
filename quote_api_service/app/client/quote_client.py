from typing import Optional
from lookup_models import Quote
from .base_client import BaseHttpClient


class QuoteClient(BaseHttpClient):
    def __init__(self, base_url: str = "http://localhost:8000"):
        super().__init__(base_url)
        self.api_path = "/api/v1"

    async def get_quote(
        self, quote_number: str, revision_number: int
    ) -> Optional[Quote]:
        """
        Fetch a specific quote by its quote number and revision

        Args:
            quote_number: The quote number (e.g., Q-2024-005)
            revision_number: The revision number (e.g., 4)

        Returns:
            Quote object if found, None otherwise

        Raises:
            httpx.HTTPError: If the request fails
        """
        response = await self._request(
            method="GET",
            path=f"{self.api_path}/quotes/{quote_number}/revisions/{revision_number}",
            headers={"accept": "application/json"},
        )
        return Quote.model_validate(response.json())
