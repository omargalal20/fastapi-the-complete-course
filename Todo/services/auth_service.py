from fastapi import HTTPException
from starlette import status

from data.models.user import User
from data.repository.user_repository import UserRepository
from utils.security import verify_password


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def login(self, username: str, password: str) -> User:
        user: User = self.user_repository.get_one_by_username(username)

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        if not user:
            raise credentials_exception
        if not verify_password(password, user.password):
            raise credentials_exception

        return user
