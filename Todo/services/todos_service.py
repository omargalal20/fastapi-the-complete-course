from typing import Type

from fastapi import HTTPException

from models.todo import Todo
from repository.todos_repository import TodosRepository
from schemas.request.todos_request import ManageOneRequest


class TodosService:
    def __init__(self, todos_repository: TodosRepository):
        self.todos_repository = todos_repository

    def create_one(self, request: ManageOneRequest) -> Todo:
        todo: Todo = Todo(**request.model_dump())

        created_todo: Todo = self.todos_repository.create_one(todo)

        return created_todo

    def get_many(self) -> list[Type[Todo]]:

        todos: list[Type[Todo]] = self.todos_repository.get_many()

        return todos

    def get_one(self, todo_id: int) -> Todo:

        todo: Todo | None = self.todos_repository.get_one(todo_id)

        if not todo:
            raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")

        return todo

    def update_one(self, todo_id: int, todo_data: ManageOneRequest) -> Todo:
        todo = self.get_one(todo_id)

        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")

        todo.title = todo_data.title
        todo.description = todo_data.description
        todo.priority = todo_data.priority
        todo.complete = todo_data.complete

        updated_todo: Todo = self.todos_repository.update_one(todo)

        return updated_todo

    def delete_one(self, todo_id: int) -> None:
        todo = self.get_one(todo_id)

        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")

        self.todos_repository.delete_one(todo)
