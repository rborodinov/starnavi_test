import datetime

from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    description: str | None = None


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class Like(BaseModel):
    owner_id: int
    post_id: int
    created: datetime


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    posts: list[Post] = []
    last_visit: datetime
    last_request: datetime

    class Config:
        orm_mode = True
