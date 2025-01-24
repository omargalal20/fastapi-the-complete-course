from typing import Annotated, Type

from fastapi import APIRouter, Depends
from starlette import status

from data.models.user import User
from routers.dependencies import get_user_service
from schemas.request.user_request import ManageOneRequest
from schemas.response.user_response import UserResponse
from services.user_service import UserService

router = APIRouter(prefix="/users")


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_one(request: ManageOneRequest, service: Annotated[UserService, Depends(get_user_service)]):
    response: User = service.create_one(request)

    return response

@router.get("", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
def get_many(
        service: Annotated[UserService, Depends(get_user_service)]):
    response: list[Type[User]] = service.get_many()

    return response


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_one(user_id: int, service: Annotated[UserService, Depends(get_user_service)]):
    response: User = service.get_one(user_id)

    return response


@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_one(
        user_id: int,
        request: ManageOneRequest,
        service: Annotated[UserService, Depends(get_user_service)]
):
    updated_todo = service.update_one(user_id, request)

    return updated_todo


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_one(
        user_id: int,
        service: Annotated[UserService, Depends(get_user_service)]
):
    service.delete_one(user_id)