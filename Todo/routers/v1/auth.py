from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from config.settings import get_settings
from data.models.user import User
from schemas.response.login_response import LoginResponse
from utils.security import create_access_token
from ..dependencies import AuthServiceDependency, AuthenticatedUserDependency

router = APIRouter(prefix="/auth")

settings = get_settings()


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
          service: AuthServiceDependency) -> LoginResponse:
    user: User = service.login(form_data.username, form_data.password)

    access_token_expires: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        user, expires_delta=access_token_expires
    )
    return LoginResponse(access_token=access_token, token_type="bearer")


@router.get("/me")
async def get_me(
        authenticated_user: AuthenticatedUserDependency,
):
    return authenticated_user
