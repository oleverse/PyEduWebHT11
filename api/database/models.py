from sqlalchemy import Column, Integer, String, func
from sqlalchemy.sql.sqltypes import Date, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(13), nullable=True)
    birth_date = Column(Date, default=func.now())
    created_at = Column('created_at', DateTime, default=func.now())
    description = Column(String(250), nullable=True)
