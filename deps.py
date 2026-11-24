from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from database.db import SessionLocal
from auths import decode_token
from database import dbModels
from database.dbModels import User
from sqlalchemy.orm import Session

router = APIRouter()

OAuth2_scheme = OAuth2PasswordBearer(tokenUrl='users/login')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token : str = Depends(OAuth2_scheme), db : Session=Depends(get_db)):
    decoded = decode_token(token)
    sub = int(decoded.get("sub"))

    current_user = db.query(User).filter(User.user_id == sub).first()
    return current_user


def get_user_by_email(email : str, db : Session):
    user = db.query(User).filter(User.email==email).first()
    return user


def get_user_by_username(username : str, db : Session):
    user = db.query(User).filter(User.username==username).first()
    return user