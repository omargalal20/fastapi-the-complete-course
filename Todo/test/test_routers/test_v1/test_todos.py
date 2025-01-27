from fastapi import status

from ...dependencies import *
from ...utils import *
from ....data.database.postgres import get_db
from ....middleware.security import get_authenticated_user

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_authenticated_user] = override_get_authenticated_user


def test_get_many_authenticated(test_todos):
    response = client.get("/api/v1/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == test_get_many_todos_authenticated_response


def test_get_one_authenticated(test_users_and_admins, test_todos):
    test_todo_id = 1
    response = client.get(f"/api/v1/todos/{test_todo_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == test_get_one_todos_authenticated_response


def test_get_one_authenticated_not_owner(test_users_and_admins, test_todos):
    test_todo_id = 2
    response = client.get(f"/api/v1/todos/{test_todo_id}")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {'detail': 'You are not authorized to perform this action'}


def test_get_one_authenticated_not_found(test_todos):
    test_todo_id = 999
    response = client.get(f"/api/v1/todos/{test_todo_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': f'Todo with id {test_todo_id} not found'}


def test_create_one_authenticated(test_users_and_admins, test_todos):
    test_create_one_request = {
        "title": "Complete FastAPI Course",
        "description": "Finish the FastAPI course by the end of the week",
        "priority": 5,
        "complete": False
    }
    test_create_one_response = client.post("/api/v1/todos", json=test_create_one_request)
    assert test_create_one_response.status_code == status.HTTP_201_CREATED
    assert test_create_one_response.json().get('title') == test_create_one_request.get('title')
    assert test_create_one_response.json().get('description') == test_create_one_request.get('description')
    assert test_create_one_response.json().get('priority') == test_create_one_request.get('priority')
    assert test_create_one_response.json().get('complete') == test_create_one_request.get('complete')

    test_get_one_response = client.get(f"/api/v1/todos/{test_create_one_response.json().get('id')}")
    assert test_get_one_response.status_code == status.HTTP_200_OK
    assert test_get_one_response.json() == {
        "id": test_create_one_response.json().get('id'),
        "title": test_create_one_response.json().get('title'),
        "description": test_create_one_response.json().get('description'),
        "priority": test_create_one_response.json().get('priority'),
        "complete": test_create_one_response.json().get('complete')
    }


def test_create_one_authenticated_invalid_request():
    test_todo_request = {
        "title": "",
        "description": "",
        "priority": 10,
        "complete": False
    }
    response = client.post("/api/v1/todos", json=test_todo_request)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {
        "detail": [
            {
                "type": "string_too_short",
                "loc": [
                    "body",
                    "title"
                ],
                "msg": "String should have at least 3 characters",
                "input": "",
                "ctx": {
                    "min_length": 3
                }
            },
            {
                "type": "string_too_short",
                "loc": [
                    "body",
                    "description"
                ],
                "msg": "String should have at least 3 characters",
                "input": "",
                "ctx": {
                    "min_length": 3
                }
            },
            {
                "type": "less_than",
                "loc": [
                    "body",
                    "priority"
                ],
                "msg": "Input should be less than 6",
                "input": 10,
                "ctx": {
                    "lt": 6
                }
            }
        ]
    }


def test_update_one_authenticated(test_users_and_admins, test_todos):
    test_todo_id = 1
    test_create_one_request = {
        "title": "Complete FastAPI Course",
        "description": "Finish the FastAPI course by the end of the week",
        "priority": 5,
        "complete": False
    }

    test_update_one_response = client.put(f"/api/v1/todos/{test_todo_id}", json=test_create_one_request)
    assert test_update_one_response.status_code == status.HTTP_200_OK
    assert test_update_one_response.json().get('title') == test_create_one_request.get('title')
    assert test_update_one_response.json().get('description') == test_create_one_request.get('description')
    assert test_update_one_response.json().get('priority') == test_create_one_request.get('priority')
    assert test_update_one_response.json().get('complete') == test_create_one_request.get('complete')

    test_get_one_response = client.get(f"/api/v1/todos/{test_update_one_response.json().get('id')}")
    assert test_get_one_response.status_code == status.HTTP_200_OK
    assert test_get_one_response.json() == {
        "id": test_update_one_response.json().get('id'),
        "title": test_update_one_response.json().get('title'),
        "description": test_update_one_response.json().get('description'),
        "priority": test_update_one_response.json().get('priority'),
        "complete": test_update_one_response.json().get('complete')
    }


def test_update_one_authenticated_not_owner(test_users_and_admins, test_todos):
    test_todo_id = 2
    test_update_one_request = {
        "title": "Complete FastAPI Course",
        "description": "Finish the FastAPI course by the end of the week",
        "priority": 5,
        "complete": False
    }
    response = client.put(f"/api/v1/todos/{test_todo_id}", json=test_update_one_request)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {'detail': 'You are not authorized to perform this action'}


def test_update_one_authenticated_invalid_request():
    test_todo_id = 1
    test_update_one_request = {
        "title": "",
        "description": "",
        "priority": 10,
        "complete": False
    }
    response = client.put(f"/api/v1/todos/{test_todo_id}", json=test_update_one_request)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {
        "detail": [
            {
                "type": "string_too_short",
                "loc": [
                    "body",
                    "title"
                ],
                "msg": "String should have at least 3 characters",
                "input": "",
                "ctx": {
                    "min_length": 3
                }
            },
            {
                "type": "string_too_short",
                "loc": [
                    "body",
                    "description"
                ],
                "msg": "String should have at least 3 characters",
                "input": "",
                "ctx": {
                    "min_length": 3
                }
            },
            {
                "type": "less_than",
                "loc": [
                    "body",
                    "priority"
                ],
                "msg": "Input should be less than 6",
                "input": 10,
                "ctx": {
                    "lt": 6
                }
            }
        ]
    }


def test_update_one_authenticated_not_found(test_todos):
    test_todo_id = 999
    test_update_one_request = {
        "title": "Complete FastAPI Course",
        "description": "Finish the FastAPI course by the end of the week",
        "priority": 5,
        "complete": False
    }
    response = client.put(f"/api/v1/todos/{test_todo_id}", json=test_update_one_request)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': f'Todo with id {test_todo_id} not found'}


def test_delete_one_authenticated(test_users_and_admins, test_todos):
    test_todo_id = 1

    test_delete_one_response = client.delete(f"/api/v1/todos/{test_todo_id}")
    assert test_delete_one_response.status_code == status.HTTP_204_NO_CONTENT

    test_get_one_response = client.get(f"/api/v1/todos/{test_todo_id}")
    assert test_get_one_response.status_code == status.HTTP_404_NOT_FOUND
    assert test_get_one_response.json() == {'detail': f'Todo with id {test_todo_id} not found'}


def test_delete_one_authenticated_not_owner(test_users_and_admins, test_todos):
    test_todo_id = 2
    response = client.get(f"/api/v1/todos/{test_todo_id}")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {'detail': 'You are not authorized to perform this action'}


def test_delete_one_authenticated_not_found(test_todos):
    test_todo_id = 999
    response = client.get(f"/api/v1/todos/{test_todo_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': f'Todo with id {test_todo_id} not found'}


# Unauthenticated

def test_get_many_unauthenticated():
    app.dependency_overrides = {}
    response = client.get("/api/v1/todos")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {
        "detail": "Not authenticated"
    }


def test_get_one_unauthenticated():
    app.dependency_overrides = {}
    test_todo_id = 2
    response = client.get(f"/api/v1/todos/{test_todo_id}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {
        "detail": "Not authenticated"
    }


def test_create_one_unauthenticated():
    app.dependency_overrides = {}
    test_create_one_request = {
        "title": "Complete FastAPI Course",
        "description": "Finish the FastAPI course by the end of the week",
        "priority": 5,
        "complete": False
    }
    response = client.post("/api/v1/todos", json=test_create_one_request)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {
        "detail": "Not authenticated"
    }


def test_update_one_unauthenticated():
    app.dependency_overrides = {}
    test_todo_id = 1
    test_create_one_request = {
        "title": "Complete FastAPI Course",
        "description": "Finish the FastAPI course by the end of the week",
        "priority": 5,
        "complete": False
    }
    response = client.put(f"/api/v1/todos/{test_todo_id}", json=test_create_one_request)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {
        "detail": "Not authenticated"
    }


def test_delete_one_unauthenticated():
    app.dependency_overrides = {}
    test_todo_id = 1
    response = client.get(f"/api/v1/todos/{test_todo_id}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {
        "detail": "Not authenticated"
    }
