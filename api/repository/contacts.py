from typing import Type

from sqlalchemy.orm import Session
from sqlalchemy import extract, func, and_
from sqlalchemy.types import Interval
from sqlalchemy.exc import IntegrityError

from api.database.db import NotUniqueException
from api.database.models import Contact, User
from api.schemas import ContactBase, ContactUpdate


async def get_contacts(skip: int, limit: int, params: dict[str, str | None], user: User, db: Session) -> list[Type[Contact]]:
    """
    Retrieves a list of contacts for a specific user with specified pagination and additional parameters.

    :param skip: number of contacts to skip
    :type skip: int
    :param limit: max number of contacts in a set
    :type limit: int
    :param params: used for other parameters, for example - searching birthday people, or email to search by
    :type params: str
    :param user: the authorized user
    :type user: User
    :param db: database session
    :type db: Session
    :return: a list of contacts
    :rtype: List[Contact]
    """
    query = db.query(Contact)\

    query = query.filter(Contact.first_name.like(f'%{params["first_name"]}%')) if params["first_name"] else query
    query = query.filter(Contact.last_name.like(f'%{params["last_name"]}%')) if params["last_name"] else query
    query = query.filter(Contact.email.like(f'%{params["email"]}%')) if params["email"] else query

    if params["bt_within_week"]:
        # get number of years between the current year and the year of birth date
        # add the number of years we've got to the birth_date and subtract current_date from it
        query = query.filter(
            extract('day',
                    Contact.birth_date + func.concat(
                        extract('year', func.current_date()) - extract('year', Contact.birth_date),
                        ' ', 'year').cast(Interval) - func.current_date()
                    ).between(0, 7))

    result = query.filter(Contact.user_id == user.id).offset(skip).limit(limit).all()

    return result


async def get_contact(contact_id: int, user: User, db: Session) -> Type[Contact] | None:
    """
    Retrieves a contact by its ID

    :param contact_id: The ID of the contact in the DB
    :type contact_id: int
    :param user: the authorized user
    :type user: User
    :param db: database session
    :type db: Session
    :return: the contact by ID if found
    :rtype: Contact | None
    """
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def create_contact(body: ContactBase, user: User, db: Session) -> Contact | None:
    """
    Creates a new contact for a specific user

    :param body: information for creating a contact
    :type body: ContactBase
    :param user: the authorized user
    :type user: User
    :param db: database session
    :type db: Session
    :return: the newly created contact if succeeded
    :rtype: Contact | None
    """
    contact = Contact(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        phone=body.phone,
        birth_date=body.birth_date,
        description=body.description,
        user=user
    )
    db.add(contact)
    try:
        db.commit()
    except IntegrityError as integrity_error:
        db.rollback()
        raise NotUniqueException('The contact already exists!')

    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactUpdate, user: User, db: Session) -> Contact | None:
    """
    Updates existing contact for a specific user

    :param contact_id: ID of the contact to update
    :type contact_id: int
    :param body: new info to update the existing contact
    :type body: ContactUpdate
    :param user: the authorized user
    :type user: User
    :param db: database session
    :type db: Session
    :return: the updated contact
    :rtype: Contact | None
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.first_name = body.first_name or contact.first_name
        contact.last_name = body.last_name or contact.last_name
        contact.email = body.email or contact.email
        contact.phone = body.phone or contact.phone
        contact.birth_date = body.birth_date or contact.birth_date
        contact.description = body.description or contact.description
        db.commit()

    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    """
    Removes existing contact for a specific user

    :param contact_id: ID of the contact to remove
    :type contact_id: int
    :param user: the authorized user
    :type user: User
    :param db: database session
    :type db: Session
    :return: the removed contact if it existed
    :rtype: Contact | None
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()

    return contact
