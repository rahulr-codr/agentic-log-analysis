import json
from pathlib import Path
from typing import Optional, Dict
from fastapi import HTTPException

from lookup_service.models import Product
from lookup_service.logging_config import logger


class ProductService:
    def __init__(self):
        self.products: Dict[str, Product] = {}
        self._load_products()
        logger.info(
            "product_service_initialized", message="Product service initialized"
        )

    def _load_products(self):
        products_file = (
            Path(__file__).parent.parent.parent
            / "data"
            / "products"
            / "consolidated_products.json"
        )
        try:
            with open(products_file, "r") as f:
                products_data = json.load(f)
                for product_id, product_data in products_data.items():
                    self.products[product_id] = Product(**product_data)
            logger.info("products_loaded", count=len(self.products))
        except FileNotFoundError:
            logger.warning("products_file_not_found", file_path=str(products_file))
            raise HTTPException(status_code=500, detail="Products data file not found")

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
        logger.info("product_lookup_started", product_id=product_id)
        if product_id not in self.products:
            logger.warning("product_not_found", product_id=product_id)
            raise HTTPException(
                status_code=404, detail=f"Product {product_id} not found"
            )
        logger.info("product_found", product_id=product_id)
        return self.products[product_id]
