import uvicorn
from fastapi import FastAPI

from config.settings import get_settings
from database import database
from models import todo
from routers.v1 import todos

settings = get_settings()

todo.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.include_router(todos.router, prefix="/api/v1", tags=["Todos"])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
