from fastapi import APIRouter, Depends, status, HTTPException, Query
from api.schemas import ContactBase, ContactResponse, ContactUpdate
from api.database.db import get_db, NotUniqueException
from api.database.models import User
from sqlalchemy.orm import Session
from typing import Annotated
from api.services.auth import auth_service

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
                        db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    """
    API route for retrieving a list of contacts for a specific user with specified pagination and additional parameters.

    :param skip: number of contacts to skip
    :type skip: int
    :param limit: max number of contacts to get
    :type limit: int
    :param first_name: an optional first_name to look for contacts by
    :type first_name: str
    :param last_name: an optional last_name to look for contacts by
    :type last_name: str
    :param email: an optional email address to look for contacts by
    :type email: str
    :param bt_within_week: specifies whether birthday people should be found or not
    :type bt_within_week: bool
    :param db: database session
    :type db: Session
    :param current_user: currently authorized user
    :type current_user: User
    :return: list of contacts
    :rtype: List[Contact]
    """

    query_params = {"first_name": first_name, "last_name": last_name,
                    "email": email, "bt_within_week": bt_within_week}
    contacts = await repository_contacts.get_contacts(skip, limit, query_params, current_user, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    """
    API route for retrieving a contact by its ID

    :param contact_id: ID of the contact to retrieve
    :param db: database session
    :type db: Session
    :param current_user: currently authorized user
    :type current_user: User
    :return: the contact by ID if found
    :rtype: Contact | None
    :raises: HTTPException
    """
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactBase, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    API route for creating a new contact for a specific user

    :param body:
    :param db: database session
    :type db: Session
    :param current_user: currently authorized user
    :type current_user: User
    :return: the newly created contact if succeeded
    :rtype: Contact | None
    :raises: HTTPException
    """
    try:
        contact = await repository_contacts.create_contact(body, current_user, db)
    except NotUniqueException as not_unique_error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(not_unique_error))
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactUpdate, contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    API route for updating existing contact for a specific user

    :param body:
    :param contact_id:  ID of the contact to update
    :param db: database session
    :type db: Session
    :param current_user: currently authorized user
    :type current_user: User
    :return: the updated contact
    :rtype: Contact | None
    :raises: HTTPException
    """
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    API route to remove existing contact for a specific user

    :param contact_id:  ID of the contact to delete
    :param db: database session
    :type db: Session
    :param current_user: currently authorized user
    :type current_user: User
    :return: the removed contact if it existed
    :rtype: Contact | None
    :raises: HTTPException
    """
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact
