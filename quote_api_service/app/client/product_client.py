from typing import Optional
from lookup_models import Product
from .base_client import BaseHttpClient


class ProductClient(BaseHttpClient):
    def __init__(self, base_url: str = "http://localhost:8000"):
        super().__init__(base_url)
        self.api_path = "/api/v1"

    async def get_product(self, product_id: str) -> Optional[Product]:
        """
        Fetch a specific product by its ID

        Args:
            product_id: The unique identifier for the product

        Returns:
            Product object if found, None otherwise

        Raises:
            httpx.HTTPError: If the request fails
        """
        response = await self._request(
            method="GET",
            path=f"{self.api_path}/products/{product_id}",
            headers={"accept": "application/json"},
        )
        return Product.model_validate(response.json())
