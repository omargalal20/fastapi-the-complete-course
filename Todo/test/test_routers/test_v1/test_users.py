from fastapi import status

from ...dependencies import *
from ....data.database.postgres import get_db
from ....middleware.security import get_authenticated_user


def test_create_one_authenticated_admin_valid_request(test_users_and_admins):
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_authenticated_user] = override_get_authenticated_admin

    test_create_one_request = {
        "username": "testjohndoe",
        "email": "testjohndoe@email.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": "testpassword",
        "is_active": True,
        "role": Role.USER.name,
        "phone_number": "111-111-1111"
    }

    test_create_one_response = client.post("/api/v1/users", json=test_create_one_request)
    assert test_create_one_response.status_code == status.HTTP_201_CREATED

    created_user = test_create_one_response.json()
    assert created_user.get('username') == test_create_one_request.get('username')
    assert created_user.get('email') == test_create_one_request.get('email')
    assert created_user.get('first_name') == test_create_one_request.get('first_name')
    assert created_user.get('last_name') == test_create_one_request.get('last_name')
    assert created_user.get('is_active') == test_create_one_request.get('is_active')
    assert created_user.get('role') == test_create_one_request.get('role')
    assert created_user.get('phone_number') == test_create_one_request.get('phone_number')

    assert 'password' not in created_user


def test_create_one_authenticated_admin_invalid_email(test_users_and_admins):
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_authenticated_user] = override_get_authenticated_admin

    test_create_one_request = {
        "username": "userjohndoe",
        "email": "userjohnemail.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": "testpassword",
        "is_active": True,
        "role": Role.USER.value,
        "phone_number": "(111)-111-1111"
    }
    response = client.post("/api/v1/users", json=test_create_one_request)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_one_authenticated_user(test_users_and_admins):
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_authenticated_user] = override_get_authenticated_user

    test_user_id = 1
    response = client.get(f"/api/v1/users/{test_user_id}")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {
        "detail": "You are not authorized to perform this action"
    }


def test_get_many_authenticated_admin(test_users_and_admins):
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_authenticated_user] = override_get_authenticated_admin

    response = client.get("/api/v1/users")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "id": 1,
            "username": "userjohndoe",
            "email": "userjohndoe@email.com",
            "first_name": "John",
            "last_name": "Doe",
            "is_active": True,
            "role": "USER",
            "phone_number": "(111)-111-1111"
        },
        {
            "id": 2,
            "username": "userjanedoe",
            "email": "userjanedoe@email.com",
            "first_name": "Jane",
            "last_name": "Doe",
            "is_active": True,
            "role": "USER",
            "phone_number": "(222)-222-2222"
        },
        {
            "id": 3,
            "username": "adminjohndoe",
            "email": "adminjohndoe@email.com",
            "first_name": "John",
            "last_name": "Doe",
            "is_active": True,
            "role": "ADMIN",
            "phone_number": "(333)-333-3333"
        },
        {
            "id": 4,
            "username": "adminjanedoe",
            "email": "adminjanedoe@email.com",
            "first_name": "Jane",
            "last_name": "Doe",
            "is_active": True,
            "role": "ADMIN",
            "phone_number": "(444)-444-4444"
        }
    ]


def test_get_many_authenticated_user(test_users_and_admins):
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_authenticated_user] = override_get_authenticated_user

    response = client.get("/api/v1/users")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {
        "detail": "You are not authorized to perform this action"
    }


def test_get_one_authenticated_admin(test_users_and_admins):
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_authenticated_user] = override_get_authenticated_admin

    test_user_id = 1
    response = client.get(f"/api/v1/users/{test_user_id}")
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


def test_get_one_authenticated_user(test_users_and_admins):
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_authenticated_user] = override_get_authenticated_user

    test_user_id = 1
    response = client.get(f"/api/v1/users/{test_user_id}")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {
        "detail": "You are not authorized to perform this action"
    }


def test_update_one_authenticated_admin_valid_request(test_users_and_admins):
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_authenticated_user] = override_get_authenticated_admin

    # Test request payload for updating the user
    test_update_one_request = {
        "username": "testjohndoe",
        "email": "testjohndoe@email.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": "testpassword",
        "is_active": True,
        "role": Role.USER.name,
        "phone_number": "111-111-1111"
    }

    test_user_id = 1

    test_update_one_response = client.put(f"/api/v1/users/{test_user_id}", json=test_update_one_request)
    assert test_update_one_response.status_code == status.HTTP_200_OK

    # Assert the response matches the updated data, excluding sensitive or irrelevant fields
    updated_user = test_update_one_response.json()
    assert updated_user.get('username') == test_update_one_request.get('username')
    assert updated_user.get('email') == test_update_one_request.get('email')
    assert updated_user.get('first_name') == test_update_one_request.get('first_name')
    assert updated_user.get('last_name') == test_update_one_request.get('last_name')
    assert updated_user.get('is_active') == test_update_one_request.get('is_active')
    assert updated_user.get('role') == test_update_one_request.get('role')
    assert updated_user.get('phone_number') == test_update_one_request.get('phone_number')

    # Verify sensitive fields like the password are not returned
    assert 'password' not in updated_user

    # Optional: Fetch the updated user via a GET request and validate consistency
    test_get_one_response = client.get(f"/api/v1/users/{test_user_id}")
    assert test_get_one_response.status_code == status.HTTP_200_OK
    fetched_user = test_get_one_response.json()
    assert fetched_user == updated_user


def test_update_one_authenticated_admin_invalid_email(test_users_and_admins):
    test_update_one_request = {
        "username": "testjohndoe",
        "email": "testjohndoemail.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": "testpassword",
        "is_active": True,
        "role": Role.USER.name,
        "phone_number": "111-111-1111"
    }

    test_user_id = 1

    test_update_one_response = client.put(f"/api/v1/users/{test_user_id}", json=test_update_one_request)
    assert test_update_one_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_one_authenticated_user(test_users_and_admins):
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_authenticated_user] = override_get_authenticated_user

    test_update_one_request = {
        "username": "testjohndoe",
        "email": "testjohndoe@email.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": "testpassword",
        "is_active": True,
        "role": Role.USER.name,
        "phone_number": "111-111-1111"
    }

    test_user_id = 1
    response = client.put(f"/api/v1/users/{test_user_id}", json=test_update_one_request)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {
        "detail": "You are not authorized to perform this action"
    }


def test_delete_one_authenticated_admin(test_users_and_admins):
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_authenticated_user] = override_get_authenticated_admin

    test_user_id = 1
    test_delete_one_response = client.delete(f"/api/v1/users/{test_user_id}")
    assert test_delete_one_response.status_code == status.HTTP_204_NO_CONTENT

    test_get_one_response = client.get(f"/api/v1/users/{test_user_id}")
    assert test_get_one_response.status_code == status.HTTP_404_NOT_FOUND
    assert test_get_one_response.json() == {'detail': f'User with id {test_user_id} not found'}


def test_delete_one_authenticated_admin_not_found(test_users_and_admins):
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_authenticated_user] = override_get_authenticated_admin

    test_user_id = 999
    test_delete_one_response = client.delete(f"/api/v1/users/{test_user_id}")
    assert test_delete_one_response.status_code == status.HTTP_404_NOT_FOUND
    assert test_delete_one_response.json() == {'detail': f'User with id {test_user_id} not found'}


def test_delete_one_authenticated_user(test_users_and_admins):
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_authenticated_user] = override_get_authenticated_user

    test_user_id = 1
    test_delete_one_response = client.delete(f"/api/v1/users/{test_user_id}")
    assert test_delete_one_response.status_code == status.HTTP_403_FORBIDDEN
    assert test_delete_one_response.json() == {
        "detail": "You are not authorized to perform this action"
    }


# Unauthenticated

def test_get_many_unauthenticated():
    app.dependency_overrides = {}
    response = client.get("/api/v1/users")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {
        "detail": "Not authenticated"
    }


def test_get_one_unauthenticated():
    app.dependency_overrides = {}
    test_user_id = 1
    response = client.get(f"/api/v1/users/{test_user_id}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {
        "detail": "Not authenticated"
    }


def test_update_one_unauthenticated():
    app.dependency_overrides = {}
    test_update_one_request = {
        "username": "testjohndoe",
        "email": "testjohndoe@email.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": "testpassword",
        "is_active": True,
        "role": Role.USER.name,
        "phone_number": "111-111-1111"
    }

    test_user_id = 1
    response = client.put(f"/api/v1/users/{test_user_id}", json=test_update_one_request)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {
        "detail": "Not authenticated"
    }


def test_delete_one_unauthenticated():
    app.dependency_overrides = {}

    test_user_id = 1
    response = client.delete(f"/api/v1/users/{test_user_id}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {
        "detail": "Not authenticated"
    }
