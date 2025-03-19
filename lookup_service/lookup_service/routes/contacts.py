from fastapi import APIRouter
from lookup_service.services.contact_service import ContactService
from lookup_models import Contact

router = APIRouter()
contact_service = ContactService()


@router.get("/contacts/{contact_id}", response_model=Contact)
async def get_contact(contact_id: str):
    """
    Get a contact by its ID.

    Args:
        contact_id: The unique identifier of the contact

    Returns:
        Contact object if found

    Raises:
        HTTPException: If contact is not found (404)
    """
    return contact_service.get_contact(contact_id)
