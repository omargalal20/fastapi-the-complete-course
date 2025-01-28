from fastapi import HTTPException
from starlette import status

from .validation import AuthValidator
from ...data.models.user import User
from ...data.repository.user_repository import UserRepository
from ...middleware.security import verify_password, get_password_hash
from ...schemas.request.change_password_request import ChangePasswordRequest


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

        AuthValidator.change_password_validator(request.old_password, user.password)

        user.password = get_password_hash(request.new_password)

        self.user_repository.update_one(user)
