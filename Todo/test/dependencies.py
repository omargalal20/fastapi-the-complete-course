import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ..data.models import todo, user
from ..data.models.todo import Todo
from ..data.models.user import Role, User
from ..main import app
from ..middleware.security import AuthenticatedUser
from ..middleware.security import get_password_hash

SQLALCHEMY_DATABASE_URL = "sqlite:///./test/testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

todo.Base.metadata.create_all(bind=engine)
user.Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


async def override_get_authenticated_user() -> AuthenticatedUser:
    return AuthenticatedUser(
        username="userjohndoe",
        id=1,
        role=Role.USER
    )


async def override_get_authenticated_admin() -> AuthenticatedUser:
    return AuthenticatedUser(
        username="adminjohndoe",
        id=3,
        role=Role.USER
    )


client = TestClient(app)


@pytest.fixture
def test_todos():
    todos = [
        Todo(title="Learn to code!", description="Need to learn everyday!", priority=5, complete=False, owner_id=1),
        Todo(title="Read a book", description="Read one chapter per day!", priority=3, complete=False, owner_id=2),
        Todo(title="Exercise", description="Workout for 30 minutes!", priority=4, complete=False, owner_id=1),
        Todo(title="Cook dinner", description="Try a new recipe!", priority=2, complete=False, owner_id=2),
        Todo(title="Meditate", description="Meditate for 10 minutes!", priority=1, complete=False, owner_id=1),
    ]

    db = TestingSessionLocal()
    db.add_all(todos)
    db.commit()

    yield todos

    with engine.connect() as connection:
        connection.execute(text("DELETE FROM Todo;"))
        connection.commit()


@pytest.fixture
def test_users_and_admins():
    users_and_admins = [
        User(
            username="userjohndoe",
            email="userjohndoe@email.com",
            first_name="John",
            last_name="Doe",
            password=get_password_hash("testpassword"),
            is_active=True,
            role=Role.USER,
            phone_number="(111)-111-1111",
        ),
        User(
            username="userjanedoe",
            email="userjanedoe@email.com",
            first_name="Jane",
            last_name="Doe",
            password=get_password_hash("testpassword"),
            is_active=True,
            role=Role.USER,
            phone_number="(222)-222-2222",
        ),
        User(
            username="adminjohndoe",
            email="adminjohndoe@email.com",
            first_name="John",
            last_name="Doe",
            password=get_password_hash("testpassword"),
            is_active=True,
            role=Role.ADMIN,
            phone_number="(333)-333-3333",
        ),
        User(
            username="adminjanedoe",
            email="adminjanedoe@email.com",
            first_name="Jane",
            last_name="Doe",
            password=get_password_hash("testpassword"),
            is_active=True,
            role=Role.ADMIN,
            phone_number="(444)-444-4444",
        ),
    ]

    db = TestingSessionLocal()
    db.add_all(users_and_admins)
    db.commit()

    yield users_and_admins

    with engine.connect() as connection:
        connection.execute(text("DELETE FROM User;"))
        connection.commit()
