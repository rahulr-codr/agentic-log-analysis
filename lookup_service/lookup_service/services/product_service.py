import json
from pathlib import Path
from typing import Optional, Dict
from fastapi import HTTPException

from lookup_service.models import Product


class ProductService:
    def __init__(self):
        self.products: Dict[str, dict] = {}
        self._load_products()

    def _load_products(self) -> None:
        """Load products from the consolidated JSON file."""
        products_file = Path("data/products/consolidated_products.json")
        if products_file.exists():
            with open(products_file, "r") as f:
                self.products = json.load(f)

    def get_product(self, product_id: str) -> Product:
        """
        Retrieve a product by its ID.

        Args:
            product_id: The unique identifier of the product

        Returns:
            Product object if found

        Raises:
            HTTPException: If product is not found (404)
        """
        if product_data := self.products.get(product_id):
            return Product(**product_data)
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
