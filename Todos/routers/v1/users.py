from typing import Type
from fastapi import APIRouter
from starlette import status
from ..dependencies import UserServiceDependency, isAuthenticatedAdminDependency
from data.models.user import User
from schemas.request.user_request import ManageOneRequest
from schemas.response.user_response import UserResponse
import logging

# Get the logger instance
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users")


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_one(request: ManageOneRequest, service: UserServiceDependency):
    logger.info(f"create_one, request: {request}")

    response: User = service.create_one(request)

    return response


@router.get("", dependencies=[isAuthenticatedAdminDependency], response_model=list[UserResponse],
            status_code=status.HTTP_200_OK)
def get_many(service: UserServiceDependency):
    logger.info(f"get_many")

    response: list[Type[User]] = service.get_many()

    return response


@router.get("/{user_id}", dependencies=[isAuthenticatedAdminDependency], response_model=UserResponse,
            status_code=status.HTTP_200_OK)
def get_one(user_id: int, service: UserServiceDependency):
    logger.info(f"get_one, user_id: {user_id}")

    response: User = service.get_one(user_id)

    return response


@router.put("/{user_id}", dependencies=[isAuthenticatedAdminDependency], response_model=UserResponse,
            status_code=status.HTTP_200_OK)
def update_one(
        user_id: int,
        request: ManageOneRequest,
        service: UserServiceDependency
):
    logger.info(f"update_one, user_id: {user_id}, request: {request}")

    updated_user = service.update_one(user_id, request)

    return updated_user


@router.delete("/{user_id}", dependencies=[isAuthenticatedAdminDependency], status_code=status.HTTP_204_NO_CONTENT)
def delete_one(
        user_id: int,
        service: UserServiceDependency
):
    logger.info(f"delete_one, user_id: {user_id}")

    service.delete_one(user_id)