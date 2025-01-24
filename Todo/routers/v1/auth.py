from fastapi import APIRouter, Depends
from starlette import status

from data.models.user import User
from routers.dependencies import get_user_service
from schemas.request.user_request import ManageOneRequest
from schemas.response.user_response import UserResponse
from services.user_service import UserService

router = APIRouter(prefix="/auth")


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(todo: ManageOneRequest, service: UserService = Depends(get_user_service)):
    response: User = service.create_one(todo)

    return response


@router.get("", status_code=status.HTTP_200_OK)
def get_user():
    return {'user': 'Authenticated'}
