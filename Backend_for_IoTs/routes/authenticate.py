from fastapi import Depends, APIRouter, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from database.dbModels import User
from auths import hash_password, create_access_token, verify_password, create_refresh_token
from schema.schema import CreateUser, UserSchema
from deps import get_db

router = APIRouter(prefix='', tags=["Endpoits"])

DBdepends = Annotated[Session, Depends(get_db)]

@router.post("/signup", response_model=UserSchema)
def create_user(user : CreateUser, db : DBdepends):
    exist : bool = (db.query(User).filter(
        User.username == user.username
    ).first() is not None) or (db.query(User).filter(
        User.email == user.email
    ).first() is not None)
    if exist:
        raise HTTPException(
            status_code=400,
            detail="User already exist"
        )
    hash_pass=hash_password(user.password)
    new_user = User(
        fullname=user.fullname,
        username=user.username,
        hased_password=hash_pass,
        email=user.email,
        number=user.number
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post('/login')
def login(
    form_data : Annotated[OAuth2PasswordRequestForm, Depends()],
    db : DBdepends,
):
    user = db.query(User).filter(User.email==form_data.username).first()


    if (user == None):
        raise HTTPException(
            status_code=404, detail="User not Found"
        )
    if not verify_password(form_data.password, user.hased_password):

        raise HTTPException(
            status_code=409, detail="Incorrect Credentials"
        )
    
    access_token = create_access_token(user.user_id)
    refreh_token = create_refresh_token(user.user_id)

    return {
        "token_type" : "Bearer",
        "access_token" : access_token,
        "refresh_token" : refreh_token
    }
    

@router.post('/logout')
def logout():
    pass