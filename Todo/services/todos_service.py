from typing import Type

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.todo import Todo


class TodosService:
    def __init__(self, session: Session):
        """
        Initializes the TodosService with a database session.

        :param session: The database session to use for queries
        """
        self.session = session

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
