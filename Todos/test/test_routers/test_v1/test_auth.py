from fastapi import status

from ...dependencies import *
from ....data.database.postgres import get_db
from ....middleware.security import get_authenticated_user


def test_login_success(test_users_and_admins):
    app.dependency_overrides[get_db] = override_get_db

    test_login_request = {
        "username": "userjohndoe",
        "password": "testpassword",
        "grant_type": "password"
    }

    response = client.post("/api/v1/auth/login", data=test_login_request)

    assert response.status_code == status.HTTP_200_OK

    response_json = response.json()
    assert "access_token" in response_json
    assert response_json["token_type"] == "bearer"


def test_login_invalid(test_users_and_admins):
    app.dependency_overrides[get_db] = override_get_db

    test_login_request = {
        "username": "userjohndoe",
        "password": "wrongpassword",
        "grant_type": "password"
    }

    response = client.post("/api/v1/auth/login", data=test_login_request)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_my_profile_authenticated_user(test_users_and_admins):
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_authenticated_user] = override_get_authenticated_user

    response = client.get("/api/v1/auth/my-profile")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "username": "userjohndoe",
        "email": "userjohndoe@email.com",
        "first_name": "John",
        "last_name": "Doe",
        "is_active": True,
        "role": "USER",
        "phone_number": "(111)-111-1111"
    }


def test_change_password_authenticated_user(test_users_and_admins):
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_authenticated_user] = override_get_authenticated_user

    test_change_password_request = {
        "new_password": "newpassword",
        "old_password": "testpassword"
    }

    response = client.post("/api/v1/auth/change-password", json=test_change_password_request)
    assert response.status_code == status.HTTP_202_ACCEPTED


def test_change_password_authenticated_user_incorrect_wrong_old_password(test_users_and_admins):
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_authenticated_user] = override_get_authenticated_user

    test_change_password_request = {
        "new_password": "newpassword",
        "old_password": "wrong_old_password"
    }

    response = client.post("/api/v1/auth/change-password", json=test_change_password_request)
    assert response.status_code == status.HTTP_409_CONFLICT


# Unauthenticated

def test_get_my_profile_unauthenticated():
    app.dependency_overrides = {}
    response = client.get("/api/v1/auth/my-profile")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {
        "detail": "Not authenticated"
    }


def test_change_password_unauthenticated(test_users_and_admins):
    app.dependency_overrides = {}

    test_change_password_request = {
        "new_password": "newpassword",
        "old_password": "testpassword"
    }

    response = client.post("/api/v1/auth/change-password", json=test_change_password_request)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {
        "detail": "Not authenticated"
    }
