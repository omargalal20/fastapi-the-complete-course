from datetime import timedelta, datetime, timezone

import jwt
from passlib.context import CryptContext

from config.settings import get_settings
from data.models.user import User

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(user: User, expires_delta: timedelta | None = None):
    encode = {'sub': user.username, 'id': user.id, 'role': user.role.name}
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    encode.update({"exp": expire})
    encoded_jwt = jwt.encode(encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
