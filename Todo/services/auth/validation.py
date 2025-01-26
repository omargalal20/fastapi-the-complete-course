from fastapi import HTTPException
from starlette import status

from ...middleware.security import verify_password


class AuthValidator:
    @staticmethod
    def change_password_validator(request_old_password: str, user_old_password: str):
        old_password_validation_exception = HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Enter correct old password",
        )

        if not verify_password(request_old_password, user_old_password):
            raise old_password_validation_exception
