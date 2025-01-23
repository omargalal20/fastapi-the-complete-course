from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from services.todos_service import TodosService
from ..dependencies import get_todos_service

router = APIRouter(prefix="/todos")


@router.get("", status_code=status.HTTP_200_OK)
def get_many(
        service: Annotated[TodosService, Depends(get_todos_service)]):
    response = service.get_many()
    return response


@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
def get_todo(todo_id: int, service: Annotated[TodosService, Depends(get_todos_service)]):
    return service.get_one(todo_id)
