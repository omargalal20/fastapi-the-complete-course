from typing import Annotated

from fastapi import Depends

from data.database.sqlite import SessionDep
from data.repository.todos_repository import TodosRepository
from data.repository.user_repository import UserRepository
from services.auth_service import AuthService
from services.todos_service import TodosService
from services.user_service import UserService


def get_todos_repository(session: SessionDep):
    return TodosRepository(session)


def get_user_repository(session: SessionDep):
    return UserRepository(session)


def get_todos_service(
        todos_repository: Annotated[TodosRepository, Depends(get_todos_repository)]) -> TodosService:
    return TodosService(todos_repository)


def get_user_service(
        user_repository: Annotated[UserRepository, Depends(get_user_repository)]) -> UserService:
    return UserService(user_repository)


def get_auth_service(
        user_repository: Annotated[UserRepository, Depends(get_user_repository)]) -> AuthService:
    return AuthService(user_repository)
