from database.database import SessionDep
from services.todos_service import TodosService


def get_todos_service(session: SessionDep) -> TodosService:
    return TodosService(session)
