from typing import Type

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from data.models.user import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_one(self, user: User) -> User:
        """
        Adds a new user to the database.
        """
        self.session.add(user)
        try:
            self.session.commit()
            self.session.refresh(user)
        except IntegrityError:
            self.session.rollback()
            raise HTTPException(status_code=400, detail="Error creating User")
        return user

    def get_many(self) -> list[Type[User]]:
        """
        Retrieves all users from the database.
        """
        return self.session.query(User).all()

    def get_one(self, user_id: int) -> User | None:
        """
        Retrieves a single user by their ID.
        """
        user = self.session.query(User).filter(User.id.__eq__(user_id)).first()

        return user

    def update_one(self, updated_user: User) -> User:
        """
        Updates an existing user in the database.
        """
        try:
            self.session.commit()
            self.session.refresh(updated_user)
        except IntegrityError:
            self.session.rollback()
            raise HTTPException(status_code=400, detail="Error updating User")
        return updated_user

    def delete_one(self, user: User) -> None:
        """
        Deletes a user from the database.
        """
        self.session.delete(user)
        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise HTTPException(status_code=400, detail="Error deleting User")
