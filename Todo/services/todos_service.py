from sqlite3 import IntegrityError
from typing import Type

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.todo import Todo
from schemas.request.todos_request import ManageOneRequest


class TodosService:
    def __init__(self, session: Session):
        """
        Initializes the TodosService with a database session.

        :param session: The database session to use for queries
        """
        self.session = session

    def create_one(self, request: ManageOneRequest) -> Todo:
        todo = Todo(**request.model_dump())
        self.session.add(todo)

        try:
            self.session.commit()
            self.session.refresh(todo)
        except IntegrityError as e:
            self.session.rollback()
            raise HTTPException(status_code=400, detail="Error creating Todo")
        return todo

    def get_many(self) -> list[Type[Todo]]:
        """
        Retrieves all todos from the database.

        :return: A list of Todo objects
        """
        result = self.session.query(Todo).all()
        return result

    def get_one(self, todo_id: int) -> Todo:
        """
        Retrieves a single todo by its ID.

        :param todo_id: The ID of the todo to retrieve
        :return: The Todo object if found
        :raises HTTPException: If the todo is not found
        """
        todo = self.session.query(Todo).get(todo_id)
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

        try:
            self.session.commit()
            self.session.refresh(todo)
        except IntegrityError as e:
            self.session.rollback()
            raise HTTPException(status_code=400, detail="Error updating Todo")

        return todo

    def delete_one(self, todo_id: int) -> None:
        todo = self.get_one(todo_id)

        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")

        # Delete the Todo item
        self.session.delete(todo)
        try:
            self.session.commit()
        except IntegrityError as e:
            self.session.rollback()
            raise HTTPException(status_code=400, detail="Error deleting Todo")
