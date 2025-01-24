from datetime import timedelta, datetime, timezone

import jwt
from fastapi import HTTPException, status
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from config.settings import get_settings
from data.models.user import User
from utils.dependencies import TokenDependency, UserRepositoryDependency

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


async def get_authenticated_user(token: TokenDependency, user_repository: UserRepositoryDependency) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None or user_role is None:
            raise credentials_exception
        user = user_repository.get_one_by_username(username)
        return user
    except InvalidTokenError:
        raise credentials_exception
