import json
from pathlib import Path
from typing import Optional, Dict
from fastapi import HTTPException

from lookup_service.models import Contact


class ContactService:
    def __init__(self):
        self.contacts: Dict[str, dict] = {}
        self._load_contacts()

    def _load_contacts(self) -> None:
        """Load contacts from the consolidated JSON file."""
        contacts_file = Path("data/contacts/consolidated_contacts.json")
        if contacts_file.exists():
            with open(contacts_file, "r") as f:
                self.contacts = json.load(f)

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
        if contact_data := self.contacts.get(contact_id):
            return Contact(**contact_data)
        raise HTTPException(status_code=404, detail=f"Contact {contact_id} not found")
