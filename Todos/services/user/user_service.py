from typing import Type

from fastapi import HTTPException

from data.models.user import User
from data.repository.user_repository import UserRepository
from schemas.request.user_request import ManageOneRequest
from . import user_mapper


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_one(self, request: ManageOneRequest) -> User:
        user: User = user_mapper.to_user(request)

        created_user: User = self.user_repository.create_one(user)

        return created_user

    def get_many(self) -> list[Type[User]]:
        users: list[Type[User]] = self.user_repository.get_many()

        return users

    def get_one(self, user_id: int) -> User:
        user: User | None = self.user_repository.get_one(user_id)

        if not user:
            raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")

        return user

    def update_one(self, user_id: int, request: ManageOneRequest) -> User:
        user: User = self.get_one(user_id)

        updated_user: User = user_mapper.update_user(user, request)

        return self.user_repository.update_one(updated_user)

    def delete_one(self, user_id: int) -> None:
        user: User = self.get_one(user_id)

        self.user_repository.delete_one(user)
