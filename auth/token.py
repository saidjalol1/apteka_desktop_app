from datetime import datetime, timedelta, timezone
from fastapi import Depends
from jose import jwt, JWTError
from decouple import config

JWT_SECRET = config("secret")
ALGORITH = config("algorithm")


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {"sub" : username, "id" : user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    print(expires)
    encode.update({"exp": expires})
    return jwt.encode(encode, JWT_SECRET,algorithm=ALGORITH)

