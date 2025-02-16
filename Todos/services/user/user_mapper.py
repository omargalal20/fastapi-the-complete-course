from data.models.user import User
from schemas.request.user_request import ManageOneRequest
from middleware.security import get_password_hash


def to_user(request: ManageOneRequest) -> User:
    created_user: User = User(
        email=request.email,
        username=request.username,
        first_name=request.first_name,
        last_name=request.last_name,
        role=request.role,
        password=get_password_hash(request.password),
        is_active=request.is_active,
        phone_number=request.phone_number
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
    user.phone_number = request.phone_number

    return user
