from fastapi import HTTPException
from starlette import status

from data.models.user import Role
from middleware.security import AuthenticatedUser


class TodosValidator:
    @staticmethod
    def verify_ownership(todo_owner_id: int, authenticated_user: AuthenticatedUser) -> None:
        if todo_owner_id != authenticated_user.id and authenticated_user.role != Role.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to perform this action"
            )
