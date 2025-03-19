from typing import Optional
from lookup_models import Contact
from .base_client import BaseHttpClient


class ContactClient(BaseHttpClient):
    def __init__(self, base_url: str = "http://localhost:8000"):
        super().__init__(base_url)
        self.api_path = "/api/v1"

    async def get_contact(self, contact_id: str) -> Optional[Contact]:
        """
        Fetch a specific contact by its ID

        Args:
            contact_id: The unique identifier for the contact

        Returns:
            Contact object if found, None otherwise

        Raises:
            httpx.HTTPError: If the request fails
        """
        response = await self._request(
            method="GET",
            path=f"{self.api_path}/contacts/{contact_id}",
            headers={"accept": "application/json"},
        )
        return Contact.model_validate(response.json())
