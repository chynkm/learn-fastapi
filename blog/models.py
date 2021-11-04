from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(50))
    body = Column(String(254))

    user = relationship('User', back_populates='blogs')


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(254), unique=True)
    password = Column(String(254))

    blogs = relationship('Blog', back_populates='user')
