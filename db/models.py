from db.base import Base
from sqlalchemy import String, Column, Integer, DateTime


class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    patronymic = Column(String(50))
    email = Column(String(50), unique=True)
    password = Column(String)
    date_created = Column(DateTime)
    date_updated = Column(DateTime, nullable=True)
