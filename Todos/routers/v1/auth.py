from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from config.settings import get_settings
from data.models.user import User
from middleware.security import create_access_token
from schemas.request.change_password_request import ChangePasswordRequest
from schemas.response.login_response import LoginResponse
from schemas.response.user_response import UserResponse
from ..dependencies import AuthServiceDependency, AuthenticatedUserDependency
import logging

# Get the logger instance
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth")

settings = get_settings()


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
          service: AuthServiceDependency) -> LoginResponse:
    logger.info(f"login, username: {form_data.username}")

    user: User = service.login(form_data.username, form_data.password)

    access_token_expires: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        user, expires_delta=access_token_expires
    )
    return LoginResponse(access_token=access_token, token_type="bearer")


@router.get("/my-profile", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_my_profile(
        authenticated_user: AuthenticatedUserDependency,
        service: AuthServiceDependency
) -> UserResponse:
    logger.info(f"get_my_profile, user {authenticated_user.id}")

    response = service.get_my_profile(authenticated_user.id)

    return response


@router.post("/change-password", status_code=status.HTTP_202_ACCEPTED)
def change_password(
        request: ChangePasswordRequest,
        authenticated_user: AuthenticatedUserDependency,
        service: AuthServiceDependency
):
    logger.info(f"change_password, request: {request}, user {authenticated_user.id}")

    service.change_password(authenticated_user.id, request)