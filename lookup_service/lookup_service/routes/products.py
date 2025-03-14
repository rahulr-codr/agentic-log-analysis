from fastapi import APIRouter, HTTPException
from lookup_service.services.product_service import ProductService
from lookup_service.models import Product

router = APIRouter()
product_service = ProductService()


@router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    """
    Get a product by its ID.

    Args:
        product_id: The unique identifier of the product

    Returns:
        Product object if found

    Raises:
        HTTPException: If product is not found (404)
    """
    return product_service.get_product(product_id)
