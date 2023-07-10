from fastapi import APIRouter, Depends, status, HTTPException, Query
from api.schemas import ContactBase, ContactResponse, ContactUpdate
from api.database.db import get_db
from sqlalchemy.orm import Session
from typing import Annotated

from api.repository import contacts as repository_contacts

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/", response_model=list[ContactResponse])
async def read_contacts(skip: int = 0, limit: int = 100,
                        first_name: Annotated[str | None, Query(
                            max_length=100,
                            description="First name search pattern of a contact"
                        )] = None,
                        last_name: Annotated[str | None, Query(
                            max_length=100,
                            description="Last name search pattern of a contact"
                        )] = None,
                        email: Annotated[str | None, Query(
                            max_length=100,
                            description="Email address search pattern of a contact"
                        )] = None,
                        bt_within_week: Annotated[bool | None, Query(
                            description="If true only contacts with birth date within 7 days will be shown."
                        )] = None,
                        db: Session = Depends(get_db)):

    query_params = {"first_name": first_name, "last_name": last_name,
                    "email": email, "bt_within_week": bt_within_week}
    contacts = await repository_contacts.get_contacts(skip, limit, query_params, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactResponse)
async def create_contact(body: ContactBase, db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(body, db)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactUpdate, contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact
