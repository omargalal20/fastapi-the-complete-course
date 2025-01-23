from typing import Annotated, Type

from fastapi import APIRouter, Depends
from starlette import status

from models.todo import Todo
from schemas.request.todos_request import ManageOneRequest
from schemas.response.todos_response import TodosResponse
from services.todos_service import TodosService
from ..dependencies import get_todos_service

router = APIRouter(prefix="/todos")


@router.post("", response_model=TodosResponse, status_code=status.HTTP_201_CREATED)
def create_todo(todo: ManageOneRequest, service: TodosService = Depends(get_todos_service)):
    response: Todo = service.create_one(todo)

    return response


@router.get("", response_model=list[TodosResponse], status_code=status.HTTP_200_OK)
def get_many(
        service: Annotated[TodosService, Depends(get_todos_service)]):
    response: list[Type[Todo]] = service.get_many()

    return response


@router.get("/{todo_id}", response_model=TodosResponse, status_code=status.HTTP_200_OK)
def get_todo(todo_id: int, service: Annotated[TodosService, Depends(get_todos_service)]):
    response: Todo = service.get_one(todo_id)

    return response


@router.put("/{todo_id}", response_model=TodosResponse, status_code=status.HTTP_200_OK)
def update_todo(
        todo_id: int,
        todo_data: ManageOneRequest,
        service: Annotated[TodosService, Depends(get_todos_service)]
):
    updated_todo = service.update_one(todo_id, todo_data)

    return updated_todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
        todo_id: int,
        service: Annotated[TodosService, Depends(get_todos_service)]
):
    service.delete_one(todo_id)
