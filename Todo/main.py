import uvicorn
from fastapi import FastAPI

from config.settings import get_settings
from data.database import sqlite
from data.models import todo, user
from routers.v1 import todos, auth, users

settings = get_settings()

todo.Base.metadata.create_all(bind=sqlite.engine)
user.Base.metadata.create_all(bind=sqlite.engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.include_router(todos.router, prefix="/api/v1", tags=["Todo"])
app.include_router(auth.router, prefix="/api/v1", tags=["Auth"])
app.include_router(users.router, prefix="/api/v1", tags=["User"])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
