from datetime import datetime

from pydantic import BaseModel
from pydantic.networks import EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


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
    email: EmailStr

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class UserModify(UserCreate):
    last_visit: datetime
    last_request: datetime

    class Config:
        orm_mode = True


class User(UserModify):
    id: int
    posts: list[Post] = []

    class Config:
        orm_mode = True

