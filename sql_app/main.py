from fastapi import APIRouter
from datetime import timedelta
from sql_app.database import SessionLocal
from sql_app import crud, models, schemas, security
from sql_app.database import engine
from sql_app.security import oauth2, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Give bearer token to user for further access"""
    user = security.authenticate_user(db, form_data.username, form_data.password)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    # Update user last login time
    crud.update_user_last_login(db=db, user=user)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/users/", response_model=schemas.UserCreate)
def create_user(user: schemas.UserCreate , db: Session = Depends(get_db)):
    """Endpoint similar to signup but in clear REST we want to see POST on /users/
      as signup is equivalent of create new user"""
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=422,
                            detail={"loc": ["body", "email"],
                                    "msg": "This email is already registered",
                                    "type": "value_error.email"})
    return crud.create_user(db, user=user)


@router.get("/users/", response_model=list[schemas.User])
def read_users(token=Depends(oauth2), db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return users


@router.delete("/users/")
def delete_all_users(token=Depends(oauth2), db: Session = Depends(get_db)):
    users = crud.delete_all_users(db)
    return users


@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

#
# @router.post("/users/{user_id}/posts/", response_model=schemas.Post)
# def create_item_for_user(
#         user_id: int, item: schemas.PostCreate
#         , db: Session = Depends(get_db)):
#     return crud.create_user_post(item=item, user_id=user_id)
#
#
# @router.get("/posts/", response_model=list[schemas.Post])
# def read_items(skip: int = 0, limit: int = 100):
#     items = crud.get_posts(skip=skip, limit=limit)
#     return items
