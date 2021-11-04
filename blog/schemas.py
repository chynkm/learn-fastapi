from pydantic import BaseModel
from typing import List


class User(BaseModel):
    name: str
    email: str
    password: str


class BlogBase(BaseModel):
    title: str
    body: str


class Blog(BlogBase):
    class Config():
        orm_mode = True


class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[Blog] = []

    class Config():
        orm_mode = True


class ShowBlog(BaseModel):
    title: str
    body: str
    user: ShowUser

    # for DB data retrieval
    class Config():
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str
