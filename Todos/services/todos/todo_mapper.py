from ...data.models.todo import Todo
from ...schemas.request.todos_request import ManageOneRequest


def to_todo(request: ManageOneRequest, owner_id: int) -> Todo:
    created_todo: Todo = Todo(
        title=request.title,
        description=request.description,
        priority=request.priority,
        complete=request.complete,
        owner_id=owner_id
    )

    return created_todo


def update_todo(todo: Todo, request: ManageOneRequest) -> Todo:
    todo.title = request.title
    todo.description = request.description
    todo.priority = request.priority
    todo.complete = request.complete

    return todo
