from fastapi import HTTPException

from data.models.user import User
from data.repository.user_repository import UserRepository
from utils.security import verify_password


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def authenticate_user(self, username: str, password: str) -> User:
        user: User = self.user_repository.get_one_by_username(username)

        if not user:
            raise HTTPException(status_code=401,
                                detail='Could not validate user.')
        if not verify_password(password, user.password):
            raise HTTPException(status_code=401,
                                detail='Could not validate user.')

        return user
