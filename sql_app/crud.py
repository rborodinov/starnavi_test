from datetime import datetime
from sqlalchemy.orm import Session
from . import models, schemas
from .security import get_password_hash


def get_user(db: Session, user_id: int):

    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):

    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session):

    return db.query(models.User).all()


def delete_all_users(db: Session):
    count = db.query(models.User).count()
    db.query(models.User).delete()
    db.commit()
    return count


def update_user_last_login(db: Session, user: models.User):

    user.last_visit = datetime.utcnow()
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user_last_request(db: Session, user: models.User):

    user.last_request = datetime.utcnow()
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_user(db: Session, user: schemas.UserCreate):
    """Create User using pydantic and secured password """

    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def modify_user(db: Session, user:models.User, data: schemas.UserCreate):
    data.password = get_password_hash(data.password)
    for key, value in data.__dict__.items():
        setattr(user, key, value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def change_password(db: Session, user:models.User, password: str):
    password = get_password_hash(password)
    user.password = password
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# def get_posts(db: Session, skip: int = 0, limit: int = 100):
#
#     return db.query(models.Post).offset(skip).limit(limit).all()
#
#
# def create_user_post(db: Session, post: schemas.PostCreate, user_id: int):
#
#     db_item = models.Post(**post.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
#