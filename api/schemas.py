from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr


class ContactBase(BaseModel):
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=12, pattern=r'^[0-9]{3,}$')
    birth_date: date
    description: Optional[str] = Field(None, max_length=150)


class ContactResponse(ContactBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class ContactUpdate(ContactBase):
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = Field(None)
    phone: Optional[str] = Field(None, max_length=12, pattern=r'^[0-9]{3,}$')
    birth_date: Optional[date] = Field(None)
    description: Optional[str] = Field(None, max_length=150)


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr
