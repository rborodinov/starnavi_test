from fastapi import APIRouter
from social_network import crud, schemas, security
from social_network.database import get_db
from social_network.security import oauth2
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/posts/", response_model=list[schemas.Post])
def read_user_posts(db: Session = Depends(get_db), token=Depends(oauth2)):
    """All posts published bu user (user extracted from authentication token)"""
    user_id = security.get_current_user_id(token)
    posts = crud.get_posts(db, user_id)
    return posts

#
@router.post("/posts/", response_model=schemas.Post)
def create_user_post(post: schemas.PostCreate, db: Session = Depends(get_db),
               token=Depends(oauth2)):
    """Publish post from current user"""
    user_id = security.get_current_user_id(token)
    post = crud.create_user_post(db=db, post=post, user_id=user_id)
    return post

@router.delete("/posts/")
def delete_all_user_post(db: Session = Depends(get_db), token=Depends(oauth2)):
    """Delete all post from current user"""
    user_id = security.get_current_user_id(token)
    post = crud.delete_user_post(db=db, user_id=user_id)
    return post



@router.get("/posts/{post_id}", response_model=schemas.Post)
def read_user_single_post(post_id: int, db: Session = Depends(get_db),
                          token=Depends(oauth2)):
    """Get post by id published by current user"""
    user_id = security.get_current_user_id(token)
    posts = crud.get_post(db, user_id, post_id)
    return posts



@router.put("/posts/{post_id}", response_model=schemas.Post)
def change_user_single_post(post_id:int, post: schemas.Post, db: Session = Depends(get_db),
                          token=Depends(oauth2)):
    """Modify single post published earlier by user"""
    user_id = security.get_current_user_id(token)
    posts = crud.modify_post(db, user_id, post_id, post)
    return posts


@router.delete("/posts/{post_id}")
def delete_user_single_post(post_id:int, db: Session = Depends(get_db),
                          token=Depends(oauth2)):
    """Delete single post published earlier by user"""
    user_id = security.get_current_user_id(token)
    posts = crud.delete_post(db, user_id, post_id)
    return posts

#
# @router.get("/posts/{post_id}/likes", response_model=schemas.Like)
# def check_post_likes(post_id:int, db: Session = Depends(get_db),
#                           token=Depends(oauth2)):
#     """View likes done by user"""
#     user_id = security.get_current_user_id(token)
#     posts = crud.show_likes(db, user_id, post_id)
#     return posts
# #
# @router.post("/posts/{post_id}/likes")
# def like_post(post_id:int, db: Session = Depends(get_db),
#                           token=Depends(oauth2)):
#     """add like to the post"""
#     user_id = security.get_current_user_id(token)
#     posts = crud.delete_post(db, user_id, post_id)
#     return posts
#
# @router.delete("/posts/{post_id}/likes")
# def remove_user_likes(post_id:int, db: Session = Depends(get_db),
#                           token=Depends(oauth2)):
#     """Delete all likes from the post done by user"""
#     user_id = security.get_current_user_id(token)
#     posts = crud.delete_post(db, user_id, post_id)
#     return posts
#
# @router.delete("/posts/{post_id}/like/{like_id}")
# def remove_one_like(post_id:int, db: Session = Depends(get_db),
#                           token=Depends(oauth2)):
#     """Delete concrete like"""
#     user_id = security.get_current_user_id(token)
#     posts = crud.delete_post(db, user_id, post_id)
#     return posts
