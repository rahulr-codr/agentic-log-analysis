import json
from pathlib import Path
from typing import Optional, Dict
from fastapi import HTTPException

from lookup_service.models import Contact
from lookup_service.logging_config import logger


class ContactService:
    def __init__(self):
        self.contacts: Dict[str, Contact] = {}
        self._load_contacts()
        logger.info(
            "contact_service_initialized", message="Contact service initialized"
        )

    def _load_contacts(self):
        contacts_file = (
            Path(__file__).parent.parent.parent
            / "data"
            / "contacts"
            / "consolidated_contacts.json"
        )
        try:
            with open(contacts_file, "r") as f:
                contacts_data = json.load(f)
                for contact_id, contact_data in contacts_data.items():
                    self.contacts[contact_id] = Contact(**contact_data)
            logger.info("contacts_loaded", count=len(self.contacts))
        except FileNotFoundError:
            logger.warning("contacts_file_not_found", file_path=str(contacts_file))
            raise HTTPException(status_code=500, detail="Contacts data file not found")

    def get_contact(self, contact_id: str) -> Contact:
        """
        Retrieve a contact by its ID.

        Args:
            contact_id: The unique identifier of the contact

        Returns:
            Contact object if found

        Raises:
            HTTPException: If contact is not found (404)
        """
        logger.info("contact_lookup_started", contact_id=contact_id)
        if contact_id not in self.contacts:
            logger.warning("contact_not_found", contact_id=contact_id)
            raise HTTPException(
                status_code=404, detail=f"Contact {contact_id} not found"
            )
        logger.info("contact_found", contact_id=contact_id)
        return self.contacts[contact_id]
