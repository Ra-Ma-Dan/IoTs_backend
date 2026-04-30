from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer #OAuth2PasswordForm
import hashlib
from datetime import datetime, timedelta, timezone
from jose import jwt


ACCESS_TOKEN_EXP_MINUTES = 30
REFRESH_TOKEN_EXP_DAY = 7



ALGO = 'HS256'
SECERET_KEY = "super-seceret"

pw_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password : str) -> str:
    digest = hashlib.sha3_256(password.encode("utf-8")).digest()
    return pw_context.hash(digest)

def verify_password(plain : str, hashed : str) -> bool:
    digest = hashlib.sha3_256(plain.encode("utf-8")).digest()
    return pw_context.verify(digest, hashed)

def create_access_token(user_id : int):
    payload = {
        'sub' : str(user_id),
        'exp' : datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXP_MINUTES)
    }
    return jwt.encode(payload, SECERET_KEY, algorithm=ALGO,)

def create_refresh_token(user_id : int):
    payload = {
        'sub' : str(user_id),
        'exp' : datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXP_DAY)
    }

    return jwt.encode(payload, SECERET_KEY, algorithm=ALGO)


def decode_token(token : str):
    return jwt.decode(token, SECERET_KEY, algorithms=[ALGO])

# def refresh(token : str):
#     payload = decode_token(token)
