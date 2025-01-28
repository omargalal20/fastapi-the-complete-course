from typing import Type

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from data.models.todo import Todo


class TodosRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_one(self, todo: Todo) -> Todo:
        self.session.add(todo)
        try:
            self.session.commit()
            self.session.refresh(todo)
        except IntegrityError:
            self.session.rollback()
            raise HTTPException(status_code=400, detail="Error creating Todos")
        return todo

    def get_many(self) -> list[Type[Todo]]:

        return self.session.query(Todo).all()

    def get_many_by_user_id(self, user_id: int) -> list[Type[Todo]]:

        return self.session.query(Todo).filter(Todo.owner_id.__eq__(user_id)).all()

    def get_one(self, todo_id: int) -> Todo | None:
        todo = self.session.query(Todo).filter(Todo.id.__eq__(todo_id)).first()

        return todo

    def update_one(self, updated_todo: Todo) -> Todo:
        try:
            self.session.commit()
            self.session.refresh(updated_todo)
        except IntegrityError:
            self.session.rollback()
            raise HTTPException(status_code=400, detail="Error updating Todos")
        return updated_todo

    def delete_one(self, todo: Todo) -> None:
        self.session.delete(todo)
        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise HTTPException(status_code=400, detail="Error deleting Todos")
