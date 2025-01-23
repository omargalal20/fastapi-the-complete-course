from typing import Annotated

from fastapi import Depends
from database.database import SessionDep
from repository.todos_repository import TodosRepository
from services.todos_service import TodosService

def get_todos_repository(session: SessionDep):
    return TodosRepository(session)

def get_todos_service(
    todos_repository: Annotated[TodosRepository, Depends(get_todos_repository)]) -> TodosService:
    return TodosService(todos_repository)
