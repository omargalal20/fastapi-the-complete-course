from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from data.database.sqlite import SessionDep
from data.repository.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


def get_user_repository(session: SessionDep):
    return UserRepository(session)


UserRepositoryDependency = Annotated[UserRepository, Depends(get_user_repository)]
TokenDependency = Annotated[str, Depends(oauth2_scheme)]
