from datetime import datetime
from sqlalchemy.orm import Session
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


def modify_user(db: Session, user:User, data: schemas.UserCreate):
    data.password = get_password_hash(data.password)
    for key, value in data.__dict__.items():
        setattr(user, key, value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def change_password(db: Session, user:User, password: str):
    password = get_password_hash(password)
    user.password = password
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_posts(db: Session, user_id:int):
    return db.query(Post).filter().all()


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


def get_post(db: Session,user_id:int,  post_id: int):
    return (db.query(Post).filter(Post.owner_id == user_id)
                          .filter(Post.id == post_id).first())


def modify_post(db: Session, user_id:int, post_id:int,
                data: schemas.PostUpdate):
    post = get_post(db, user_id=user_id, post_id=post_id)
    if post:
        for key, value in data.__dict__.items():
            setattr(post, key, value)
        db.add(post)
        db.commit()
        db.refresh(post)
        return post


def delete_post (db: Session, user_id:int, post_id:int):
    return (db.query(Post).filter(Post.owner_id == user_id)
                          .filter(Post.id == post_id).delete())


# def show_likes(db, user_id, post_id):
#     return db.query(Like)
#



