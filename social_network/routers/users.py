from fastapi import APIRouter
from datetime import timedelta
from social_network import crud, models, schemas, security
from social_network.database import engine, get_db
from social_network.security import oauth2, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session


router = APIRouter()


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Give bearer token to user for further access"""
    user = security.authenticate_user(db, form_data.username, form_data.password)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email, "id": user.id}, expires_delta=access_token_expires
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
    """List of all users currently registered"""
    users = crud.get_users(db)
    return users


@router.delete("/users/")
def delete_all_users(token=Depends(oauth2), db: Session = Depends(get_db)):
    """Remove all users including yourself"""
    users = crud.delete_all_users(db)
    return users


@router.get("/users/{user_id}", response_model=schemas.User)
def get_single_user(user_id: int, db: Session = Depends(get_db),
                    token=Depends(oauth2)):
    """Read information about any user (unsafe))

    User activity an endpoint which will show when user was login last time and when he mades a last request to the service.
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/users/{user_id}", response_model=schemas.User)
def modify_single_user(user_id: int, user_data: schemas.UserModify,
                       db: Session = Depends(get_db), token=Depends(oauth2)):
    """Modify any user, security issue present )"""
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user = crud.modify_user(db, user=db_user, data=user_data)
    return user


@router.post("/change_password", response_model=schemas.User)
def change_password(password: str, db: Session = Depends(get_db),
                    token=Depends(oauth2)):
    """Change password, actually we can use /user/{id} endpoint with PUTCH
    But why user must to enter his id to modify password )"""
    email = security.get_current_user_email(token)
    user = crud.get_user_by_email(db, email)
    user = crud.change_password(db, user, password)
    return user

