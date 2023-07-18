from libgravatar import Gravatar
from sqlalchemy.orm import Session

from api.database.models import User
from api.schemas import UserModel

from typing import Type


async def get_user_by_email(email: str, db: Session) -> Type[User]:
    """
    Gets a user by its email address

    :param email: valid email address
    :type email: str
    :param db: database session
    :type db: Session
    :return: the found user
    :rtype: User
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    Creates a new user

    :param body: informational fields to create a new user
    :type body: UserModel
    :param db: database session
    :type db: Session
    :return: the newly created user
    :rtype: User
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.model_dump(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    Updates the refresh_token of the user

    :param user: user whose token is being updated
    :type user: User
    :param token: new token
    :type token: str | None
    :param db: database session
    :type db: Session
    :return:
    :rtype: None
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    Sets email status of the user to confirmed

    :param email: valid email address
    :type email: str
    :param db: database session
    :type db: Session
    :return:
    :rtype: None
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email: str, url: str, db: Session) -> Type[User]:
    """
    Writes a new value of the avatar string for the user

    :param email: valid email address
    :type email: str
    :param url: URL of the new avatar
    :type url: str
    :param db: database session
    :type db: Session
    :return: the user whose avatar has been updated
    :rtype: User
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
