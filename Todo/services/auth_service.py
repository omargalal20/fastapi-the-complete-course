from fastapi import HTTPException
from starlette import status

from data.models.user import User
from data.repository.user_repository import UserRepository
from schemas.request.change_password_request import ChangePasswordRequest
from utils.security import verify_password, get_password_hash


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

    def get_my_profile(self, user_id: int) -> User:
        user: User = self.user_repository.get_one(user_id)

        return user

    def change_password(self, user_id: int, request: ChangePasswordRequest):
        user: User = self.user_repository.get_one(user_id)

        old_password_validation_exception = HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Enter correct old password",
        )

        if not verify_password(request.old_password, user.password):
            raise old_password_validation_exception

        user.password = get_password_hash(request.new_password)

        self.user_repository.update_one(user)
