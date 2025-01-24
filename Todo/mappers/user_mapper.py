from passlib.hash import pbkdf2_sha256

from data.models.user import User
from schemas.request.user_request import ManageOneRequest


def to_user(request: ManageOneRequest) -> User:
    created_user: User = User(
        email=request.email,
        username=request.username,
        first_name=request.first_name,
        last_name=request.last_name,
        role=request.role,
        password=pbkdf2_sha256.hash(request.password),
        is_active=True
    )

    return created_user


def update_user(user: User, request: ManageOneRequest) -> User:
    user.email = request.email
    user.username = request.username
    user.first_name = request.first_name
    user.last_name = request.last_name
    user.password = request.password
    user.is_active = request.is_active
    user.role = request.role

    return user
