from datetime import datetime, date
from sqlalchemy.orm import Session
from sqlalchemy import func
from social_network import schemas
from social_network.models import Post, User, Like
from social_network.security import get_password_hash


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session):
    return db.query(User).all()


def delete_all_users(db: Session):
    count = db.query(User).delete()
    db.commit()
    return count


def update_user_last_login(db: Session, user: User):
    user.last_visit = datetime.utcnow()
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user_last_request(db: Session, user: User):
    user.last_request = datetime.utcnow()
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_user(db: Session, user: schemas.UserCreate):
    """Create User using pydantic and secured password """

    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def modify_user(db: Session, user: User, data: schemas.UserCreate):
    data.password = get_password_hash(data.password)
    for key, value in data.__dict__.items():
        setattr(user, key, value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def change_password(db: Session, user: User, password: str):
    password = get_password_hash(password)
    user.password = password
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_posts(db: Session, user_id: int):
    return (  # db.query(Post)
        db.query(Post, func.count(Like.id).label("likes"))
        .join(Like)
        .filter(Post.owner_id == user_id)
        .all())


def create_user_post(db: Session, post: schemas.PostCreate, user_id: int):
    db_item = Post(**post.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_user_post(db: Session, user_id: int):
    count = db.query(Post).filter(Post.owner_id == user_id).delete()
    db.commit()
    return count


def get_post(db: Session, user_id: int, post_id: int):
    post = (db.query(Post)
            # db.query(Post, func.count(Like.id).label("likes"))
            # .join(Like)
            .filter(Post.owner_id == user_id)
            .filter(Post.id == post_id)
            .first())
    return post


def modify_post(db: Session, user_id: int, post_id: int,
                data: schemas.PostUpdate):
    post = get_post(db, user_id=user_id, post_id=post_id)
    if post:
        for key, value in data.__dict__.items():
            setattr(post, key, value)
        db.add(post)
        db.commit()
        db.refresh(post)
        return post


def delete_post(db: Session, user_id: int, post_id: int):
    return (db.query(Post).filter(Post.owner_id == user_id)
            .filter(Post.id == post_id).delete())


def show_likes(db: Session, user_id: int, post_id: int):
    return (db.query(Like).filter(Like.owner_id == user_id)
            .filter(Like.post_id == post_id).all())


def add_like(db: Session, user_id: int, post_id: int):
    like = Like()
    like.owner_id = user_id
    like.post_id = post_id
    db.add(like)
    db.commit()
    db.refresh(like)
    return like


def delete_likes(db: Session, user_id: int, post_id: int):
    return (db.query(Like).filter(Like.owner_id == user_id)
            .filter(Like.post_id == post_id).delete())


def delete_one_like(db: Session, user_id: int, post_id: int, like_id: int):
    return (db.query(Like).filter(Like.owner_id == user_id)
            .filter(Like.post_id == post_id)
            .filter(Like.id == like_id).delete())


def count_likes(db: Session, date_from: date, date_to: date):
    return (db.query(func.count(Like.id))
            .filter(func.DATE(Like.created) >= date_from)
            .filter(func.DATE(Like.created) <= date_to)
            .first())
