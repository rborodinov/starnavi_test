import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType

from .database import Base


class User(Base):
    """
    User Model
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(EmailType, unique=True)
    password = Column(Text)

    posts = relationship("Post", back_populates="owner")

    last_visit = Column(DateTime)
    last_request = Column(DateTime)


class Post(Base):
    """
    Model to store user posts
    """
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="posts")
    created = Column(DateTime, default=datetime.datetime.now)



class Like(Base):
    """
    Model to store likes

    It might be with composite primary key of users_id and posts_id
    but task requirements are different.

    """
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="likes")

    post_id = Column(Integer, ForeignKey("posts.id"))
    post = relationship("Post", back_populates="likes")

    created = Column(DateTime, default=datetime.datetime.now)

