from typing import Type

from fastapi import APIRouter
from starlette import status

from data.models.todo import Todo
from schemas.request.todos_request import ManageOneRequest
from schemas.response.todos_response import TodosResponse
from ..dependencies import TodosServiceDependency, AuthenticatedUserDependency

router = APIRouter(prefix="/todos")


@router.post("", response_model=TodosResponse, status_code=status.HTTP_201_CREATED)
def create_one(request: ManageOneRequest,
               service: TodosServiceDependency,
               authenticated_user: AuthenticatedUserDependency):
    response: Todo = service.create_one(request, authenticated_user.id)

    return response


@router.get("", response_model=list[TodosResponse], status_code=status.HTTP_200_OK)
def get_many(
        service: TodosServiceDependency, authenticated_user: AuthenticatedUserDependency):
    response: list[Type[Todo]] = service.get_many(authenticated_user)

    return response


@router.get("/{todo_id}", response_model=TodosResponse, status_code=status.HTTP_200_OK)
def get_one(todo_id: int, service: TodosServiceDependency, authenticated_user: AuthenticatedUserDependency):
    response: Todo = service.get_one(todo_id, authenticated_user)

    return response


@router.put("/{todo_id}", response_model=TodosResponse, status_code=status.HTTP_200_OK)
def update_one(
        todo_id: int,
        request: ManageOneRequest,
        service: TodosServiceDependency,
        authenticated_user: AuthenticatedUserDependency
):
    updated_todo = service.update_one(todo_id, request, authenticated_user)

    return updated_todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_one(
        todo_id: int,
        service: TodosServiceDependency,
        authenticated_user: AuthenticatedUserDependency
):
    service.delete_one(todo_id, authenticated_user)
