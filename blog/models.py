from sqlalchemy import Column, Integer, String
from .database import Base


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    body = Column(String(254))


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(254), unique=True)
    password = Column(String(254))
