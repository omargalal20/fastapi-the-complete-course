from typing import Type

from fastapi import HTTPException

from . import todo_mapper
from .validation import TodosValidator
from ...data.models.todo import Todo
from ...data.models.user import Role
from ...data.repository.todos_repository import TodosRepository
from ...middleware.security import AuthenticatedUser
from ...schemas.request.todos_request import ManageOneRequest


class TodosService:
    def __init__(self, todos_repository: TodosRepository):
        self.todos_repository = todos_repository

    def create_one(self, request: ManageOneRequest, user_id: int) -> Todo:
        todo: Todo = todo_mapper.to_todo(request, user_id)
        created_todo: Todo = self.todos_repository.create_one(todo)

        return created_todo

    def get_many(self, authenticated_user: AuthenticatedUser) -> list[Type[Todo]]:

        todos: list[Type[
            Todo]] = self.todos_repository.get_many() if authenticated_user.role == Role.ADMIN \
            else self.todos_repository.get_many_by_user_id(authenticated_user.id)

        return todos

    def get_one(self, todo_id: int, authenticated_user: AuthenticatedUser) -> Todo:

        todo: Todo | None = self.todos_repository.get_one(todo_id)

        TodosValidator.verify_ownership(todo.owner_id, authenticated_user)

        if not todo:
            raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")

        return todo

    def update_one(self, todo_id: int, request: ManageOneRequest, authenticated_user: AuthenticatedUser) -> Todo:
        todo: Todo = self.get_one(todo_id, authenticated_user)

        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")

        updated_todo: Todo = todo_mapper.update_todo(todo, request)

        return self.todos_repository.update_one(updated_todo)

    def delete_one(self, todo_id: int, authenticated_user: AuthenticatedUser) -> None:
        todo: Todo = self.get_one(todo_id, authenticated_user)

        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")

        self.todos_repository.delete_one(todo)
