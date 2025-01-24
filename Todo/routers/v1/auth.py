from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette import status

from config.settings import get_settings
from data.models.user import User
from routers.dependencies import get_user_service, get_auth_service
from schemas.request.user_request import ManageOneRequest
from schemas.response.login_response import LoginResponse
from schemas.response.user_response import UserResponse
from services.auth_service import AuthService
from services.user_service import UserService
from utils.security import create_access_token

router = APIRouter(prefix="/auth")

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(todo: ManageOneRequest, service: UserService = Depends(get_user_service)):
    response: User = service.create_one(todo)

    return response


@router.post("/token", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
          service: AuthService = Depends(get_auth_service)) -> LoginResponse:
    user: User = service.authenticate_user(form_data.username, form_data.password)

    access_token_expires: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        user, expires_delta=access_token_expires
    )
    return LoginResponse(access_token=access_token, token_type="bearer")
