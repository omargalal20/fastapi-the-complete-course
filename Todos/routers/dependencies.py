from typing import Annotated

from fastapi import Depends

from data.database.postgres import SessionDep
from data.repository.todos_repository import TodosRepository
from data.repository.user_repository import UserRepository
from middleware.security import get_authenticated_user, authorized_admin, AuthenticatedUser
from services.auth.auth_service import AuthService
from services.todos.todos_service import TodosService
from services.user.user_service import UserService


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


TodosServiceDependency = Annotated[TodosService, Depends(get_todos_service)]
UserServiceDependency = Annotated[UserService, Depends(get_user_service)]
AuthServiceDependency = Annotated[AuthService, Depends(get_auth_service)]
AuthenticatedUserDependency = Annotated[AuthenticatedUser, Depends(get_authenticated_user)]
isAuthenticatedUserDependency = Depends(get_authenticated_user)
isAuthenticatedAdminDependency = Depends(authorized_admin)
