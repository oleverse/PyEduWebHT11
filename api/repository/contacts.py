from typing import Type

from sqlalchemy.orm import Session
from sqlalchemy import extract, func, and_
from sqlalchemy.types import Interval
from sqlalchemy.exc import IntegrityError

from api.database.db import NotUniqueException
from api.database.models import Contact, User
from api.schemas import ContactBase, ContactUpdate


async def get_contacts(skip: int, limit: int, params: dict[str, str], user: User, db: Session) -> list[Type[Contact]]:
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
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def create_contact(body: ContactBase, user: User, db: Session) -> Contact | str | None:
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
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()

    return contact
